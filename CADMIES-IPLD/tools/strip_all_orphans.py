#!/usr/bin/env python3
"""
File: strip_all_orphans.py
Tool: CADMIES Orphan Edge Stripper
Version: 1.0.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Strip all edges pointing to non-existent targets.
         Creates a backup tarball of blocks/ before modifying anything.

Usage:
    python tools/strip_all_orphans.py           # dry run
    python tools/strip_all_orphans.py --apply   # strip with backup
"""

import json, sys, subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import dag_cbor

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR, STORE_DIR

BACKUP_DIR = PROJECT_ROOT / "store" / "index" / "backups"
apply = "--apply" in sys.argv

print(f"=== Strip All Orphan Edges {'— APPLY' if apply else '— DRY RUN'} ===\n")

all_cids = load_all_concept_cids()
node_ids = set()
source_cid_map = {}
for cid in all_cids:
    concept = load_concept(cid)
    if 'error' not in concept:
        hid = concept.get('human_id', '')
        node_ids.add(hid)
        source_cid_map[hid] = cid

blockstore_edges = []
for cid in all_cids:
    concept = load_concept(cid)
    if 'error' in concept: continue
    hid = concept.get('human_id', '')
    rels = concept.get('relationships', {})
    for rel_type in ['builds_upon', 'related_to', 'specializes', 'contradicts']:
        for target in rels.get(rel_type, []):
            if isinstance(target, str):
                blockstore_edges.append({'source': hid, 'target': target, 'type': rel_type})

orphans = [e for e in blockstore_edges if e['target'] not in node_ids]
print(f'Orphan edges found: {len(orphans)}')

unique_targets = set(e['target'] for e in orphans)
print(f'Unique missing targets: {len(unique_targets)}')
print('Sample targets:')
for t in sorted(unique_targets)[:10]:
    count = sum(1 for e in orphans if e['target'] == t)
    print(f'  {t} ({count} edges)')

if not apply:
    print(f'\nDry run. Add --apply to strip with backup.')
    sys.exit(0)

timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
backup_name = f'blocks_pre_orphan_strip_{timestamp}.tar.gz'
backup_path = BACKUP_DIR / backup_name
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

print(f'\nCreating backup: {backup_name}')
subprocess.run([
    'tar', '-czf', str(backup_path),
    '-C', str(PROJECT_ROOT), 'store/blocks'
], check=True)
print(f'Backup saved: {backup_path}')

by_source = defaultdict(list)
for e in orphans:
    by_source[e['source']].append(e)

stripped_edges = 0
stripped_concepts = 0
for hid, edges in by_source.items():
    cid = source_cid_map.get(hid)
    if not cid: continue
    concept = load_concept(cid)
    if 'error' in concept: continue
    rels = concept.get('relationships', {})
    modified = False
    for e in edges:
        t = e['type']
        target = e['target']
        if t in rels and target in rels[t]:
            rels[t].remove(target)
            if not rels[t]:
                del rels[t]
            stripped_edges += 1
            modified = True
    if modified:
        concept['relationships'] = rels
        path = BLOCKS_DIR / f'{cid}.cbor'
        if not path.exists():
            path = BLOCKS_DIR / cid
        with open(path, 'wb') as f:
            f.write(dag_cbor.encode(concept))
        stripped_concepts += 1

print(f'\nStripped {stripped_edges} orphan edges from {stripped_concepts} concepts.')
print(f'Undo: tar -xzf {backup_path} -C {PROJECT_ROOT}')
print('\nRun generate_mycelium_map.py to verify.')
