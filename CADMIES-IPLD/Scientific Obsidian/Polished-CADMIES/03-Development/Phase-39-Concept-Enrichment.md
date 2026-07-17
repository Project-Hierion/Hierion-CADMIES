---
phase: 39
date: 2026-05-15
status: Complete — Built, Tested, Deployed
related: [[Harvester Pipeline (Superceded by Workflows)]], [[Phase-35-Difficulty-Levels]], [[Phase-35-Results]], [[Session-008]], [[bayes_theorem]]
---

# Phase 39: Concept Enrichment Pipeline

## Summary

Built and deployed a two-pass concept enrichment system that brings all 174+ CADMIES concepts to a unified, complete schema. Pass 1 normalizes JSON structure across all concepts. Pass 2 uses Mistral 7B to fill missing or weak fields with scholarly content. The pipeline preserves all existing data, validates every enrichment, and maintains provenance through version increments and supersedes chains.

## Architecture

### Two-Pass Design

**Pass 1: Schema Normalizer** (`tools/normalize_concept_schema.py`)
- Reads all source_concept JSONs
- Merges each against a unified target schema (derived from bayes_theorem)
- Adds missing fields as null/empty
- Preserves ALL existing data — never modifies or deletes
- No LLM, no GPU — local-only JSON transformation
- Output: structurally identical concepts

**Pass 2: Enrichment** (`tools/enrich_concepts.py`)
- Detects 9 types of gaps: type, subdomain, difficulty_levels, discoverer, discovery_year, historical_context, limitations, applications, key_references
- Sends concept to Mistral 7B (or Codestral 22B with `--model` flag) with structured enrichment prompt
- Merges enriched fields, preserving existing quality content
- Validates enriched concept via ScientificValidator
- Remints with new CID, increments version, tracks supersedes chain
- Creates provenance record for every enrichment

### Enrichment Prompt

Designed with input from Codestral 22B. Key rules enforced:
- Return enriched fields as valid JSON only — no markdown fences, no commentary
- If a field is already well-populated, return it EXACTLY as-is
- Do not hallucinate references — only include verifiable works
- Use specific types (PhilosophicalConcept, MathematicalTheorem, etc.) not generic "Concept"
- For concepts from conversations (not historical discoveries), use "Unknown" for discoverer and null for discovery_year
- Provide three distinct difficulty tiers if current ones are weak or identical

## Test Results

### Single Concept Test: resonant_oblivion

| Field | Before | After |
|-------|--------|-------|
| type | "Concept" | "PhilosophicalConcept" |
| subdomain | "" | "Metaphysics" |
| discoverer | (missing) | "Unknown" |
| discovery_year | (missing) | null |
| historical_context | (missing) | "Originated from discussions on consciousness and memory in philosophy" |
| limitations | (missing) | ["Relies on assumption that consciousness patterns can be affected by collective memory", "Practical verification remains elusive"] |
| applications | (missing) | ["Exploring collective consciousness in psychology", "Understanding persistence of ideas in sociology", "Contemplating immortality of the soul in theology"] |
| version | 1 | 2 |
| supersedes | null | bafyreicdj6d5wxmqxt4peeqmjzwhs... |

### Batch Test: 174 Concepts

| Metric | Value |
|--------|-------|
| Concepts Processed | 174 |
| Enriched & Reminted | 22 |
| No Gaps Detected (Skipped) | ~115 |
| Source Concepts Not Found | ~35 |
| JSON Parse Failures | 2 |
| Validation Success Rate | 100% |

### Failed Enrichments

- `fractals` — JSON parse failure (raw output saved for debugging)
- `wu_wei_effortless_action` — JSON parse failure (raw output saved)

Both saved to `tools/enrich_failed_*.txt` for manual review.

## Bugs Fixed During Development

### v1.0.0 → v1.0.1

1. **Version not incrementing.** `concept["metadata"]["version"]` was being set to the current value + 1, but the current value wasn't being read correctly. Fixed by reading `current_version` before modification.
2. **Supersedes chain not tracking.** Old CID was being read from the source_concepts file AFTER it was overwritten with the enriched version. Fixed by reading old CID from the index BEFORE saving.

## Design Decisions

1. **Two-pass over one-pass.** Separating normalization (structure) from enrichment (content) keeps each tool focused and testable independently.
2. **Mistral over Codestral for batch.** Mistral's speed (5s per concept) made the 174-concept batch feasible. Codestral available for individual deep enrichment via `--model=codestral`.
3. **Conservative merge.** Enrichment only overwrites fields that are missing, empty, or demonstrably weak (identical beginner/intermediate). Existing quality content is always preserved.
4. **Gap detection over blind enrichment.** The script only calls the LLM when gaps are detected. Already-complete concepts (bayes_theorem, dunning_kruger_effect, game_theory, etc.) are skipped automatically.

## CLI Flags

| Flag | Effect |
|------|--------|
| `--concept=bayes_theorem` | Enrich a single concept |
| `--dry-run` | Preview enrichment without minting |
| `--model=codestral` | Use Codestral 22B instead of Mistral 7B |
| `--all` | Enrich all concepts even if no gaps detected |

## Integration

The enrichment pipeline integrates with existing CADMIES infrastructure:

- **CID Generator:** New CIDs for reminted concepts
- **Scientific Validator:** Validates every enriched concept before minting
- **Provenance Manager:** Records enrichment event with model, version, and supersedes info
- **Blockstore Index:** Updated with new CIDs after remint
- **Harvester Pipeline:** Future harvests will flow through Normalize → Enrich after minting

## Next Steps

- Debug and reprocess the 2 failed JSON parses
- Reconcile ~35 index entries missing source_concept JSONs
- Integrate enrichment into the main harvest pipeline as optional post-processing step
- Add `--remint-only` flag for manual edits that don't need LLM enrichment