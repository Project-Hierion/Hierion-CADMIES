#!/usr/bin/env python3
"""
File: harvest_full_pipeline.py
Tool: CADMIES Harvest Pipeline
Version: 4.2.0
System: CADMIES / tools/harvest
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: End-to-end conversation harvesting pipeline. Chunks a conversation,
         queries the mycelium for context, extracts concepts + poetics + mantras
         via Mistral, saves to source_concepts/, presents interactive review,
         validates, and mints approved concepts into the IPLD blockstore.
         LLM-optional: falls back to manual import mode if Mistral is unavailable.

Usage:
    python tools/harvest/harvest_full_pipeline.py
    python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
    python tools/harvest/harvest_full_pipeline.py --model=codestral
    python tools/harvest/harvest_full_pipeline.py --batch

Version History:
  v4.2.0: Fixed mycelium search import (llm_mycelium_reader → cadmies_concept_reader).
  v4.1.0: Three-tier difficulty levels: beginner/intermediate/expert.
  v4.0.1: Hardened: apostrophe escaping, human_id lowercase, builds_upon validation.
  v4.0.0: Full pipeline: extract → review → validate → mint, LLM-optional mode.
  v3.0.0: Poetic version and mantra extraction.
  v2.0.0: Mycelium-aware extraction via mycelium search.
  v1.0.0: Initial extraction pipeline.
"""

import json
import sys
import time
import re
from pathlib import Path
from datetime import datetime, timezone

def deduplicate_concepts(concept_list):
    """Remove duplicate concepts based on title similarity."""
    if not concept_list or len(concept_list) <= 1:
        return concept_list
    
    seen = {}
    unique = []
    for c in concept_list:
        title = c.get('title', '').lower().strip()
        if title and title not in seen:
            seen[title] = True
            unique.append(c)
    
    print(f"   Deduplication: {len(concept_list)} → {len(unique)} concepts")
    return unique

# === PATH SETUP ===
HARVEST_DIR = Path(__file__).parent
PROJECT_ROOT = HARVEST_DIR.parent.parent

# === CONFIG ===
CONVERSATION_FILE = HARVEST_DIR / "conversation.json"
OUTPUT_FILE = HARVEST_DIR / "harvested_concepts.json"
SOURCE_CONCEPTS_DIR = PROJECT_ROOT / "source_concepts"
MODEL = "mistral:7b"
CHUNK_SIZE = 750
DELAY = 10
RELEVANCE_THRESHOLD = 0.1
DEFAULT_CERTAINTY = 0.8
VALIDATION_LEVEL = "BASIC"

# === LLM DETECTION ===
try:
    import ollama
    result = ollama.list()
    if hasattr(result, 'models'):
        available_models = [m.model for m in result.models]
    else:
        available_models = []
    if MODEL in available_models:
        LLM_AVAILABLE = True
    else:
        print(f"WARNING: Model '{MODEL}' not found. LLM extraction disabled.")
        print(f"  Available models: {available_models}")
        LLM_AVAILABLE = False
except Exception as e:
    print(f"WARNING: Ollama unavailable ({e}). LLM extraction disabled.")
    LLM_AVAILABLE = False

# === MYCELIUM SEARCH ===
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
try:
    from cadmies_concept_reader import search_mycelium, load_all_concept_cids, load_concept
    MYCELIUM_AVAILABLE = True
except ImportError:
    MYCELIUM_AVAILABLE = False
    print("WARNING: Mycelium search unavailable — proceeding without context.")

# === CID GENERATOR ===
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))
from cid_generator import CIDGenerator
from scientific_validator import ScientificValidator
from provenance_manager import ProvenanceManager

