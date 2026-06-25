#!/usr/bin/env python3
"""
File: enrich_concepts.py
Tool: CADMIES Concept Enrichment Pipeline
Version: 1.0.1
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Enriches existing minted concepts with missing or weak fields.
         Detects gaps (missing type, subdomain, discoverer, identical difficulty
         levels, empty extra_fields), sends the concept to an LLM for enrichment,
         validates the result, and remints with a new CID superseding the old one.

Usage:
    python tools/enrich_concepts.py                     # Enrich all concepts with gaps
    python tools/enrich_concepts.py --concept=entropy   # Enrich single concept
    python tools/enrich_concepts.py --model=codestral   # Use Codestral for deeper enrichment
    python tools/enrich_concepts.py --dry-run           # Preview without reminting

Version History:
  v1.0.1: Fixed supersedes chain and version increment bugs.
  v1.0.0: Initial enrichment pipeline — detect gaps, enrich, validate, remint.
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).parent
PROJECT_ROOT = TOOLS_DIR.parent
SOURCE_CONCEPTS_DIR = PROJECT_ROOT / "source_concepts"
STORE_DIR = PROJECT_ROOT / "store"

# === CONFIG ===
MODEL = "mistral:7b"
DELAY = 5
DEFAULT_CERTAINTY = 0.8

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
        print(f"WARNING: Model '{MODEL}' not found.")
        print(f"  Available models: {available_models}")
        LLM_AVAILABLE = False
except Exception as e:
    print(f"WARNING: Ollama unavailable ({e}).")
    LLM_AVAILABLE = False

# === CID GENERATOR & VALIDATOR ===
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))
from cid_generator import CIDGenerator
from scientific_validator import ScientificValidator
from provenance_manager import ProvenanceManager

# === ENRICHMENT PROMPT ===
ENRICHMENT_PROMPT = """You are a concept enrichment system for the CADMIES knowledge graph. You will receive an existing concept as JSON. Your job is to enrich specific fields that are missing or weak, and return the enriched fields in valid JSON.

RULES:
- If a field is already well-populated and accurate, return it EXACTLY as-is. Do not change good data.
- Do NOT hallucinate references. For key_references, only include works you are highly confident exist. If uncertain, leave the array empty or include only the most well-known reference.
- For type, use a specific type (e.g., "PhilosophicalConcept", "MathematicalTheorem", "ScientificTheory", "EthicalPrinciple", "MetaphysicalFramework") — NOT the generic "Concept".
- For difficulty_levels, provide three DISTINCT explanations: beginner (ELI5, simple metaphor, no jargon), intermediate (proper terminology, connects to related ideas), expert (full depth, philosophical implications, edge cases).
- For discoverer and discovery_year, use "Unknown" and null if the concept emerged from a conversation rather than a historical discovery.
- For applications, list 2-5 real-world or intellectual applications.
- For limitations, note 1-3 known boundaries or critiques of the concept.
- For historical_context, provide 1-3 sentences about how this concept fits into intellectual history or what tradition it emerges from.

Return ONLY a JSON object with these enriched fields. No markdown fences. No commentary. JUST the JSON.

EXISTING CONCEPT:
{concept_json}

