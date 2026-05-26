> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 021 — The Harvester Hardening

## Soundtrack
Pine Vinyl — Luke LaRock. Bong rips. Flaming Hot Cheeto Puffs. Bob's judgmental mustache.

## What Went Down

- Resumed from Session 020 (May 25, 5:15 PM).
- `import_from_car.py` upgraded to v1.2.0 — automatic index update on every block save.
  No more manual index rebuild after CAR import.
- Debugged JSON parse failures in harvester. Four root causes identified and fixed:
  1. Missing commas between array elements (Codestral found it).
  2. Double-escaped apostrophes — our fix was breaking valid JSON. Removed it.
  3. Prose before JSON — Mistral finishes sentences before outputting JSON. 
     Fix: strip everything before first `{`.
  4. Chunk size reduced from 1000 to 750 words.
- Codestral audited all 337 source concepts. Found 3 with missing difficulty levels.
  Enriched them. 100% validation pass.
- Merged 4 case-variant duplicates into lowercase canonicals.
- Added 15 unmapped domains to DOMAIN_UPWARD_MAP. Map legend clean.
- `startup.sh` hardened for bare Paperspace machines. 5 steps including Ollama auto-install.
  Cross-contamination with Buttercup's script discovered and fixed.
- Paperspace Core vs Gradient pricing researched. Hybrid architecture scoped.
- Buttercup training continued on separate notebook.
- Two full harvest runs: 23 new concepts minted, zero parse failures.
- All four nodes synced. CAR exported.

## Final State

| Metric | Start | End |
|--------|-------|-----|
| Nodes | 383 | 404 |
| Edges | 458 | 512 |
| Harvester | v4.1.0 | v4.2.2 |
| Import | v1.1.0 | v1.2.0 |
| Source concept issues | 3 | 0 |
| Duplicates | 4 | 0 |
| Parse failures | Multiple | 0 |

## Bugs Fixed

1. Missing commas in JSON arrays — regex fix
2. Double-escaped apostrophes — removed broken fix
3. Prose before JSON — strip to first `{`
4. `llm_mycelium_reader` → `cadmies_concept_reader`
5. `car_utils.py` location: `tools/` → `tools/core/`
6. `read_car_index()` missing — added to car_utils v1.0.3
7. Startup script cross-contamination

## Nuggets

- "A missing comma. Not apostrophes. I was so focused on the wrong problem."
- "Mistral learned. We didn't."
- "ZERO. FAILURES. ZERO. ERRORS."
- "Mistral extracts, Codestral enriches. Option B, Alex."

## Next Steps (Session 022)

- Option B: Mistral extracts → Codestral enriches pipeline
- Fix new unmapped domains (Climate Science, Plant Physiology, Oceanography, etc.)
- Resume Buttercup training from checkpoint
- Phase 52: llama.cpp groundwork