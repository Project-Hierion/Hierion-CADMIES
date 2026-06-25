#!/usr/bin/env python3
"""
File: phase1_extract.py
Tool: CADMIES Relationship Generator — Phase 1
Version: 1.0.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Send concept batches to Mistral, save raw responses.
         No JSON parsing — just collect whatever Mistral returns.

Usage:
    python tools/phase1_extract.py
"""

import json, sys, time
from pathlib import Path
from collections import defaultdict

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

MODEL = "mistral:7b"
DELAY = 1
BATCH_SIZE = 15
RAW_DIR = PROJECT_ROOT / "raw_extractions"

def gather_ids():
    all_cids = load_all_concept_cids()
    ids = []
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' not in concept:
            ids.append(concept.get('human_id', ''))
    return sorted(ids)

def build_prompt(batch_ids):
    ids_only = "\n".join(batch_ids)
    return f"""Propose relationships between these concept IDs.

{ids_only}

For each concept ID above, list related concepts using one of these types:
builds_upon, related_to, specializes, contradicts

Format your response like this:
concept_id → [type] target_id

Example:
entropy → [builds_upon] thermodynamics
entropy → [related_to] arrow_of_time
thermodynamics → [specializes] statistical_mechanics"""

def call_mistral(prompt, step_name):
    import ollama
    print(f"  Mistral ← {len(prompt.split())} tokens...", end=" ", flush=True)
    try:
        response = ollama.generate(model=MODEL, prompt=prompt, options={"num_predict": 1024, "temperature": 0.1})
        raw = response["response"].strip()
        print(f"→ {len(raw)} chars")
        return raw
    except Exception as e:
        print(f"ERROR: {e}")
        return ""

def main():
    RAW_DIR.mkdir(exist_ok=True)
    all_ids = gather_ids()
    print(f"Loaded {len(all_ids)} concepts")
    
    batches = [all_ids[i:i+BATCH_SIZE] for i in range(0, len(all_ids), BATCH_SIZE)]
    print(f"Phase 1: {len(batches)} batches\n")
    
    for i, batch in enumerate(batches):
        print(f"Batch {i+1}/{len(batches)} ({len(batch)} concepts)")
        prompt = build_prompt(batch)
        raw = call_mistral(prompt, f"batch{i+1}")
        
        out_path = RAW_DIR / f"batch_{i+1:02d}.txt"
        with open(out_path, 'w') as f:
            f.write(raw)
        print(f"  Saved: {out_path}")
        sys.stdout.flush()
        if i < len(batches) - 1:
            time.sleep(DELAY)
    
    print(f"\nDone. {len(batches)} files saved to {RAW_DIR}")

if __name__ == "__main__":
    main()
