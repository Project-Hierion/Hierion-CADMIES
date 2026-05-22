#!/usr/bin/env python3
"""
File: generate_relationships.py
Tool: CADMIES Relationship Generator
Version: 1.2.4
System: CADMIES / tools
Status: ACTIVE

Purpose: Feeds minted concepts to Mistral in small batches to propose
         cross-reference relationships. Uses ultra-light prompts
         (IDs + domains only) with one-shot examples for reliable JSON
         structure on CPU inference (~40s per batch).

         Two-phase strategy:
           Phase 1: Intra-batch edges (15 concepts per batch)
           Phase 2: Cross-batch bridges (8 ambassadors per call)

         No timeouts, no stop tokens — num_predict=256 is the only cap.

Usage:
    python tools/generate_relationships.py           # Dry run — preview only
    python tools/generate_relationships.py --write   # Apply edges to blockstore
    python tools/generate_relationships.py --incremental  # Only sparse concepts

Lessons Learned (2026-05-09):
    - One-shot examples in prompts fix JSON structure issues
    - "stop" token cuts off JSON → removed; num_predict is enough
    - Mistral invents IDs/types → strict rules + example in prompt
    - signal.alarm() conflicts with ollama.generate → removed
    - Trailing commas before } or ] → stripped in call_mistral()

Changelog (2026-05-21 — v1.2.4):
    - Phase 47 fix: write step now validates target exists in full blockstore
      index before appending edge. Prevents orphan edges from deleted/renamed
      concepts. Skips with log message instead of silently creating ghost edges.
"""

import json
import sys
import time
from pathlib import Path
from collections import defaultdict

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR
from cid_generator import CIDGenerator
import dag_cbor

# === CONFIG ===
MODEL = "mistral:7b"
DELAY = 2
BATCH_SIZE = 15
BRIDGE_BATCH_SIZE = 8
VALID_RELATION_TYPES = ["builds_upon", "related_to", "specializes", "contradicts"]


# ============================================================================
# DATA GATHERING
# ============================================================================

def gather_concept_summaries():
    """Load all concepts from blockstore. Returns summaries dict and CID mapping."""
    all_cids = load_all_concept_cids()
    summaries = {}
    cid_map = {}
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        hid = concept.get('human_id', '')
        summaries[hid] = {
            'title': concept.get('title', hid.replace('_', ' ').title()),
            'domain': concept.get('domain', 'Unknown'),
            'relationships': concept.get('relationships', {}),
        }
        cid_map[hid] = cid
    return summaries, cid_map


# ============================================================================
# PROMPT BUILDERS — One-shot examples force correct JSON structure
# ============================================================================

def build_intra_batch_prompt(batch_ids, summaries):
    """Send ONLY concept IDs — no domains, no titles, no brackets."""
    ids_only = "\n".join(batch_ids)
    
    return f"""Propose relationships between these concept IDs.

{ids_only}

CRITICAL RULES:
- Use the EXACT IDs listed directly above this sentence as both keys and targets
- ONLY use types: builds_upon, related_to, specializes, contradicts
- Every ID listed above must appear as a key, even with empty array

Return ONLY this exact structure:
{{"relationships": {{"concept_id": [{{"target": "other_id", "type": "builds_upon"}}], "other_id": []}}}}"""

def build_bridge_prompt(ambassadors, summaries):
    """
    Build prompt for cross-batch bridges.
    Same one-shot example pattern as intra-batch.
    """
    lines = []
    for hid in ambassadors:
        s = summaries[hid]
        lines.append(f"{hid} [{s['domain']}]")
    concept_block = "\n".join(lines)

    return f"""Find cross-domain connections between these concepts.

CRITICAL: Return EXACTLY this JSON structure — an OBJECT keyed by source ID,
each containing an ARRAY of edge objects:

EXAMPLE for concepts entropy, consciousness:
{{"relationships": {{"entropy": [{{"target":"consciousness","type":"related_to"}}], "consciousness": []}}}}

Now do the same for these concepts. Use the EXACT concept IDs shown.
ONLY use types: related_to, builds_upon, contradicts.
Do NOT invent new IDs or types. Include EVERY concept as a key, even if empty array.

{concept_block}

Return ONLY the JSON (no markdown, no commentary):"""

# ============================================================================
# MISTRAL INTERFACE — No timeout, no stop tokens, trailing comma fix
# ============================================================================

