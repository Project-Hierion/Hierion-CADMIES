---
phase: 35
date: 2026-05-14
status: Complete
related: [[Harvester Pipeline (Superceded by Workflows)]], [[bayes_theorem]], [[Session-006]]
---

# Phase 35: Three-Tier Difficulty Levels

## What Changed

Updated `harvest_full_pipeline.py` v4.0.1 to v4.1.0 to fix a schema regression where `beginner` and `intermediate` difficulty levels were populated with the same definition string. Early CADMIES concepts (e.g., `bayes_theorem`) had three distinct, tiered explanations. The harvester lost this when it was built.

## Why

The original schema, designed during the PhD template phase, specified three distinct difficulty tiers:

- **Beginner:** ELI5 — simple language, relatable metaphor, no jargon
- **Intermediate:** Proper terminology, connects to related concepts
- **Expert:** Full depth, philosophical implications, edge cases

The harvester's `transform_to_concept()` function was mapping both `beginner` and `intermediate` to `extracted.get("definition", "")`, producing identical text for both levels. Only `expert` received distinct content from the `insight` field.

This meant the public gateway's difficulty tabs would show the same text for two of three settings.

## Changes Made

### 1. Extraction Prompt

Added three new fields to the JSON template Mistral is instructed to return. The `definition` field remains the canonical 1-3 sentence definition. The three explanation fields are additional, tier-specific expansions with explicit instructions for what each tier requires.

### 2. Transform Function

Updated the `difficulty_levels` mapping with a fallback chain. If Mistral fails to provide the new fields (backward compatibility), the function falls back to using `definition` for beginner/intermediate and `insight` for expert — the old behavior — gracefully.

### 3. GPU Requirement Documentation

Added a GPU requirement notice to the file header, making explicit what was already implicit: this pipeline requires GPU acceleration for practical use. Minimum ~6GB VRAM for Mistral 7B, 12GB+ recommended for Codestral enrichment.

## Testing

To be tested on Paperspace A4000 with Mistral 7B. A harvest run with a test conversation will verify:

- [ ] All three difficulty levels contain distinct text
- [ ] Beginner uses simple language and metaphor
- [ ] Intermediate uses proper terminology
- [ ] Expert contains philosophical depth and novel insight
- [ ] Fallback chain works if fields are missing

## Sample Expected Output

For a concept like `relational_entanglement`, the three tiers should differ meaningfully:

- **Beginner:** "Imagine two dancers moving together — when one spins, the other spins too, even if they're on opposite sides of the room. They're entangled because they're part of the same dance."
- **Intermediate:** "Relational entanglement describes how entities become correlated through interaction history such that measuring one provides information about the other, regardless of spatial separation."
- **Expert:** "Relational entanglement extends quantum entanglement's formalism into a philosophical framework where correlation is ontologically prior to separation. It challenges the assumption that objects exist independently before interaction, suggesting instead that relationship constitutes identity."

## Related Schema Fields

The `bayes_theorem` concept (minted 2026-04-03) served as the reference template. Its `difficulty_levels` already demonstrated the three-tier pattern the harvester needed to restore. Additional fields present in that template but still missing from the harvester will be addressed in a future enrichment pass (Phase 2 of the extraction pipeline).