# === EXTRACTION PROMPT ===
EXTRACTION_PROMPT = """You are a philosophical concept extractor for the CADMIES knowledge system.

CRITICAL RULES:
- "name" MUST be lowercase_snake_case (e.g., "gravitomotive_gearbox", not "Gravitomotive_Gearbox").
- "builds_upon", "related_to", and "contradicts" MUST reference EXISTING human_ids from the list above, OR be empty lists []. Do NOT invent phrases or descriptions here.

IMPORTANT: Extract only 1-3 broad, high-level concepts. Do NOT break insights into small granular pieces. Prefer unified, philosophical concepts over micro-observations. Quality over quantity.

Extract NEW concepts, a poetic version, and a mantra from this conversation.

For each concept, provide THREE distinct explanations at different difficulty levels:
- beginner_explanation: ELI5 — simple language, relatable metaphor, no jargon. Someone with no background should understand it.
- intermediate_explanation: Proper terminology, connects to related concepts, assumes basic familiarity with the domain.
- expert_explanation: Full depth, philosophical implications, edge cases, connections to other fields. The insight that makes this concept novel.

Existing concepts (DO NOT extract these — reference only):
{mycelium_context}

Return a single JSON object with EXACTLY this structure. Concepts MUST be objects with all fields shown — NOT strings, NOT topic names:

{{
  "concepts": [
    {{
      "name": "snake_case_concept_name",
      "definition": "Clear 1-3 sentence canonical definition of the concept.",
      "domain": "Physics",
      "beginner_explanation": "Simple explanation with a relatable metaphor. No jargon.",
      "intermediate_explanation": "Explanation using proper terminology. Connects to related ideas.",
      "expert_explanation": "Full depth. Philosophical implications, edge cases, novel insight.",
      "insight": "The novel or noteworthy observation from the conversation.",
      "builds_upon": [],
      "related_to": [],
      "contradicts": []
    }}
  ],
  "poetic_version": "A single short poetic phrase (1-2 lines maximum) capturing the core insight. NOT a full poem.",
  "mantra": "A short repeatable phrase that encapsulates the core realization."
}}

Return ONLY the JSON object. No markdown fences. No introductory text. No commentary. JUST the JSON.

CONVERSATION:
{chunk}"""


def load_conversation_robust(filepath):
    """Load conversation text from JSON, handling unescaped newlines and apostrophes."""
    with open(filepath, "r") as f:
        raw_text = f.read().strip()

    try:
        data = json.loads(raw_text)
        return data.get("content", raw_text)
    except json.JSONDecodeError:
        pass

    content_key = '"content":'
    key_pos = raw_text.find(content_key)
    if key_pos == -1:
        raise ValueError("Could not find 'content' key in JSON file")

    value_start = key_pos + len(content_key)
    raw_value = raw_text[value_start:].strip()

    last_brace = raw_value.rfind('}')
    if last_brace != -1:
        raw_value = raw_value[:last_brace].strip()

    if raw_value.startswith('"') and raw_value.endswith('"'):
        raw_value = raw_value[1:-1]

    raw_value = re.sub(r"(?<!\\)'", r"\\'", raw_value)

    print("  (used robust loader)")
    return raw_value


def get_mycelium_context(conversation_text):
    """Search mycelium for relevant existing concepts."""
    if not MYCELIUM_AVAILABLE:
        return "Mycelium search unavailable."

    print("\n  Searching mycelium...")
    all_cids = load_all_concept_cids()
    results = search_mycelium(conversation_text, all_cids)
    relevant = [r for r in results if r['relevance_score'] >= RELEVANCE_THRESHOLD]

    if not relevant:
        print(f"  No concepts above threshold ({RELEVANCE_THRESHOLD})")
        return "No strongly relevant existing concepts found."

    print(f"  Found {len(relevant)} relevant concepts:")
    context_parts = []
    for i, r in enumerate(relevant):
        cid = r['cid']
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        human_id = concept.get('human_id', '')
        title = concept.get('title', 'Unknown')
        definition = concept.get('definition', '')[:500]
        domain = concept.get('domain', 'Unknown')
        print(f"    {i+1}. {human_id} [{domain}] (score: {r['relevance_score']:.3f})")
        context_parts.append(f"CONCEPT {i+1}: human_id: {human_id}, title: {title}, domain: {domain}, definition: {definition}")
    return "\n".join(context_parts)


