---
phase: 84
date: 2026-11-05
status: In Progress
related: "[[Phase-83B-Split-Brain-Recovery-and-Full-Pipeline-Rebuild]], [[Phase-57-Index-Integrity-and-Disaster-Recovery]], [[Session-066-2026-10-30-to-2026-11-03-The-October-Harvest-Massive-13-Part-DeepSeek-Conversation-Export-Extraction)]]"
---

# Phase 84: The October Harvest

## What Changed

The complete DeepSeek conversation export — 13 parts, spanning the project's conversational history — was harvested for concepts, with **2,359 draft spores** extracted into `source_concepts/` and pushed to git. The harvest phase was extraction-only by design: **zero concepts were minted during extraction**. Following the harvest, the gardener ruled that all 2,359 drafts enter the library wholesale; the full set will be minted in the next session.

Codestral 22B was formally adopted as the concept harvester's canonical extraction model following a comparative bake-off, replacing mistral:7b.

## Why

The harvest was deliberately decoupled from minting, for two reasons. First, a genuine scientific curiosity: the gardener wanted to observe what kind of concepts, if any, would emerge from heavily technical conversation material (code, scripts, and operational discussion). Second, the gardener wanted the opportunity to review the drafts and edit, enhance, or delete before minting.

Upon reviewing the results, the plan was revised: all harvested concepts are accepted into the library without exception. They all originated in real conversations, were harvested by the pipeline, and were produced as concepts — so it is what it is. Curation shifts from pre-mint to post-mint: merging, editing, and enrichment happen after the concepts are in the library, as needed.

## Changes Made

### Model Bake-Off (2026-10-30)

Twin dry runs on the same 82,716-word conversation segment were conducted to select the canonical extraction model. Comparative concept counts were treated as incidental; selection was based on qualitative evaluation across four criteria:

| Criterion | mistral:7b | codestral:22b |
|-----------|------------|---------------|
| Abstraction quality | Surface-level extraction; concepts tended to echo the source text rather than generalize from it | Genuine transferable concepts lifted from conversational material; reusable abstractions |
| Factual reliability | One factual hallucination observed (LoRA defined as "Layer-wise Relevance Adaptation") | No factual fabrications observed in the run |
| Difficulty-tier construction | Three-tier ladders present but insubstantial | Substantive beginner/intermediate/expert progression per concept |
| Noise resistance | Dragged in logistical byproduct (version-control and workflow pseudo-concepts) | Closer adherence to genuine knowledge extraction |

**Verdict:** codestral:22b adopted as the canonical concept-harvest LLM. Both models produced valid concepts, but codestral's output met the library's core requirement — durable, transferable knowledge — at materially higher fidelity. Mistral may be retried on small conversations in the future.

### Full Extraction Sweep (2026-10-30 to 2026-11-03)

- All 13 parts of the DeepSeek conversation export processed, extraction-only
- Run command: `python tools/harvest/harvest_full_pipeline.py --model=codestral:22b` (review mode, quit at menu — no mints)
- Largest parts exceeded 180 chunks at 750 words per chunk; longest single run approximately two hours on the RTX A4000
- Harvester version 4.2.1; chunk-by-chunk persistence protected all extractions against multiple Paperspace 6-hour session terminations — no spores lost
- Crown jewel: `cosmic_codebreaker` — the cross-scale pattern-recognition terminology previously missing from the taxonomy
- `scripts/startup.sh` updated to install both models and designate codestral as the standard harvest model

### Deployment

- 2,359 draft concept JSONs committed to `source_concepts/` and pushed (commit a781cd6), following standard push protocol: source_concepts only; conversation.json and harvested_concepts.json excluded; raw_failed_chunk_*.txt residue deleted before commit
- Blockstore intentionally untouched — no mints during the harvest phase
- Post-harvest decision: all 2,359 drafts accepted into the library wholesale. Curation shifted from pre-mint to post-mint: the full set will be minted in the next session, with merging, editing, and enrichment performed afterward as needed

## Testing

- Extraction review at the interactive menu for every run; spot-review of individual concepts confirmed schema conformance (UniversalScientificConcept v1.0.0), populated three-tier difficulty levels, and correct provenance stamping
- Automated reference filtering operated correctly throughout, stripping invalid builds_upon/related_to references from drafts
- Exact-title deduplication ran on each batch; cross-chapter near-duplicates intentionally preserved for later merging

## Results

| Metric | Value |
|--------|-------|
| Parts harvested | 13 of 13 |
| Draft concepts in source_concepts/ | 2,359 |
| Concepts minted (harvest phase) | 0 (by design) |
| Canonical extraction model | codestral:22b |
| Spores lost to machine timeouts | 0 |

## Analysis

The two-phase design worked. Extraction produced a raw but complete corpus of 2,359 drafts against the existing 650 minted concepts — potentially a fourfold library expansion. Known issues surfaced and confirmed live: exact-title-only deduplication leaves substantial near-duplicate families (the iterative_/adaptive_/continual_ learning cluster, the documentation_* cluster, the mycelium family); code/logistics contamination from technical conversation segments; and off-canonical domains throughout. These are all post-mint curation work items, not extraction defects.

## Known Issues (Deferred)

- Semantic deduplication remains a top pipeline guardrail — merging will absorb the cost manually post-mint
- `--conv=` flag still parsed but unused; manual import mode still has no flag
- raw_failed_chunk_*.txt cleanup still manual
- Off-taxonomy domains will need mapping during curation

## Conclusion

The harvest phase is complete: 2,359 drafts banked in git, all accepted into the library by gardener's ruling. The garden's next growth event is the mint run, followed by map and gateway regeneration, then a session-ending tarball per the cardinal rule.

## Next Steps

- Full mint run: `--auto --with-relationships --model=codestral:22b` — all 2,359 drafts
- Map and gateway regeneration
- Session-ending tarball export
- Post-mint curation: merge similar concepts, edit, enhance as needed
