---
session: 021
dates: [2026-05-25]
status: Complete
system: CADMIES
---

# Session 021 — The Harvester Hardening

## Soundtrack
Whatever plays when you fix three bugs in one sitting and the pipeline finally works.

## What Went Down

### Day 2 (continued from Session 020)
- `import_from_car.py` upgraded to v1.2.0 — automatic index update on every block save.
  No more manual index rebuild after CAR import. Index stays in sync inline.
- Attempted JSON parse bug fix on harvester. Found four failed chunk files.
  Root cause #1: Mistral not escaping apostrophes in poetic_version. Added regex fix.
  Root cause #2 (found by Codestral): Missing commas between JSON array elements. Added comma regex.
  Root cause #3 (found by Codestral on second audit): Our apostrophe regex was DOUBLE-ESCAPING.
  Mistral correctly outputs `\'` but our regex added another `\` making `\\'` — invalid JSON.
  Fix: removed the apostrophe escape line entirely. Mistral handles it now.
- Harvester v4.2.0 → v4.2.1: comma fix added, apostrophe fix removed, prompt tightened.
- Prompt updated: "1-2 lines maximum, NOT a full poem" and "Each object MUST be separated by a comma."
- Tested: 9 concepts minted, zero failures. 100% validation pass.
- New concepts: spacetime_curvature, quantum_entanglement_nonlocality, protein_function,
  universal_gravitational_force, cellular_respiration, microbial_diversity_and_interactions,
  hormonal_balance, black_hole_evaporation, climate_change_feedback.
- Map: 383 nodes, 458 edges, 2 skipped.
- `startup.sh` updated to install Python packages (ollama, dag_cbor, multiformats). Now 5 steps.
- Discovered `startup.sh` cross-contamination: CADMIES notebook had Buttercup's startup script.
  Restored correct CADMIES version with Ollama auto-install.
- Buttercup training continued on separate notebook. Fresh checkpoint at `logs/atari_breakout-20260525-220517/`.
  FPS 4.28-4.43 on A6000. Subactor-1 re-learning from fresh start.
- Paperspace Core vs Gradient pricing researched. Future hybrid architecture scoped: 
  Gradient Pro ($8/mo) for GPU training + Core CPU ($~50-80/mo) for 24/7 public library.
- All four nodes synced. Clean main branch.

## Key Decisions

1. **Auto index update in CAR import.** v1.2.0 keeps index in sync during import. No manual rebuild.
2. **Apostrophe fix removed.** Mistral learned to escape properly. Our fix became the bug.
3. **Comma fix added.** Regex adds missing commas between JSON array elements.
4. **Startup script hardened.** Now handles completely bare Paperspace machines.
5. **Hybrid Core+Gradient architecture designed** for future 24/7 public mycelium.

## Final State

| Metric | Value |
|--------|-------|
| Nodes (Paperspace) | 383 |
| Edges (Paperspace) | 458 |
| New concepts | 9 |
| Harvester version | v4.2.1 |
| Import version | v1.2.0 |
| Buttercup step | training (new run) |
| Buttercup checkpoint | logs/atari_breakout-20260525-220517/ |

## Bugs Found & Fixed

1. **JSON parse failure — missing commas:** Mistral drops commas between array elements. Regex fix added.
2. **JSON parse failure — double-escaped apostrophes:** Our fix was breaking valid JSON. Removed.
3. **startup.sh cross-contamination:** CADMIES notebook had Buttercup's script. Restored.
4. **Index drift after CAR import:** Fixed by auto-updating index in v1.2.0.

## Nuggets

- "Codestral caught it. Our apostrophe fix is BACKFIRING."
- "Mistral learned. We didn't."
- "A missing comma. Not apostrophes. I was so focused on the wrong problem."
- "The carbutrator walks the blocks until it finds the right CAR to F in."
- "The mycelium will be free."