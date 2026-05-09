#!/usr/bin/env python3
"""
File: harvest_full_pipeline.py
CLI: CADMIES Conversation Harvester (Full Pipeline)
Version: 4.0.0
System: CADMIES-IPLD / harvest
Status: ACTIVE — TESTING on phase19-harvest-pipeline-v4
Dependencies: ollama, llm_mycelium_reader, cid_generator, scientific_validator,
              provenance_manager, paths

Purpose: End-to-end conversation harvesting pipeline. Chunks a conversation,
         queries the mycelium for context, extracts concepts + poetics + mantras
         via Mistral (if available), saves to source_concepts/, presents
         interactive review, validates, and mints approved concepts directly
         into the IPLD blockstore.

         LLM-optional: If Mistral is unavailable, skips extraction and allows
         manual import from source_concepts/ for review + minting. Only
         unminted concepts (not in blockstore index) are shown.

         Born from a washing machine. Powered by the Kerr Spacetime Gearbox.

Version History:
  1.0.0 — Initial extraction pipeline (extract_concepts.py)
  2.0.0 — Mycelium-aware extraction via Willie's search
  3.0.0 — Poetic version and mantra extraction
  4.0.0 — Full pipeline: extract → review → validate → mint, LLM-optional mode
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# === PATH SETUP ===
HARVEST_DIR = Path(__file__).parent
PROJECT_ROOT = HARVEST_DIR.parent

# === CONFIG ===
CONVERSATION_FILE = HARVEST_DIR / "conversation.json"
OUTPUT_FILE = HARVEST_DIR / "harvested_concepts.json"
SOURCE_CONCEPTS_DIR = PROJECT_ROOT / "source_concepts"
MODEL = "mistral:7b"
CHUNK_SIZE = 500
DELAY = 2
RELEVANCE_THRESHOLD = 0.1
DEFAULT_CERTAINTY = 0.8
VALIDATION_LEVEL = "BASIC"  # Was "STANDARD" — proofs not required for harvested concepts

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
    from llm_mycelium_reader import search_mycelium, load_all_concept_cids, load_concept
    MYCELIUM_AVAILABLE = True
except ImportError:
    MYCELIUM_AVAILABLE = False
    print("WARNING: Mycelium search unavailable — proceeding without context.")

# === CID GENERATOR ===
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))
from cid_generator import CIDGenerator_v1_1_0 as CIDGenerator
from scientific_validator import ScientificValidator_v1_0_0 as ScientificValidator
from provenance_manager import ProvenanceManager

# === EXTRACTION PROMPT ===
EXTRACTION_PROMPT = """You are a philosophical concept extractor for the CADMIES knowledge system.

IMPORTANT: Extract only 1-3 broad, high-level concepts. Do NOT break insights into small granular pieces. Prefer unified, philosophical concepts over micro-observations. Quality over quantity.

Extract NEW concepts, a poetic version, and a mantra from this conversation.

Existing concepts (DO NOT extract these — reference only):
{mycelium_context}

Return a single JSON object with EXACTLY this structure. Concepts MUST be objects with all fields shown — NOT strings, NOT topic names:

{{
  "concepts": [
    {{
      "name": "snake_case_concept_name",
      "definition": "Clear 1-3 sentence definition of the concept.",
      "domain": "Physics",
      "insight": "The novel or noteworthy observation from the conversation.",
      "builds_upon": [],
      "related_to": [],
      "contradicts": []
    }}
  ],
  "poetic_version": "A multi-line verse capturing the soul and wonder of the insight.",
  "mantra": "A short repeatable phrase that encapsulates the core realization."
}}

Return ONLY the JSON object. No markdown fences. No introductory text. No commentary. JUST the JSON.

