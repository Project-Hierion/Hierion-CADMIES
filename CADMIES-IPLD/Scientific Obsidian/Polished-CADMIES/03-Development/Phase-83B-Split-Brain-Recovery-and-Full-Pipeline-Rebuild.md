---
phase: 83B
date: 2026-10-20
status: Complete
related: "[[Phase-83A-Blockstore-Rebuild-From-Spores]], [[Phase-57-Index-Integrity-and-Disaster-Recovery]], [[Session-063-2026-10-19-Mycelium-Regrown-From-Spores]]"
---

# Phase 83B: Split-Brain Recovery and Full Pipeline Rebuild

## What Changed

The interrupted Oct 19 rebuild was discovered to be in a split-brain state: the
blockstore index had been reverted by the prior session's `git reset --hard`,
leaving it pointing at old CIDs while 2,144 block files (old and new) sat on
disk. Diagnosis: 659 index entries, but only 234 had matching blocks — 425
pointed at nonexistent files. The full pipeline was re-run from source_concepts:
index emptied, 650 concepts re-minted with fresh CIDs, 574 edges generated,
map and gateway regenerated at full size.

## Why

The Phase 83A handoff flagged one open question: did the reset revert
`human_id_to_cid.json`? Verification showed the damage was worse than feared —
the index was a stale snapshot whose CIDs mismatched the actual block files.
Attempts to patch around it (incremental relationship pass, reminter) were
rejected because every downstream tool reads the index, not the raw blocks.
Following Phase 57 precedent (source_concepts is ground truth), the store was
rebuilt cleanly from spores rather than forensically repaired.

## Changes Made

### Diagnosis

- Relationship generator reported "Loaded 234 concepts" vs blockstore's 659 —
  first signal of index/block divergence
- Integrity scan confirmed: 659 index entries, 425 missing blocks, 0 missing
  extensions — stale CIDs, not filename drift
- Harvester manual-mode check showed 651 concepts "already minted" — proving
  the index was a full-but-wrong snapshot, not a partial one

### Rebuild

- Stale index backed up to `human_id_to_cid.json.stale-backup`, then emptied
- Broken `tools/harvest/conversation.json` (contained merge conflict markers;
  5 months old) deleted to force manual import mode
- Harvester run in `--auto` manual mode: 650 concepts validated and minted,
  0 failures (659 sources minus known duplicates)
- Post-mint integrity check: 650 index entries, 0 missing blocks

### Relationship Generation

- Full (non-incremental) codestral:22b run: 574 edges across 392 concepts
- Map generated: 650 nodes, 686 edges, 0 skipped (263 orphan edges filtered)
- Gateway regenerated: index.html, concepts.json (~700KB), sitemap.xml

### Deployment

- All outputs committed and pushed (commits e858f8c, 2a94215)
- Recovery tarball `cadmies_rebuild_2026-10-20b.tar.gz` (3.5 MB) force-added
  and pushed to GitHub

## Testing

- Index/block reconciliation: 650/650, zero missing
- Map and gateway both report full 650-concept coverage
- Validation passed on all 650 mints (Scientific Validator v1.1.0, BASIC)

## Results

| Metric | Value |
|--------|-------|
| Concepts indexed | 650 |
| Blocks missing | 0 |
| Edges written | 574 |
| Map nodes / edges | 650 / 686 |
| Recovery tarball in git | Yes (2a94215) |

## Known Issues (Deferred)

- Blockstore holds ~1,900 orphan block files from old mints alongside the
  current 650 — harmless but bloated; candidate for a store-wide orphan-block
  sweep
- Harvester has no clean way to force manual import mode (mode is hardcoded
  to conversation.json existence); contributed to diagnostic confusion
- `--conv=` flag is parsed but never used in the mode check (script bug)
- No dedicated bulk-mint tool exists; the Phase 83A/83B rebuilds relied on
  the harvester's manual mode after emptying the index
- DOMAIN_UPWARD_MAP still missing ~90 domains (default color fallback)

## Conclusion

The split-brain was healed by trusting spores over surgery. Two full rebuilds
in two days confirms the source-concepts-as-ground-truth doctrine works — but
also that the pipeline needs guardrails: an index-vs-blocks consistency check
should run before any relationship or remint pass, and manual-import mode needs
a real flag.
