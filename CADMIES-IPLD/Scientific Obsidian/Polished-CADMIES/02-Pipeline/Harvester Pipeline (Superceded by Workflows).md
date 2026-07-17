---
phase: 19, 33, 35
pipeline: harvest-pipeline
date: 2026-05-15
status: Active
related: [[Phase-35-Difficulty-Levels]], , [[Phase-66-Mycelium Map UX — Fractal Succulent Layout & Progressive Loading]]
---

# Harvester Pipeline

The CADMIES Conversation Harvester is the primary concept extraction engine. It transforms raw conversations into structured, validated, minted concepts within the IPLD blockstore. The pipeline runs on GPU (Paperspace A4000) using Mistral 7B by default, with Codestral 22B available for enrichment passes.

**File:** `harvest/harvest_full_pipeline.py`

***

## Pipeline Steps

| Step | Name | Description |
|------|------|-------------|
| 1 | Load | Robust JSON loader — handles unescaped newlines, apostrophes, malformed conversation files |
| 2 | Mycelium Context | Queries existing concepts via Willie's hybrid search to ground extraction in what's already known |
| 3 | Chunk | Splits conversation into ~1000-word chunks for LLM processing |
| 4 | Extract | Sends each chunk to Mistral with a structured prompt. Returns concepts, poetics, mantras. |
| 4b | Manual Import | (No-LLM fallback) Loads unminted concept JSONs from source_concepts/ for review |
| 5 | Transform | Maps Mistral output to the UniversalScientificConcept schema. Filters invalid references. |
| 6 | Save | Writes transformed concepts to source_concepts/{human_id}.json |
| 7 | Merge | Deduplicates concepts across chunks |
| 8 | Review | Interactive menu — view, approve, skip, or quit |
| 9 | Validate | Scientific validator checks schema compliance |
| 10-11 | Mint | CID generation, blockstore save, provenance record creation |

***

## Version History

### v1.0.0 — Initial Extraction
- Basic chunk-and-extract pipeline
- No mycelium awareness
- JSON output only

### v2.0.0 — Mycelium-Aware
- Integrated Willie's hybrid search
- Existing concepts injected into extraction prompt as context
- Relevance threshold filtering

### v3.0.0 — Poetics & Mantras
- Added poetic version extraction
- Added mantra extraction
- Richer concept output

### v4.0.0 — Full Pipeline
- End-to-end: extract → review → validate → mint
- LLM-optional mode (manual import from source_concepts/)
- CID generation and blockstore integration
- Provenance records

### v4.0.1 — Hardened
- Apostrophe escaping in JSON values
- human_id lowercase enforcement
- builds_upon validation against minted IDs
- Robust markdown fence stripping
- Fixed: prose-before-fence JSON extraction

### v4.1.0 — Three-Tier Difficulty Levels
- Extraction prompt now requests three distinct explanations per concept: beginner, intermediate, expert
- transform_to_concept() maps them into difficulty_levels with fallback chain
- GPU requirement documented in file header
- Version bumped, harvester_version in extra_fields updated

***

## Key Design Decisions

1. **GPU-tier by design.** Multiple LLM calls per concept require GPU acceleration. Minimum ~6GB VRAM for Mistral 7B. CPU users use manual import path.
2. **Graceful LLM absence.** If no LLM is available, the script doesn't pretend to harvest. It switches to manual minting mode or exits cleanly.
3. **Two-pass architecture (planned).** Phase 1 extracts core concepts. Phase 2 (enrichment) adds scholarly fields: type, subdomain, limitations, applications, historical_context, discoverer, discovery_year, key_references.
4. **Case-insensitive deduplication.** human_id matching ignores case to prevent near-duplicates.
5. **Invalid reference filtering.** Mistral sometimes suggests relationships to unminted concepts. The transform step filters these with a warning.

***

## CLI Flags

| Flag | Effect |
|------|--------|
| `--auto` | Skip review menu, approve all valid concepts |
| `--batch` | Process all JSON files in harvest/conversations/ |
| `--with-relationships` | Auto-run relationship generator after minting |
| `--model=codestral` | Use Codestral 22B instead of Mistral 7B |
| `--model=tinyllama:1.1b` | Use TinyLlama (CPU-capable) |
| `--conv=path/to/file.json` | Specify a different conversation file |

***

## Known Limitations

- beginner and intermediate explanations were identical in v4.0.1 and earlier (fixed in v4.1.0)
- Batch mode currently runs each file but re-imports the module per file (needs refactor)
- Enrichment pass (Phase 2) not yet implemented
- extra_fields missing discoverer, discovery_year, limitations, applications, key_references, historical_context compared to early template concepts like bayes_theorem

***

## Related Concepts

- [[bayes_theorem]] — early concept template showing the full schema the harvester is working toward
- [[Phase-35-Difficulty-Levels]] — the fix that brought three-tier explanations online
-  — the next link in the chain after harvesting