CONVERSATION:
{chunk}"""


# ============================================================================
# STEP 1: LOAD CONVERSATION
# ============================================================================

def load_conversation_robust(filepath):
    """Load conversation text from JSON, handling unescaped newlines."""
    with open(filepath, "r") as f:
        raw_text = f.read().strip()

    # Try standard JSON first
    try:
        data = json.loads(raw_text)
        return data.get("content", raw_text)
    except json.JSONDecodeError:
        pass

    # Robust: find "content": and extract everything until the final closing brace
    content_key = '"content":'
    key_pos = raw_text.find(content_key)
    if key_pos == -1:
        raise ValueError("Could not find 'content' key in JSON file")

    # Start after the key
    value_start = key_pos + len(content_key)
    raw_value = raw_text[value_start:].strip()

    # The content is everything until the LAST closing brace
    last_brace = raw_value.rfind('}')
    if last_brace != -1:
        raw_value = raw_value[:last_brace].strip()

    # Strip wrapping quotes if present
    if raw_value.startswith('"') and raw_value.endswith('"'):
        raw_value = raw_value[1:-1]

    print("  (used robust loader)")
    return raw_value


# ============================================================================
# STEP 2: MYCELIUM CONTEXT
# ============================================================================

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


# ============================================================================
# STEP 3: CHUNK
# ============================================================================

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of roughly chunk_size words."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


# ============================================================================
# STEP 4: EXTRACT (LLM)
# ============================================================================

def extract_from_chunk(chunk, mycelium_context, index, total):
    """Send chunk to Mistral, parse response."""
    prompt = EXTRACTION_PROMPT.format(mycelium_context=mycelium_context, chunk=chunk)
    print(f"\n  Chunk {index+1}/{total} ({len(chunk.split())} words)...")

    try:
        response = ollama.generate(model=MODEL, prompt=prompt)
        raw = response["response"].strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:]) if lines[0].startswith("```") else raw
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        result = json.loads(raw, strict=False)
        concepts = result.get("concepts", [])
        poetic = result.get("poetic_version", "")
        mantra = result.get("mantra", "")
        print(f"  -> {len(concepts)} concept(s), poetics: {'yes' if poetic else 'no'}, mantra: {'yes' if mantra else 'no'}")
        return {"concepts": concepts, "poetic_version": poetic, "mantra": mantra}

    except json.JSONDecodeError:
        # Save raw output for debugging
        dump_path = HARVEST_DIR / f"raw_failed_chunk_{index+1}.txt"
        with open(dump_path, "w") as f:
            f.write(raw)
        print(f"  WARNING: JSON parse failed. Raw output saved to {dump_path}")
        return {"concepts": [{"error": "json_parse_failed", "raw_output": raw}], "poetic_version": "", "mantra": ""}
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"concepts": [], "poetic_version": "", "mantra": ""}


# ============================================================================
# STEP 4b: MANUAL IMPORT (No LLM)
# ============================================================================

def import_from_source_concepts(source_dir, minted_ids=None):
    """Load unminted concept JSONs from source_concepts/ for review/minting."""
    if minted_ids is None:
        minted_ids = set()

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
            if human_id in minted_ids:
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


# ============================================================================
# STEP 5: TRANSFORM
# ============================================================================

def transform_to_concept(extracted, chunk_index):
    """Transform Mistral output to UniversalScientificConcept schema."""
    name = extracted.get("name", "unnamed_concept")
    title = name.replace("_", " ").title()
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    return {
        "schema_version": "1.0.0",
        "human_id": name,
        "title": title,
        "definition": extracted.get("definition", ""),
        "type": "Concept",
        "domain": extracted.get("domain", "Unknown"),
        "subdomain": "",
        "proofs": [
    {
        "type": "conversation_extraction",
        "description": f"Extracted from conversation via {MODEL}",
        "confidence": DEFAULT_CERTAINTY,
        "date": now,
        "reference": f"CADMIES Harvest Pipeline v4.0 — {CONVERSATION_FILE.name}"
    }
],
        "metadata": {
            "created": now,
            "creator": "CADMIES Harvest Pipeline v4.0",
            "certainty_score": DEFAULT_CERTAINTY,
            "version": 1,
            "license": "CC BY-SA 4.0",
            "purpose": "educational",
            "supersedes": None,
            "superseded_by": None
        },
        "relationships": {
            "builds_upon": extracted.get("builds_upon", []) or [],
            "contradicts": extracted.get("contradicts", []) or [],
            "related_to": extracted.get("related_to", []) or [],
            "specializes": []
        },
        "difficulty_levels": {
            "beginner": extracted.get("definition", ""),
            "intermediate": extracted.get("definition", ""),
            "expert": extracted.get("insight", "")
        },
        "learning_path": {
            "prerequisites": extracted.get("builds_upon", []) or [],
            "next_steps": []
        },
        "cross_references": {},
        "extra_fields": {
            "insight": extracted.get("insight", ""),
            "source_chunk": chunk_index + 1,
            "origin_file": CONVERSATION_FILE.name,
            "harvester_version": "4.0.0"
        }
    }


# ============================================================================
# STEP 6: SAVE
# ============================================================================

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


# ============================================================================
# STEP 7: MERGE
# ============================================================================

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


# ============================================================================
# STEP 8: REVIEW MENU
# ============================================================================

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


# ============================================================================
# STEP 9: VALIDATE
# ============================================================================

def validate_concept(concept):
    """Run scientific validator."""
    validator = ScientificValidator(VALIDATION_LEVEL)
    is_valid, errors, report = validator.validate(concept)
    if not is_valid:
        print(f"  VALIDATION FAILED: {concept.get('human_id', 'unknown')}")
        for e in errors:
            print(f"    - {e}")
    return is_valid, errors


# ============================================================================
# STEPS 10–11: MINT
# ============================================================================

def mint_concept(concept, cid_gen, pm):
    """Generate CID, save to blockstore, create provenance. Return result dict."""
    human_id = concept.get("human_id", "unknown")

    # Validate
    is_valid, errors = validate_concept(concept)
    if not is_valid:
        return {"success": False, "human_id": human_id, "error": "validation_failed", "details": errors}

    # Generate CID
    cid_result = cid_gen.generate_cid(concept)
    if not cid_result["success"]:
        return {"success": False, "human_id": human_id, "error": "cid_generation_failed", "details": cid_result.get("errors", [])}

    # Save to blockstore
    save_result = cid_gen.save_to_blockstore(cid_result, concept)
    if not save_result["success"]:
        return {"success": False, "human_id": human_id, "error": "blockstore_save_failed", "details": save_result.get("errors", [])}

    # Create provenance
    try:
        pm.create_provenance_record(
            concept_cid=cid_result["cid"],
            author="CADMIES Harvest Pipeline v4.0",
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
        # Inject poetics/mantras if available
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

    # Summary
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    print(f"\n{'='*60}")
    print(f"MINTING COMPLETE: {len(successes)} successful, {len(failures)} failed")
    if successes:
        print("  These concepts are now live in the mycelium and queryable via Willie/Dashboard.")
    print(f"{'='*60}")

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("CADMIES HARVEST FULL PIPELINE v4.0")
    print(f"Model: {MODEL}  |  Chunk Size: {CHUNK_SIZE} words")
    print(f"Branch: phase19-harvest-pipeline-v4 (TESTING)")
    print(f"LLM: {'AVAILABLE' if LLM_AVAILABLE else 'UNAVAILABLE — manual mode'}")
    print(f"Mycelium: {'ENABLED' if MYCELIUM_AVAILABLE else 'DISABLED'}")
    print("=" * 60)
    print("\a")  # Terminal bell — harvest complete

    # Load minted index for filtering
    minted_ids = set()
    index_path = PROJECT_ROOT / "store" / "index" / "human_id_to_cid.json"
    if index_path.exists():
        try:
            with open(index_path, "r") as f:
                minted_ids = set(json.load(f).keys())
        except Exception:
            pass

    # === LLM PATH ===
    if LLM_AVAILABLE and CONVERSATION_FILE.exists():
        # Step 1: Load
        text = load_conversation_robust(CONVERSATION_FILE)
        print(f"\nLoaded: {len(text.split())} words from {CONVERSATION_FILE.name}")

        # Step 2: Mycelium context
        mycelium_context = get_mycelium_context(text)

        # Step 3: Chunk
        chunks = chunk_text(text)
        print(f"\nSplit into {len(chunks)} chunk(s)")

        # Step 4: Extract
        all_results = []
        for i, chunk in enumerate(chunks):
            result = extract_from_chunk(chunk, mycelium_context, i, len(chunks))
            all_results.append(result)
            if i < len(chunks) - 1:
                time.sleep(DELAY)

        # Step 5 & 6: Transform & Save
        merged_concepts = merge_concepts(all_results)
        poetics, mantras = merge_poetics(all_results)

        concept_files = []
        concepts_full = []
        for i, c in enumerate(merged_concepts):
            if "error" in c:
                print(f"  Skipping errored concept from chunk extraction.")
                continue
            full = transform_to_concept(c, i)
            # Skip if already minted
            if full["human_id"] in minted_ids:
                print(f"  Skipping already-minted: {full['human_id']}")
                continue
            filepath = save_concept_json(full, SOURCE_CONCEPTS_DIR)
            concept_files.append(filepath)
            concepts_full.append(full)

        print(f"\nSaved {len(concept_files)} new concept(s) to source_concepts/")

        # Save aggregate log
        output = {
            "source_file": CONVERSATION_FILE.name,
            "model": MODEL,
            "harvester_version": "4.0.0",
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

    # === NO-LLM PATH ===
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

    # === REVIEW & MINT (shared path) ===
    if not concept_files:
        print("No concepts to review. Exiting.")
        sys.exit(0)

    # Step 7: Review
    approved = display_review_menu(concept_files, concepts_full, poetics, mantras)

    if approved is None:
        print("\nQuit. Concepts remain in source_concepts/ for later minting.")
        sys.exit(0)

    if not approved:
        print("\nSkipped minting. Concepts saved. Done.")
        sys.exit(0)

    # Steps 8–11: Mint
    mint_approved(approved, concepts_full, concept_files, poetics, mantras)

    print("\nDone. The mycelium grows. 🌱")


if __name__ == "__main__":
    main()