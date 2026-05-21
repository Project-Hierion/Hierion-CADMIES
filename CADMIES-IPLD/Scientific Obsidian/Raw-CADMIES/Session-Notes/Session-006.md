> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 006 — 2026-05-14

## What We Did

- Pulled latest from GitHub (2 commits behind, fast-forwarded)
- Audited early concept schema (bayes_theorem) vs current harvester output
- Discovered harvester was missing: distinct difficulty tiers, discoverer, discovery_year, limitations, applications, key_references, historical_context, proper type field
- Decided on two-pass architecture: Phase 1 extracts core, Phase 2 enriches with scholarly fields
- Implemented Phase 35: three-tier difficulty levels (v4.1.0)
  - Updated EXTRACTION_PROMPT with beginner_explanation, intermediate_explanation, expert_explanation
  - Updated transform_to_concept() with fallback chain
  - Added GPU requirement note to file header
- Established Scientific Obsidian vault (Phase 37)
  - Cosmium Angelo lore: fortress to obsidian library to living mycelium
  - Vault structure: Raw CADMIES (primary workspace) + Polished CADMIES (PhD-ready)
  - Created Note-Taking Protocol
  - Created Harvester Pipeline documentation
  - Created Phase 35 documentation
  - Created this session note
- Markdown Protocol rule established for all formatted output

## What Worked

- Schema audit was revealing — comparing bayes_theorem to harvester output showed exactly what regressed
- Two-pass architecture decision was the right call — keeps extraction prompt tight, enrichment separate
- Scientific Obsidian metaphor fits CADMIES lore perfectly
- Vault structure is clean, minimal, expandable

## Decisions Made

- GPU requirement is now explicit and documented
- Harvester v4.1.0 addresses difficulty levels only — enrichment is a separate phase
- Scientific Obsidian vault is 100% public, mistakes and all
- Raw CADMIES is the default workspace, Polished CADMIES is secondary
- Methodology influenced by Dr. Rebentisch but not a clone of his system
- Roadmap stays on GitHub, vault documents the how and why
- YAML frontmatter blocks must not conflict with body content — use `***` for dividers, never `---` in body

## Nuggets Collected

- "The fortress holds the library. The library holds the records. The mycelium holds the knowledge."
- "Scientific Obsidian is the glass that remembers."
- "It's the life that weaves through it."

## Next Session

- Test harvester v4.1.0 on Paperspace
- Verify three-tier difficulty levels are distinct
- Begin Phase 2 enrichment pass design
- Backfill more vault notes (System overview, earlier sessions)
- Commit harvester changes and push to GitHub