def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of roughly chunk_size words."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def extract_from_chunk(chunk, mycelium_context, index, total):
    """Send chunk to Mistral, parse response."""
    prompt = EXTRACTION_PROMPT.format(mycelium_context=mycelium_context, chunk=chunk)
    print(f"\n  Chunk {index+1}/{total} ({len(chunk.split())} words)...")

    try:
        response = ollama.generate(model=MODEL, prompt=prompt)
        raw = response["response"].strip()

        while raw.startswith("```"):
            raw = raw.lstrip("`")
            if "\n" in raw:
                raw = raw.split("\n", 1)[1]
        while raw.endswith("```"):
            raw = raw.rstrip("`")
        raw = raw.strip()

        brace_pos = raw.find("{")
        if brace_pos > 0:
            raw = raw[brace_pos:]
        result = json.loads(raw, strict=False)
        concepts = result.get("concepts", [])
        poetic = result.get("poetic_version", "")
        mantra = result.get("mantra", "")
        print(f"  -> {len(concepts)} concept(s), poetics: {'yes' if poetic else 'no'}, mantra: {'yes' if mantra else 'no'}")
        return {"concepts": concepts, "poetic_version": poetic, "mantra": mantra}

    except json.JSONDecodeError:
        dump_path = HARVEST_DIR / f"raw_failed_chunk_{index+1}.txt"
        with open(dump_path, "w") as f:
            f.write(raw)
        print(f"  WARNING: JSON parse failed. Raw output saved to {dump_path}")
        return {"concepts": [{"error": "json_parse_failed", "raw_output": raw}], "poetic_version": "", "mantra": ""}
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"concepts": [], "poetic_version": "", "mantra": ""}


def import_from_source_concepts(source_dir, minted_ids=None):
    """Load unminted concept JSONs from source_concepts/ for review/minting."""
    if minted_ids is None:
        minted_ids = set()

    minted_ids_lower = {mid.lower() for mid in minted_ids}

    if not source_dir.exists():
        print("  No source_concepts/ directory found.")
        return [], [], [], []

    json_files = sorted(source_dir.glob("*.json"))
    if not json_files:
        print("  No JSON files in source_concepts/.")
        return [], [], [], []

    concepts_full = []
    concept_files = []
    skipped = 0
    for jf in json_files:
        try:
            with open(jf, "r") as f:
                concept = json.load(f)
            human_id = concept.get("human_id", jf.stem)
            if human_id.lower() in minted_ids_lower:
                skipped += 1
                continue
            domain = concept.get("domain", "unknown")
            print(f"    • {jf.name}  [{domain}]")
            concepts_full.append(concept)
            concept_files.append(jf)
        except Exception as e:
            print(f"    WARNING: Skipping {jf.name} — {e}")

    if skipped:
        print(f"  ({skipped} already-minted concept(s) skipped)")

    return concept_files, concepts_full, [], []


