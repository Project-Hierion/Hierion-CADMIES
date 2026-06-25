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

import json, sys, re
from pathlib import Path
from collections import defaultdict

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from llm_mycelium_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

RAW_DIR = PROJECT_ROOT / "raw_extractions"
OUTPUT_FILE = PROJECT_ROOT / "new_edges.json"

TYPE_ALIASES = {
    "relates_to": "related_to", "related_to": "related_to",
    "builds_upon": "builds_upon",
    "specializes": "specializes", "specialized_from": "specializes",
    "specialized": "specializes", "specialized_in": "specializes",
    "contradicts": "contradicts",
}

def build_id_map():
    all_cids = load_all_concept_cids()
    id_map = {}
    human_ids = set()
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        hid = concept.get('human_id', '')
        title = concept.get('title', '')
        human_ids.add(hid)
        id_map[hid] = hid
        id_map[hid.lower()] = hid
        id_map[hid.replace('_', ' ')] = hid
        id_map[hid.replace('_', ' ').lower()] = hid
        id_map[hid.replace('_', '-')] = hid
        id_map[hid.replace('_', '-').lower()] = hid
        if title:
            id_map[title] = hid
            id_map[title.lower()] = hid
            id_map[title.lower().replace(' ', '_')] = hid
    return id_map, human_ids

def load_existing_edges():
    all_cids = load_all_concept_cids()
    existing = set()
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        hid = concept.get('human_id', '')
        rels = concept.get('relationships', {})
        for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
            for target in rels.get(rel_type, []):
                if isinstance(target, str):
                    existing.add((hid, target, rel_type))
    return existing

def parse_line(line):
    """Parse: anything [type] target1, target2"""
    line = line.strip()
    # Find the first [type] bracket
    bracket_match = re.search(r'\[([^\]]+)\]', line)
    if not bracket_match:
        return None, None, []
    
    rel_type = bracket_match.group(1).strip().lower().replace(' ', '_')
    before_bracket = line[:bracket_match.start()].strip()
    after_bracket = line[bracket_match.end():].strip()
    
    # Remove leading numbering like "1. " or "1."
    source = re.sub(r'^[\d]+\.\s*', '', before_bracket).strip().rstrip('→->').strip()
    if not source:
        return None, None, []
    
    # Clean targets: split by comma, strip notes and quotes
    targets = []
    for t in after_bracket.split(','):
        t = re.sub(r'\s*\(.*?\)\s*$', '', t.strip()).strip('"\'')
        if t:
            targets.append(t)
    
    return source, rel_type, targets

def main():
    print("Phase 2: Extracting NEW edges...")
    id_map, human_ids = build_id_map()
    existing_edges = load_existing_edges()
    print(f"  ID map: {len(id_map)} entries")
    print(f"  Existing edges: {len(existing_edges)}")
    
    new_edges = defaultdict(list)
    seen = set()
    stats = {"lines": 0, "new": 0, "exists": 0, "bad_source": 0, "bad_target": 0, "bad_type": 0}
    
    for txt_file in sorted(RAW_DIR.glob("batch_*.txt")):
        with open(txt_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('Here'):
                    continue
                source, rel_type, targets = parse_line(line)
                if not source:
                    continue
                stats["lines"] += 1
                norm_type = TYPE_ALIASES.get(rel_type)
                if not norm_type:
                    stats["bad_type"] += 1
                    continue
                source_hid = id_map.get(source) or id_map.get(source.lower()) or (source if source in human_ids else None)
                if not source_hid or source_hid not in human_ids:
                    stats["bad_source"] += 1
                    continue
                for target in targets:
                    target_hid = id_map.get(target) or id_map.get(target.lower()) or (target if target in human_ids else None)
                    if not target_hid or target_hid not in human_ids:
                        stats["bad_target"] += 1
                        continue
                    if target_hid == source_hid:
                        continue
                    edge_key = (source_hid, target_hid, norm_type)
                    if edge_key in existing_edges:
                        stats["exists"] += 1
                        continue
                    if edge_key in seen:
                        continue
                    seen.add(edge_key)
                    new_edges[source_hid].append({"target": target_hid, "type": norm_type})
                    stats["new"] += 1
    
    output = {}
    for source, edges in new_edges.items():
        output[source] = edges
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Lines parsed: {stats['lines']}")
    print(f"NEW edges: {stats['new']}")
    print(f"Already exist: {stats['exists']}")
    print(f"Bad source: {stats['bad_source']}  Bad target: {stats['bad_target']}  Bad type: {stats['bad_type']}")
    print(f"Concepts with new edges: {len(output)}")
    print(f"Saved: {OUTPUT_FILE}")
    
    if stats['new'] > 0:
        print(f"\nSample:")
        for source in sorted(output)[:10]:
            for edge in output[source][:2]:
                print(f"  {source} → [{edge['type']}] {edge['target']}")

if __name__ == "__main__":
    main()