def call_mistral(prompt, step_name):
    """
    Send prompt to Mistral and parse JSON response.
    No timeout, no stop tokens — num_predict=512 is the only cap.
    Robust JSON extraction handles prose, markdown fences, bare objects.
    Trailing commas stripped before JSON parse (common Mistral quirk).
    Failed JSON saved to tools/raw_*.txt for debugging.
    """
    import ollama
    import re

    est_tokens = len(prompt.split())
    print(f"  Mistral <- {est_tokens} tokens...", end=" ", flush=True)

    raw = None
    try:
        response = ollama.generate(
            model=MODEL,
            prompt=prompt,
            options={
                "num_predict": 512,
                "temperature": 0.1,
            }
        )
        raw = response["response"].strip()
        print(f"-> {len(raw)} chars", end=" ", flush=True)

        # Robust JSON extraction — handles prose before/after fences
        # Pattern 1: ```json ... ``` or ``` ... ``` fences anywhere in response
        match = re.search(r'```(?:json)?\s*\n?(\{.*?\})\s*```', raw, re.DOTALL)
        if match:
            raw = match.group(1).strip()
        else:
            # Pattern 2: Find the first { ... } object (handles prose-before-JSON with no fences)
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                raw = match.group(0).strip()

        # Fix trailing commas (Mistral JSON quirk)
        raw = raw.replace(", }", "}")
        raw = raw.replace(", ]", "]")
        raw = raw.replace(",}", "}")
        raw = raw.replace(",]", "]")

        data = json.loads(raw)
        rels = data.get("relationships", {})
        edge_count = sum(len(v) for v in rels.values())
        print(f"-> {edge_count} edges")
        return rels

    except json.JSONDecodeError:
        print(f"BAD JSON")
        if raw:
            dump_path = TOOLS_DIR / f"raw_{step_name.replace(' ', '_')}.txt"
            with open(dump_path, "w") as f:
                f.write(raw)
            print(f"    Saved: {dump_path}")
        return {}
    except Exception as e:
        print(f"ERROR: {e}")
        return {}


# ============================================================================
# VALIDATION
# ============================================================================

def filter_valid_edges(relationships, valid_ids):
    """
    Keep only edges with valid targets, types, and structure.
    Reports how many edges were filtered out (Mistral hallucinations).
    """
    filtered = defaultdict(list)
    filtered_out = 0
    for source, edges in relationships.items():
        if source not in valid_ids:
            if isinstance(edges, list):
                filtered_out += len(edges)
            continue
        if not isinstance(edges, list):
            filtered_out += 1
            continue
        for edge in edges:
            if not isinstance(edge, dict):
                filtered_out += 1
                continue
            target = edge.get("target", "")
            rel_type = edge.get("type", "")
            if isinstance(target, str) and target in valid_ids and target != source and rel_type in VALID_RELATION_TYPES:
                filtered[source].append({"target": target, "type": rel_type})
            else:
                filtered_out += 1

    if filtered_out:
        print(f"      ({filtered_out} invalid edge(s) filtered)")
    return filtered


# ============================================================================
# HEALTH CHECK
# ============================================================================