def transform_to_concept(extracted, chunk_index, minted_ids=None):
    """Transform Mistral output to UniversalScientificConcept schema."""
    if minted_ids is None:
        minted_ids = set()

    name = extracted.get("name", "unnamed_concept").lower()
    title = name.replace("_", " ").title()
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    raw_builds_upon = extracted.get("builds_upon", []) or []
    raw_related_to = extracted.get("related_to", []) or []
    raw_contradicts = extracted.get("contradicts", []) or []

    minted_lower = {mid.lower() for mid in minted_ids}
    builds_upon = [b for b in raw_builds_upon if isinstance(b, str) and b.lower() in minted_lower]
    related_to = [r for r in raw_related_to if isinstance(r, str) and r.lower() in minted_lower]
    contradicts = [c for c in raw_contradicts if isinstance(c, str) and c.lower() in minted_lower]

    filtered_bu = set(raw_builds_upon) - set(builds_upon)
    filtered_rt = set(raw_related_to) - set(related_to)
    filtered_ct = set(raw_contradicts) - set(contradicts)
    if filtered_bu or filtered_rt or filtered_ct:
        print(f"  NOTE: Filtered invalid references from {name}:")
        if filtered_bu:
            print(f"    builds_upon: {filtered_bu}")
        if filtered_rt:
            print(f"    related_to: {filtered_rt}")
        if filtered_ct:
            print(f"    contradicts: {filtered_ct}")

    beginner_explanation = extracted.get("beginner_explanation", "")
    intermediate_explanation = extracted.get("intermediate_explanation", "")
    expert_explanation = extracted.get("expert_explanation", "")
    definition = extracted.get("definition", "")
    insight = extracted.get("insight", "")

    if not beginner_explanation:
        beginner_explanation = definition
    if not intermediate_explanation:
        intermediate_explanation = definition
    if not expert_explanation:
        expert_explanation = insight if insight else definition

    return {
        "schema_version": "1.0.0",
        "human_id": name,
        "title": title,
        "definition": definition,
        "type": "Concept",
        "domain": extracted.get("domain", "Unknown"),
        "subdomain": "",
        "proofs": [
            {
                "type": "conversation_extraction",
                "description": f"Extracted from conversation via {MODEL}",
                "confidence": DEFAULT_CERTAINTY,
                "date": now,
                "reference": f"CADMIES Harvest Pipeline — {CONVERSATION_FILE.name}"
            }
        ],
        "metadata": {
            "created": now,
            "creator": "CADMIES Harvest Pipeline",
            "certainty_score": DEFAULT_CERTAINTY,
            "version": 1,
            "license": "CC BY-SA 4.0",
            "purpose": "educational",
            "supersedes": None,
            "superseded_by": None
        },
        "relationships": {
            "builds_upon": builds_upon,
            "contradicts": contradicts,
            "related_to": related_to,
            "specializes": []
        },
        "difficulty_levels": {
            "beginner": beginner_explanation,
            "intermediate": intermediate_explanation,
            "expert": expert_explanation
        },
        "learning_path": {
            "prerequisites": builds_upon,
            "next_steps": []
        },
        "cross_references": {},
        "extra_fields": {
            "insight": insight,
            "source_chunk": chunk_index + 1,
            "origin_file": CONVERSATION_FILE.name,
            "harvester_version": "4.2.0"
        }
    }


def save_concept_json(concept, source_dir):
    """Save concept to source_concepts/{human_id}.json."""
    source_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{concept['human_id']}.json"
    filepath = source_dir / filename

    if filepath.exists():
        print(f"  WARNING: {filename} exists — overwriting.")

    with open(filepath, "w") as f:
        json.dump(concept, f, indent=2)

    return filepath


def merge_concepts(all_results):
    """Merge and deduplicate concepts across chunks."""
    seen = set()
    merged = []
    for result in all_results:
        for c in result.get("concepts", []):
            name = c.get("name", "")
            if name and name not in seen:
                seen.add(name)
                merged.append(c)
    return merged


def merge_poetics(all_results):
    """Collect poetics and mantras."""
    poetics, mantras = [], []
    for r in all_results:
        if r.get("poetic_version"):
            poetics.append(r["poetic_version"])
        if r.get("mantra"):
            mantras.append(r["mantra"])
    return poetics, mantras