Return this exact structure:
{{
  "type": "SpecificTypeHere",
  "subdomain": "SubdomainHere",
  "difficulty_levels": {{
    "beginner": "Simple explanation with metaphor...",
    "intermediate": "Proper terminology explanation...",
    "expert": "Full depth philosophical implications..."
  }},
  "discoverer": "Name or Unknown",
  "discovery_year": null,
  "historical_context": "Brief history...",
  "limitations": "Known limitations...",
  "applications": ["Application 1", "Application 2"],
  "key_references": []
}}"""


def detect_gaps(concept):
    """Analyze a concept and return list of fields that need enrichment."""
    gaps = []

    if concept.get("type", "Concept") == "Concept":
        gaps.append("type")

    if not concept.get("subdomain", ""):
        gaps.append("subdomain")

    diff = concept.get("difficulty_levels", {})
    beginner = diff.get("beginner", "")
    intermediate = diff.get("intermediate", "")
    expert = diff.get("expert", "")
    if beginner == intermediate or not beginner or not intermediate:
        gaps.append("difficulty_levels")
    if not expert:
        gaps.append("difficulty_levels")

    extra = concept.get("extra_fields", {})
    if not extra.get("discoverer"):
        gaps.append("discoverer")
    if "discovery_year" not in extra:
        gaps.append("discovery_year")
    if not extra.get("historical_context"):
        gaps.append("historical_context")
    if not extra.get("limitations"):
        gaps.append("limitations")
    if not extra.get("applications"):
        gaps.append("applications")
    if "key_references" not in extra:
        gaps.append("key_references")

    return gaps


def enrich_concept(concept, model=MODEL):
    """Send a concept to the LLM for enrichment. Returns enriched fields dict."""
    human_id = concept.get("human_id", "unknown")
    gaps = detect_gaps(concept)
    
    if not gaps:
        print(f"  ✅ {human_id}: No gaps detected. Skipping.")
        return None
    
    print(f"  🔍 {human_id}: Gaps detected — {', '.join(gaps)}")
    
    concept_json = json.dumps(concept, indent=2)
    prompt = ENRICHMENT_PROMPT.format(concept_json=concept_json)
    
    try:
        response = ollama.generate(model=model, prompt=prompt)
        raw = response["response"].strip()
        
        while raw.startswith("```"):
            raw = raw.lstrip("`")
            if "\n" in raw:
                raw = raw.split("\n", 1)[1]
        while raw.endswith("```"):
            raw = raw.rstrip("`")
        raw = raw.strip()
        
        enriched = json.loads(raw)
        print(f"  ✅ {human_id}: Enrichment successful")
        return enriched
        
    except json.JSONDecodeError:
        print(f"  ❌ {human_id}: JSON parse failed on enrichment response")
        dump_path = TOOLS_DIR / f"enrich_failed_{human_id}.txt"
        with open(dump_path, "w") as f:
            f.write(raw)
        print(f"     Raw output saved to {dump_path}")
        return None
    except Exception as e:
        print(f"  ❌ {human_id}: {e}")
        return None


def merge_enrichment(concept, enriched):
    """Merge enriched fields into concept, overwriting only missing/weak fields."""
    merged = json.loads(json.dumps(concept))
    
    if enriched.get("type") and concept.get("type", "Concept") == "Concept":
        merged["type"] = enriched["type"]
    if enriched.get("subdomain") and not concept.get("subdomain", ""):
        merged["subdomain"] = enriched["subdomain"]
    
    current_diff = concept.get("difficulty_levels", {})
    enriched_diff = enriched.get("difficulty_levels", {})
    if enriched_diff:
        beginner_current = current_diff.get("beginner", "")
        intermediate_current = current_diff.get("intermediate", "")
        if beginner_current == intermediate_current or not beginner_current:
            merged["difficulty_levels"]["beginner"] = enriched_diff.get("beginner", beginner_current)
            merged["difficulty_levels"]["intermediate"] = enriched_diff.get("intermediate", intermediate_current)
        if enriched_diff.get("expert") and not current_diff.get("expert"):
            merged["difficulty_levels"]["expert"] = enriched_diff["expert"]
    
    if "extra_fields" not in merged:
        merged["extra_fields"] = {}
    
    extra = concept.get("extra_fields", {})
    for field in ["discoverer", "historical_context", "limitations"]:
        if enriched.get(field) and not extra.get(field):
            merged["extra_fields"][field] = enriched[field]
    
    if enriched.get("discovery_year") is not None and "discovery_year" not in extra:
        merged["extra_fields"]["discovery_year"] = enriched["discovery_year"]
    
    if enriched.get("applications") and not extra.get("applications"):
        merged["extra_fields"]["applications"] = enriched["applications"]
    
    if enriched.get("key_references") is not None and "key_references" not in extra:
        merged["extra_fields"]["key_references"] = enriched["key_references"]
    
    for key, value in extra.items():
        if key not in merged["extra_fields"]:
            merged["extra_fields"][key] = value
    
    return merged


def validate_and_remint(concept, dry_run=False):
    """Validate enriched concept and remint to blockstore. Returns result dict."""
    human_id = concept.get("human_id", "unknown")
    
    validator = ScientificValidator("BASIC")
    is_valid, errors, report = validator.validate(concept)
    if not is_valid:
        print(f"  ❌ {human_id}: Validation failed after enrichment")
        for e in errors:
            print(f"     - {e}")
        return {"success": False, "human_id": human_id, "error": "validation_failed", "details": errors}
    
    if dry_run:
        print(f"  📝 {human_id}: Dry run — would remint here")
        return {"success": True, "human_id": human_id, "dry_run": True}
    
    old_cid = None
    index_path = STORE_DIR / "index" / "human_id_to_cid.json"
    if index_path.exists():
        with open(index_path, "r") as f:
            index = json.load(f)
        old_cid = index.get(human_id)
    
    current_version = concept.get("metadata", {}).get("version", 1)
    concept["metadata"]["version"] = current_version + 1
    concept["metadata"]["supersedes"] = old_cid
    
    cid_gen = CIDGenerator()
    cid_result = cid_gen.generate_cid(concept)
    if not cid_result["success"]:
        return {"success": False, "human_id": human_id, "error": "cid_failed"}
    
    save_result = cid_gen.save_to_blockstore(cid_result, concept)
    if not save_result["success"]:
        return {"success": False, "human_id": human_id, "error": "blockstore_save_failed"}
    
    if index_path.exists():
        with open(index_path, "r") as f:
            index = json.load(f)
        index[human_id] = cid_result["cid"]
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)
    
    try:
        pm = ProvenanceManager()
        pm.create_provenance_record(
            concept_cid=cid_result["cid"],
            author="CADMIES Enrichment Pipeline",
            record_type="enrichment",
            comment=f"Enriched missing fields via {MODEL}. Version {concept['metadata']['version']}. Supersedes {old_cid}"
        )
    except Exception as e:
        print(f"  ⚠️ {human_id}: Provenance creation failed — {e}")
    
    print(f"  ✅ {human_id}: Reminted — v{concept['metadata']['version']} | CID: {cid_result['cid'][:30]}...")
    if old_cid:
        print(f"     Supersedes: {old_cid[:30]}...")
    
    return {
        "success": True, 
        "human_id": human_id, 
        "cid": cid_result["cid"], 
        "version": concept["metadata"]["version"],
        "supersedes": old_cid
    }


def load_concept_by_human_id(human_id):
    """Load a concept JSON from source_concepts/ by human_id."""
    filepath = SOURCE_CONCEPTS_DIR / f"{human_id}.json"
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return None


def load_all_concepts():
    """Load all concept human_ids from the index."""
    index_path = STORE_DIR / "index" / "human_id_to_cid.json"
    if not index_path.exists():
        print("No index found. Cannot load concepts.")
        return []
    
    with open(index_path, "r") as f:
        index = json.load(f)
    
    return sorted(index.keys())


def parse_args():
    """Parse command-line flags."""
    args = {
        "model": MODEL,
        "dry_run": False,
        "concept": None,
        "all": False,
        "gaps_only": True,
    }
    for arg in sys.argv[1:]:
        if arg.startswith("--model="):
            args["model"] = arg.split("=", 1)[1]
        elif arg == "--dry-run":
            args["dry_run"] = True
        elif arg == "--all":
            args["all"] = True
            args["gaps_only"] = False
        elif arg.startswith("--concept="):
            args["concept"] = arg.split("=", 1)[1]
    return args


def main():
    args = parse_args()
    global MODEL
    MODEL = args["model"]
    
    print("=" * 60)
    print("CADMIES CONCEPT ENRICHMENT PIPELINE v1.0.1")
    print(f"Model: {MODEL}")
    print(f"Dry Run: {args['dry_run']}")
    print(f"Gaps Only: {args['gaps_only']}")
    print(f"LLM: {'AVAILABLE' if LLM_AVAILABLE else 'UNAVAILABLE'}")
    print("=" * 60)
    
    if not LLM_AVAILABLE:
        print("\nLLM unavailable. Cannot enrich concepts.")
        sys.exit(1)
    
    if args["concept"]:
        human_ids = [args["concept"]]
    else:
        human_ids = load_all_concepts()
    
    if not human_ids:
        print("No concepts found.")
        sys.exit(0)
    
    print(f"\nProcessing {len(human_ids)} concept(s)...")
    
    results = []
    for i, human_id in enumerate(human_ids):
        print(f"\n[{i+1}/{len(human_ids)}] {human_id}")
        
        concept = load_concept_by_human_id(human_id)
        if not concept:
            print(f"  ⚠️ Source concept not found: {human_id}.json")
            continue
        
        enriched = enrich_concept(concept, MODEL)
        if enriched is None:
            continue
        
        merged = merge_enrichment(concept, enriched)
        
        filepath = SOURCE_CONCEPTS_DIR / f"{human_id}.json"
        with open(filepath, "w") as f:
            json.dump(merged, f, indent=2)
        print(f"  💾 Saved enriched: {filepath}")
        
        result = validate_and_remint(merged, dry_run=args["dry_run"])
        results.append(result)
        
        if i < len(human_ids) - 1:
            time.sleep(DELAY)
    
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    dry_runs = [r for r in results if r.get("dry_run")]
    
    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"  Enriched: {len(successes)}")
    print(f"  Failed: {len(failures)}")
    if dry_runs:
        print(f"  Dry runs: {len(dry_runs)}")
    print(f"{'='*60}")
    print("Done. The mycelium grows deeper. 🍄")


if __name__ == "__main__":
    main()
