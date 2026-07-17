---
phase: 43
date: 2026-05-25
status: In Progress — Critical path
related: [[Phase-50-CAR-Distribution-Pipeline]], [[Session-020]]
---

# Phase 43: Concept Editing & Reminting

## What Changed

The concept reminting tool (`remint_existing_concepts.py`) was used during the CAR import resolution to rebuild the local index from the blockstore. A manual index rebuild was required after 103 blocks were reminted during CAR import with new CIDs. The remint tool successfully identified 248 clean CIDs, 2 stale CIDs, and 189 missing blocks (ghost index entries).

## Why

Phase 50C revealed that CIDs computed on Paperspace differ from CIDs computed on local machines despite identical bytes. The CAR import pipeline (v1.1.0) now handles this by reminting blocks on import with provenance preservation. However, the index drifts out of sync with the blockstore during this process. The remint tool is essential for rebuilding the index from ground truth — scanning every `.cbor` file on disk and rebuilding the `human_id_to_cid.json` mapping.

## Changes Made

### Index Rebuild

After CAR import reminted 103 blocks under new CIDs, the index contained 439 entries but only 250 had corresponding block files. A manual rebuild scanned all 869 block files, extracted `human_id` from each, and built a fresh index of 687 entries. The old index was backed up to `store/index/backups/`.

### Remint Tool Status

- 248 concepts: CID clean (no change needed)
- 2 concepts: CID stale (re-minted this run)
- 189 concepts: missing block files (ghost entries — index references to blocks that don't exist locally)

## Testing

| Metric | Before Rebuild | After Rebuild |
|--------|---------------|---------------|
| Index entries | 439 | 687 |
| Block files on disk | 869 | 869 |
| Map nodes | 250 | 687 |
| Skipped (ghosts) | 189 | 0 |

## Next Steps

- Automate index rebuild in `import_from_car.py` v1.2.0 so manual intervention is never required
- Resolve the 189 ghost entries (blocks exist on Paperspace but not locally — CAR transport issue)
- Build `remint_concept.py` CLI tool for individual concept editing (original Phase 43 scope)