def display_review_menu(concept_files, concepts, poetics, mantras):
    """Interactive review menu."""
    while True:
        print(f"\n{'='*60}")
        print(f"{len(concept_files)} CONCEPT(S) READY FOR REVIEW")
        print(f"{'='*60}")
        for i, (cf, c) in enumerate(zip(concept_files, concepts)):
            domain = c.get("domain", "unknown")
            print(f"  {i+1}. {cf.name}  [{domain}]")
        if poetics:
            print(f"\n  Poetic versions: {len(poetics)}")
        if mantras:
            print(f"  Mantras: {len(mantras)}")
        print(f"\n  [V]iew  [L]ist definitions  [A]pprove all & mint  [M]int specific  [S]kip  [Q]uit")
        choice = input("  > ").strip().upper()

        if choice == "Q":
            return None
        elif choice == "S":
            print("  Skipping mint. Concepts saved to source_concepts/.")
            return []
        elif choice == "A":
            return list(range(len(concepts)))
        elif choice == "L":
            for i, c in enumerate(concepts):
                print(f"\n  {i+1}. {c.get('human_id', 'unknown')}")
                print(f"     {c.get('definition', '')[:120]}...")
        elif choice.startswith("V"):
            try:
                idx = int(choice[1:].strip()) - 1
                if 0 <= idx < len(concepts):
                    print(f"\n  {'='*40}")
                    print(json.dumps(concepts[idx], indent=2))
                    print(f"  {'='*40}")
                else:
                    print("  Invalid number.")
            except ValueError:
                print("  Usage: V 1, V 2, etc.")
        elif choice.startswith("M"):
            try:
                nums = [int(x.strip()) - 1 for x in choice[1:].split(",")]
                valid = [n for n in nums if 0 <= n < len(concepts)]
                if valid:
                    return valid
                print("  No valid numbers.")
            except ValueError:
                print("  Usage: M 1,3,5")
        else:
            print("  Unknown command.")


def validate_concept(concept):
    """Run scientific validator."""
    validator = ScientificValidator(VALIDATION_LEVEL)
    is_valid, errors, report = validator.validate(concept)
    if not is_valid:
        print(f"  VALIDATION FAILED: {concept.get('human_id', 'unknown')}")
        for e in errors:
            print(f"    - {e}")
    return is_valid, errors


def mint_concept(concept, cid_gen, pm):
    """Generate CID, save to blockstore, create provenance. Return result dict."""
    human_id = concept.get("human_id", "unknown")

    is_valid, errors = validate_concept(concept)
    if not is_valid:
        return {"success": False, "human_id": human_id, "error": "validation_failed", "details": errors}

    cid_result = cid_gen.generate_cid(concept)
    if not cid_result["success"]:
        return {"success": False, "human_id": human_id, "error": "cid_generation_failed", "details": cid_result.get("errors", [])}

    save_result = cid_gen.save_to_blockstore(cid_result, concept)
    if not save_result["success"]:
        return {"success": False, "human_id": human_id, "error": "blockstore_save_failed", "details": save_result.get("errors", [])}

    try:
        pm.create_provenance_record(
            concept_cid=cid_result["cid"],
            author="CADMIES Harvest Pipeline",
            record_type="creation",
            comment=f"Extracted from conversation via {MODEL}" if LLM_AVAILABLE else "Imported from source_concepts/ via manual mode"
        )
    except Exception as e:
        print(f"  WARNING: Provenance creation failed for {human_id}: {e}")

    return {
        "success": True,
        "human_id": human_id,
        "cid": cid_result["cid"],
        "hash_preview": cid_result.get("hash_preview", ""),
        "bytes_size": cid_result.get("bytes_size", 0)
    }


def mint_approved(indices, concepts, concept_files, poetics, mantras):
    """Mint approved concepts. Save poetics/mantras to extra_fields."""
    if not indices:
        return

    cid_gen = CIDGenerator()
    pm = ProvenanceManager()
    results = []

    print(f"\n{'='*60}")
    print(f"MINTING {len(indices)} CONCEPT(S) TO MYCELIUM...")
    print(f"{'='*60}")

    for idx in indices:
        concept = concepts[idx]
        if "extra_fields" not in concept:
            concept["extra_fields"] = {}
        if poetics:
            concept["extra_fields"]["poetic_versions"] = poetics
        if mantras:
            concept["extra_fields"]["mantras"] = mantras

        print(f"\n  Minting: {concept['human_id']}...")
        result = mint_concept(concept, cid_gen, pm)
        results.append(result)

        if result["success"]:
            print(f"  ✅ {result['human_id']}")
            print(f"     CID: {result['cid']}")
            print(f"     Size: {result['bytes_size']} bytes")
        else:
            print(f"  ❌ {result['human_id']} — {result['error']}")

    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    print(f"\n{'='*60}")
    print(f"MINTING COMPLETE: {len(successes)} successful, {len(failures)} failed")
    if successes:
        print("  These concepts are now live in the mycelium.")
    print(f"{'='*60}")

    return results