def test_ollama():
    """Quick connectivity test. Fails fast if Ollama is down."""
    import ollama
    try:
        response = ollama.generate(
            model=MODEL,
            prompt="Say OK",
            options={"num_predict": 3}
        )
        return "OK" in response["response"]
    except Exception as e:
        print(f"  Ollama test failed: {e}")
        return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    write_mode = "--write" in sys.argv
    incremental = "--incremental" in sys.argv

    print("=" * 60)
    print("CADMIES RELATIONSHIP GENERATOR v1.2.4")
    print(f"Model: {MODEL}  |  Batch: {BATCH_SIZE}  |  Delay: {DELAY}s")
    print(f"Mode: {'WRITE' if write_mode else 'DRY RUN (preview only)'}")
    print(f"Filter: {'INCREMENTAL (sparse only)' if incremental else 'FULL (all concepts)'}")
    print("=" * 60)

    # Health check
    print("\nTesting Ollama connection...", end=" ", flush=True)
    if not test_ollama():
        print("FAILED")
        print("Restart Ollama:  pkill ollama && OLLAMA_KEEP_ALIVE=24h ollama serve &")
        sys.exit(1)
    print("OK")

    # Load concepts
    summaries, cid_map = gather_concept_summaries()
    all_ids = sorted(summaries.keys())
    print(f"Loaded {len(all_ids)} concepts from blockstore")

    # Incremental mode
    if incremental:
        all_ids = [
            hid for hid in all_ids
            if sum(
                len(v) for v in summaries[hid].get('relationships', {}).values()
                if isinstance(v, list)
            ) < 3
        ]
        print(f"Incremental: {len(all_ids)} sparse concepts")
        if not all_ids:
            print("All concepts have sufficient relationships. Nothing to do.")
            return

    all_relationships = defaultdict(list)

    # === PHASE 1: Intra-batch edges ===
    batches = [all_ids[i:i+BATCH_SIZE] for i in range(0, len(all_ids), BATCH_SIZE)]
    print(f"\n{'='*40}")
    print(f"PHASE 1: Intra-batch edges ({len(batches)} batches)")
    print(f"{'='*40}")

    for i, batch in enumerate(batches):
        step = f"batch{i+1}"
        print(f"\nBatch {i+1}/{len(batches)} ({len(batch)} concepts)")
        prompt = build_intra_batch_prompt(batch, summaries)
        relationships = call_mistral(prompt, step)
        filtered = filter_valid_edges(relationships, set(batch))
        for source, edges in filtered.items():
            all_relationships[source].extend(edges)
        sys.stdout.flush()
        if i < len(batches) - 1:
            time.sleep(DELAY)

    # === PHASE 2: Cross-batch bridges ===
    if len(batches) > 1:
        ambassadors = [b[0] for b in batches]
        bridge_batches = [ambassadors[i:i+BRIDGE_BATCH_SIZE] for i in range(0, len(ambassadors), BRIDGE_BATCH_SIZE)]
        print(f"\n{'='*40}")
        print(f"PHASE 2: Cross-batch bridges ({len(bridge_batches)} bridge batches)")
        print(f"{'='*40}")

        for i, bridge in enumerate(bridge_batches):
            step = f"bridge{i+1}"
            print(f"\nBridge {i+1}/{len(bridge_batches)} ({len(bridge)} ambassadors)")
            prompt = build_bridge_prompt(bridge, summaries)
            relationships = call_mistral(prompt, step)
            filtered = filter_valid_edges(relationships, set(bridge))
            for source, edges in filtered.items():
                all_relationships[source].extend(edges)
            sys.stdout.flush()
            if i < len(bridge_batches) - 1:
                time.sleep(DELAY)

    # === DEDUPLICATE ===
    for hid in all_relationships:
        seen = set()
        unique = []
        for edge in all_relationships[hid]:
            key = (edge["target"], edge["type"])
            if key not in seen and edge["target"] != hid:
                seen.add(key)
                unique.append(edge)
        all_relationships[hid] = unique

    total_edges = sum(len(v) for v in all_relationships.values())
    print(f"\n{'='*60}")
    print(f"RESULTS: {total_edges} total edges across {len(all_relationships)} concepts")
    print(f"{'='*60}")

    if total_edges == 0:
        print("\nNo edges generated. Possible issues:")
        print("  - All proposed edges failed validation (check raw_*.txt)")
        print("  - Try BATCH_SIZE=10 for more focused proposals")
        return

    # Preview
    print("\nSample relationships:")
    count = 0
    for hid in sorted(all_relationships.keys()):
        if all_relationships[hid] and count < 12:
            edge_strs = [f"[{e['type']}] {e['target']}" for e in all_relationships[hid][:3]]
            print(f"  {hid}: {', '.join(edge_strs)}")
            count += 1

    if not write_mode:
        print(f"\n⚠️  DRY RUN complete. {total_edges} edges proposed but NOT written.")
        print(f"   Review the sample above. If it looks good, run:")
        print(f"   python tools/generate_relationships.py --write")
        return

    # === WRITE TO BLOCKSTORE ===
    print(f"\n{'='*60}")
    print(f"Writing {total_edges} edges to blockstore...")
    print(f"{'='*60}")

    cid_gen = CIDGenerator()
    updated = 0
    skipped_orphans = 0
    for hid, new_edges in all_relationships.items():
        if not new_edges:
            continue
        cid = cid_map.get(hid)
        if not cid:
            continue
        concept = load_concept(cid)
        if 'error' in concept:
            print(f"  WARNING: Could not load {hid} — skipping")
            continue
        rels = concept.get('relationships', {})
        for edge in new_edges:
            t = edge['type']
            target = edge['target']

            # Phase 47 fix: validate target exists in full blockstore index
            if target not in cid_map:
                print(f"  SKIP: target '{target}' not in blockstore (orphan prevented)")
                skipped_orphans += 1
                continue

            if t not in rels:
                rels[t] = []
            if target not in rels[t]:
                rels[t].append(target)
        concept['relationships'] = rels
        cbor_path = BLOCKS_DIR / f"{cid}.cbor"
        if not cbor_path.exists():
            cbor_path = BLOCKS_DIR / cid
        with open(cbor_path, 'wb') as f:
            f.write(dag_cbor.encode(concept))
        updated += 1

    print(f"✅ Updated {updated} concepts in blockstore")
    if skipped_orphans:
        print(f"⚠️  Skipped {skipped_orphans} orphan edge(s) — target(s) not in blockstore")
    print(f"   Run: python tools/generate_mycelium_map.py")
    print(f"   Then open mycelium_map.html in Firefox.")


if __name__ == "__main__":
    main()