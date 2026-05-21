> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 015 — 2026-05-21 — Phase 46: Unmapped Domain Batch Mapping

## Summary
Phase 46 tackled the 87 unmapped domain occurrences from Phase 44. Instead of mapping by name alone, we read actual concept definitions to determine what each concept was really about. Six "Science" concepts were redistributed to Philosophy, Physics, or Sociology. The remint process surfaced 40 never-minted concepts. Domain upward map expanded from ~22 to ~75 entries. 87 unmapped reduced to 11.

## Key Outcomes
- 87 original unmapped domain occurrences → 11 remaining
- 40 never-minted concepts discovered and reminted
- Concepts: 302 → 342
- Edges: 135 → 139
- Domain upward map: ~22 entries → ~75 entries
- Six source_concept files corrected (Science → real domains)
- Key principle: "Science is a method, not a domain — it's the HOW, not the WHAT."

## Remaining 11 Unmapped Domains
- Biomysticism → Philosophy
- Quantum Physics & Philosophy (2x) → Physics
- Philosophy, Religion, Physics → Philosophy
- Neuroscience & Quantum Physics → Neuroscience
- Philosophy, Psychology → Philosophy
- Philosophy, Consciousness → Philosophy
- Astrobiology → Biology
- Philosophy/Quantum Physics → Physics
- Metaphysics & Philosophy → Philosophy
- Neuroscience/Philosophy → Neuroscience

## Decisions Made
- Compound domains map to FIRST domain listed
- "Science" is not a domain — redistributed by concept content
- Linguistics in CADMIES = Philosophy of Language
- Project Management in CADMIES = Sociology
- Domain mapping based on concept content, not just labels

## Files Modified
- `tools/generate_mycelium_map.py` — DOMAIN_UPWARD_MAP expanded
- Six source_concept files — domain corrected
- `store/index/human_id_to_cid.json` — 46 entries updated

## Next Actions
- Add 11 remaining domain mappings
- Regenerate map, verify zero warnings
- Restart Ollama, run relationship generator
- Commit and push to GitHub
- Write polished Phase 46 note