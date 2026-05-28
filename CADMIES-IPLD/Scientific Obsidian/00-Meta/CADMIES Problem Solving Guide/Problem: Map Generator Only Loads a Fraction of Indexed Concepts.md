Problem: Map Generator Only Loads a Fraction of Indexed Concepts
Date encountered: 2026-05-27 (post-Session-023 work)
Severity: Critical — mycelium map shows 115 nodes instead of 661
Status: Resolved
See also: CAR vs Tarball — When to Use Each for Backup and Transfer

Symptoms
generate_mycelium_map.py reports "Loading 115 concepts from blockstore" when the index has 657+ entries

generate_relationships.py produces very few edges (70-80 instead of 500+)

Relationship generator output references bad-format IDs with colons, uppercase first letters, or slashes (e.g., Epistemology:Concept/PerceptualFramesAsIntelligenceMultipliers, Alchemical Insight)

Block count, index count, and source concept count don't align

Root Cause Chain
Primary trigger: Paperspace project consolidation (Session 023). Three separate Paperspace projects were merged into a single unified structure — CADMIES-Gradient with notebooks for IPLD, Buttercup, and Narrative. During this migration, the blockstore at store/blocks/ was lost or left behind. The index at store/index/human_id_to_cid.json survived (or was restored from backup), but it pointed to CIDs whose .cbor files no longer existed on disk. The consolidation also appears to have reintroduced bad-format IDs (colon-format, uppercase variants) that had been previously cleaned in Session 021 — possibly from an older index snapshot being merged in during the notebook restructuring.

This primary failure cascaded into three layered problems:

CID mismatch between index and blockstore. The live index pointed to CIDs that didn't match any .cbor files on disk. load_concept(cid) looks for store/blocks/{cid}.cbor — if the file doesn't exist, it returns an error and the concept gets skipped. Result: 657 index entries but only 115 successfully loaded by the map and relationship generators.

Bad-format IDs in the index. Entries with colons (Epistemology:Concept/...), uppercase first letters (Alchemical Insight, Conditional-Interdependence), and legacy HOG-era formats resurfaced after the consolidation. These contaminated the concept list that the relationship generator feeds to Mistral, wasting tokens on garbage entries and confusing the edge proposals. Of 700 index entries, 26 were bad-format.

Ghost blocks in the blockstore. After rebuilding from source_concepts/, the blockstore contained .cbor files whose CIDs weren't in the clean index — 180 orphan blocks from previous states. These didn't cause loading failures but cluttered the blockstore and made debugging harder.

Solution (Three-Step Cleanup)
Step 1: Rebuild blockstore from source concepts

The source JSONs in source_concepts/ are the ground truth. When blocks are missing or CIDs don't match, rebuild everything from those JSONs:

bash
cd /notebooks/CADMIES/CADMIES-IPLD && for f in source_concepts/*.json; do python tools/core/cid_generator.py --concept-file "$f"; done
This reads each source JSON, generates a fresh CID from its actual content, writes the .cbor block, and updates the index. Deterministic and reliable. In the Session 023 recovery, this rebuilt 652 concepts into the blockstore.

Step 2: Purge orphan blocks

Compare every .cbor file against the clean index. Delete any block whose CID isn't in the index:

bash
cd /notebooks/CADMIES/CADMIES-IPLD && python3 -c "
import json
from pathlib import Path

with open('store/index/human_id_to_cid.json') as f:
    index = json.load(f)

clean_cids = set(index.values())
blocks_dir = Path('store/blocks')
deleted = 0
kept = 0

for bf in blocks_dir.glob('*.cbor'):
    cid = bf.stem
    if cid not in clean_cids:
        bf.unlink()
        deleted += 1
    else:
        kept += 1

print(f'Blocks kept: {kept}')
print(f'Blocks deleted (orphans/bad format): {deleted}')
"
This removed 180 orphan blocks and left 661 clean ones matching the index.

Step 3: Remove bad-format entries from the index itself

Deleting orphan blocks doesn't clean the index. Entries with colons, uppercase first letters, or legacy formats must be removed from the index directly:

bash
cd /notebooks/CADMIES/CADMIES-IPLD && python3 -c "
import json

with open('store/index/human_id_to_cid.json') as f:
    index = json.load(f)

bad_patterns = []
clean = {}
removed = 0

for hid, cid in index.items():
    if ':' in hid or hid[0].isupper():
        removed += 1
        bad_patterns.append(hid)
    else:
        clean[hid] = cid

with open('store/index/human_id_to_cid.json', 'w') as f:
    json.dump(clean, f, indent=2)

print(f'Index entries before: {len(index)}')
print(f'Index entries after: {len(clean)}')
print(f'Removed: {removed}')
for bp in bad_patterns[:10]:
    print(f'  {bp}')
"
This removed 26 bad-format entries (colon variants, uppercase IDs, HOG-era ghosts) leaving 674 clean lowercase_snake_case entries.

Verification
After all three steps, confirm alignment between the three data stores:

bash
python3 -c "import json; data=json.load(open('store/index/human_id_to_cid.json')); print(f'Index entries: {len(data)}')" && echo "---" && ls store/blocks/*.cbor 2>/dev/null | wc -l && echo "---" && ls source_concepts/*.json 2>/dev/null | wc -l
All three numbers should be in the same ballpark. Then run the map generator to confirm it loads the full count:

bash
python tools/generate_mycelium_map.py
Expected output: "Loading 661 concepts from blockstore" with 661 nodes in the generated map.

Prevention
CAR export after every major harvest. Creates a portable snapshot of the entire blockstore + index that can be imported on any machine.

bash
python tools/export_to_car.py --all --output /notebooks/cadmies_sessionXXX.car
Backup the index before any bulk operation. The index backup directory at store/index/backups/ is automatic with some tools, but a manual copy before mass deletes or rebuilds is cheap insurance.

Tarball the full project before infrastructure changes. Before consolidating notebooks, moving directories, or restructuring projects, create a tarball:

bash
cd /notebooks/CADMIES/CADMIES-IPLD
tar -czf /notebooks/cadmies_pre_migration.tar.gz store/blocks store/index source_concepts/
Enforce lowercase_snake_case at harvest time. The harvester v4.2.0+ already does this, but older concepts imported from external sources may still have bad formats. Run the audit periodically.

Known Clean Backup
store/index/backups/human_id_to_cid.json.backup.20260527_234848 — 661 clean entries, no uppercase variants, no colon-format IDs. This is the gold-standard index snapshot from the Terminator harvest.

Related Sessions
Session 021 — Original duplicate merge and lowercase enforcement (4 case-variant duplicates merged)

Session 022 — Mega-Harvest and Rebentisch cross-pollination (461 nodes, 572 edges)

Session 023 — Terminator harvest (654 nodes), Paperspace project consolidation, blockstore loss and recovery