#!/usr/bin/env python3
"""
File: phase3_write.py
Tool: CADMIES Relationship Generator — Phase 3
Version: 1.0.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Write new edges to blockstore CBOR files.
         Merges Phase 2 output into existing concept relationships.

Usage:
    python tools/phase3_write.py
"""

import json, sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR
import dag_cbor

EDGES_FILE = PROJECT_ROOT / "new_edges.json"

with open(EDGES_FILE, 'r') as f:
    new_edges = json.load(f)

all_cids = load_all_concept_cids()
cid_map = {}
for cid in all_cids:
    concept = load_concept(cid)
    if 'error' not in concept:
        cid_map[concept.get('human_id', '')] = cid

updated = 0
total_edges = 0

for source_id, edges in new_edges.items():
    cid = cid_map.get(source_id)
    if not cid:
        print(f"  SKIP: {source_id} not found")
        continue
    
    concept = load_concept(cid)
    if 'error' in concept:
        continue
    
    rels = concept.get('relationships', {})
    for edge in edges:
        t = edge['type']
        target = edge['target']
        if t not in rels:
            rels[t] = []
        if target not in rels[t]:
            rels[t].append(target)
            total_edges += 1
    
    concept['relationships'] = rels
    
    cbor_path = BLOCKS_DIR / f"{cid}.cbor"
    if not cbor_path.exists():
        cbor_path = BLOCKS_DIR / cid
    with open(cbor_path, 'wb') as f:
        f.write(dag_cbor.encode(concept))
    
    updated += 1
    edge_types = {e['type'] for e in edges}
    print(f"  ✅ {source_id}: +{len(edges)} edges ({', '.join(sorted(edge_types))})")

print(f"\n{'='*50}")
print(f"Updated {updated} concepts with {total_edges} new edges.")
print(f"Run generate_mycelium_map.py to see the dense graph!")