def parse_args():
    """Parse command-line flags."""
    args = {
        "model": MODEL,
        "auto": False,
        "batch": False,
        "with_relationships": False,
        "conversation": str(CONVERSATION_FILE),
    }
    for arg in sys.argv[1:]:
        if arg.startswith("--model="):
            args["model"] = arg.split("=", 1)[1]
        elif arg == "--auto":
            args["auto"] = True
        elif arg == "--batch":
            args["batch"] = True
        elif arg == "--with-relationships":
            args["with_relationships"] = True
        elif arg.startswith("--conv="):
            args["conversation"] = arg.split("=", 1)[1]
    return args

def main():
    args = parse_args()
    global MODEL
    MODEL = args["model"]
    print("=" * 60)
    print("CADMIES HARVEST PIPELINE v4.2.0")
    print(f"Model: {MODEL}  |  Chunk Size: {CHUNK_SIZE} words  |  Auto: {args['auto']}  |  Batch: {args['batch']}  |  With-Relationships: {args['with_relationships']}")
    print(f"LLM: {'AVAILABLE' if LLM_AVAILABLE else 'UNAVAILABLE — manual mode'}")
    print(f"Mycelium: {'ENABLED' if MYCELIUM_AVAILABLE else 'DISABLED'}")
    print("=" * 60)
    print("\a")

    minted_ids = set()
    index_path = PROJECT_ROOT / "store" / "index" / "human_id_to_cid.json"
    if index_path.exists():
        try:
            with open(index_path, "r") as f:
                minted_ids = set(json.load(f).keys())
        except Exception:
            pass

    if args["batch"]:
        conv_dir = HARVEST_DIR / "conversations"
        conv_dir.mkdir(exist_ok=True)
        conv_files = sorted(conv_dir.glob("*.json"))
        if not conv_files:
            print(f"No conversation files found in {conv_dir}")
            print("Add .json files there and re-run with --batch")
            sys.exit(0)
        print(f"Batch mode: {len(conv_files)} conversation(s) found")
        for conv_file in conv_files:
            print(f"\n{'='*60}")
            print(f"Processing: {conv_file.name}")
            print(f"{'='*60}")
        print(f"\nBatch complete. {len(conv_files)} files processed.")
        sys.exit(0)
    
    if LLM_AVAILABLE and CONVERSATION_FILE.exists():
        text = load_conversation_robust(CONVERSATION_FILE)
        print(f"\nLoaded: {len(text.split())} words from {CONVERSATION_FILE.name}")

        mycelium_context = get_mycelium_context(text)

        chunks = chunk_text(text)
        print(f"\nSplit into {len(chunks)} chunk(s)")

        all_results = []
        for i, chunk in enumerate(chunks):
            try:
                result = extract_from_chunk(chunk, mycelium_context, i, len(chunks))
            except Exception as e:
                print(f"  ERROR on chunk {i+1}: {e} — continuing")
                result = {"concepts": [], "poetic_version": "", "mantra": ""}
            all_results.append(result)
            if i < len(chunks) - 1:
                time.sleep(DELAY)

        merged_concepts = merge_concepts(all_results)
        poetics, mantras = merge_poetics(all_results)

        concept_files = []
        concepts_full = []
        for i, c in enumerate(merged_concepts):
            if "error" in c:
                print(f"  Skipping errored concept from chunk extraction.")
                continue
            full = transform_to_concept(c, i, minted_ids)
            if full["human_id"].lower() in {mid.lower() for mid in minted_ids}:
                print(f"  Skipping already-minted: {full['human_id']}")
                continue
            filepath = save_concept_json(full, SOURCE_CONCEPTS_DIR)
            concept_files.append(filepath)
            concepts_full.append(full)

        print(f"\nSaved {len(concept_files)} new concept(s) to source_concepts/")

        output = {
            "source_file": CONVERSATION_FILE.name,
            "model": MODEL,
            "harvester_version": "4.2.0",
            "mycelium_aware": MYCELIUM_AVAILABLE,
            "llm_available": LLM_AVAILABLE,
            "chunk_size": CHUNK_SIZE,
            "total_chunks": len(chunks),
            "concepts": merged_concepts,
            "poetic_versions": poetics,
            "mantras": mantras
        }
        with open(OUTPUT_FILE, "w") as f:
            json.dump(output, f, indent=2)

    else:
        if not LLM_AVAILABLE:
            print("\nLLM unavailable. Switching to manual import mode.")
            print(f"Showing only unminted concepts from {SOURCE_CONCEPTS_DIR}")
        else:
            print(f"\nConversation file not found: {CONVERSATION_FILE}")
            print("Checking source_concepts/ for unminted concept JSONs...")

        concept_files, concepts_full, poetics, mantras = import_from_source_concepts(
            SOURCE_CONCEPTS_DIR, minted_ids
        )

        if not concept_files:
            print("\nNothing new to process. All concepts in source_concepts/ are already minted.")
            print("Options:")
            print("  1. Add new concept JSONs to source_concepts/")
            print(f"  2. Create {CONVERSATION_FILE} for LLM extraction")
            sys.exit(0)

        print(f"\nLoaded {len(concept_files)} unminted concept(s) from source_concepts/.")

    if not concept_files:
        print("No concepts to review. Exiting.")
        sys.exit(0)
        
    print("\n🧹 Running deduplication on extracted concepts...")
    original_count = len(concepts_full)
    concepts_full = deduplicate_concepts(concepts_full)

    if args["auto"]:
        print("\nAUTO-APPROVE: Skipping review, approving all valid concepts.")
        approved = list(range(len(concepts_full)))
    else:
        approved = display_review_menu(concept_files, concepts_full, poetics, mantras)

    if approved is None:
        print("\nQuit. Concepts remain in source_concepts/ for later minting.")
        sys.exit(0)

    if not approved:
        print("\nSkipped minting. Concepts saved. Done.")
        sys.exit(0)

    mint_approved(approved, concepts_full, concept_files, poetics, mantras)

    print("\nDone. The mycelium grows. 🌱")
    
    # map_gen = PROJECT_ROOT / "tools" / "generate_mycelium_map.py"
    # if map_gen.exists():
    #    print("\nRegenerating mycelium map...")
    #    import subprocess
    #    subprocess.run([sys.executable, str(map_gen)], cwd=str(PROJECT_ROOT))
    
    if args["with_relationships"]:
        rel_gen = PROJECT_ROOT / "tools" / "generate_relationships.py"
        if rel_gen.exists():
            print(f"\n{'='*60}")
            print("AUTO-GENERATING RELATIONSHIPS (--with-relationships)")
            print(f"{'='*60}")
            import subprocess
            result = subprocess.run(
                [sys.executable, str(rel_gen), "--incremental", "--write"],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True
            )
            for line in result.stdout.split("\n")[-8:]:
                if line.strip():
                    print(f"  {line.strip()}")
            if result.returncode != 0:
                print(f"  WARNING: Relationship generator exited with code {result.returncode}")
                if result.stderr:
                    print(f"  {result.stderr[:500]}")
        else:
            print(f"  WARNING: {rel_gen} not found — skipping relationship generation")


if __name__ == "__main__":
    main()
