---
sop: Concept-Harvesting-SOP
section: Appendices
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]]"
---

# 08-01 — Version History

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
maintained in the CADMIES repository. The version history documented
here reflects the harvester evolution as of the August 2026 script
audit.

## Harvester Version History

| Version | Date | Milestone |
|---|---|---|
| v1.0.0 | — | Initial extraction — chunk and extract |
| v2.0.0 | — | Mycelium-aware — Willie's hybrid search |
| v3.0.0 | — | Poetics and mantras added |
| v4.0.0 | — | Full pipeline — extract, review, validate, mint |
| v4.0.1 | — | Hardened — apostrophe escaping, human_id enforcement |
| v4.1.0 | — | Three-tier difficulty levels |
| v4.2.1 | 2026-08-12 | Current |

## Version Details

### v1.0.0 — Initial Extraction

- Basic chunk-and-extract pipeline
- No mycelium awareness
- JSON output only

### v2.0.0 — Mycelium-Aware

- Integrated Willie's hybrid search
- Existing concepts injected into extraction prompt
- Relevance threshold filtering

### v3.0.0 — Poetics and Mantras

- Added poetic version extraction
- Added mantra extraction
- Richer concept output

### v4.0.0 — Full Pipeline

- End-to-end: extract, review, validate, mint
- LLM-optional mode (manual import)
- CID generation and blockstore integration
- Provenance records

### v4.0.1 — Hardened

- Apostrophe escaping in JSON values
- human_id lowercase enforcement
- builds_upon validation against minted IDs
- Robust markdown fence stripping
- Fixed: prose-before-fence JSON extraction

### v4.1.0 — Three-Tier Difficulty Levels

- Extraction prompt requests three distinct explanations per concept
- transform_to_concept() maps into difficulty_levels
- Fallback chain implemented
- GPU requirement documented

## Other Script Versions

| Script | Version |
|---|---|
| generate_public_gateway.py | 3.2.1 |
| generate_mycelium_map.py | 2.4.1 |
| generate_relationships.py | 1.2.7 |
| cadmies_concept_reader.py | 1.3.0 |
| cid_generator.py | 1.2.0 |
| paths.py | 1.2.0 |

## Related

- [[02-Knowledge-Base]] — design decisions behind the versions
- [[05-04-Script-Inventory]] — current script status
