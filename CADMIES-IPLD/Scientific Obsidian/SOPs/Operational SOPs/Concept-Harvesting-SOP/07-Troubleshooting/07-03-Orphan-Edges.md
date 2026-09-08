---
sop: Concept-Harvesting-SOP
section: Troubleshooting
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-06-Maintain-Mycelium]]"
---

# 07-03 — Orphan Edges

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
maintained in the CADMIES repository. This troubleshooting entry
documents the orphan edge issue observed during active development.

## Symptom

The relationship generator writes edges to concepts that do not exist.
The map generator reports orphan edges — references pointing to
non-existent targets.

## Root Cause

The relationship generator does not validate targets before writing
edges. When Mistral or Codestral proposes a relationship to a concept
that was never minted, the edge is written anyway.

## Historical Impact

During Session 016, 316 orphan edges were identified. 267 unique
missing targets. The strip removed 306 edges, leaving a clean graph.

## Resolution

Strip orphan edges:

```bash
python tools/strip_all_orphans.py --apply
```

The script creates a backup tarball before stripping.

## Known Tension

The root cause was not fixed. The relationship generator still does
not validate targets before writing edges. Target validation was
flagged as a future improvement.

## Prevention

Run strip_all_orphans.py --apply after relationship generation to
clean any orphans produced.

## Related
- [[04-06-Maintain-Mycelium]] — maintenance procedure
- [[05-04-Script-Inventory]] — strip_all_orphans.py details
