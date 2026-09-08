---
sop: Concept-Harvesting-SOP
section: Experiments
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[06-01-Hieros-Origin-Harvest]], [[02-Knowledge-Base]]"
---

# 06-02 — Findings

## Compilation Note

This SOP was compiled on 2026-09-07 from session records maintained in
the CADMIES repository. The findings documented here reflect the state
of knowledge as of the August 2026 script audit.

## Finding 1: The Pipeline Scales

The Hieros Origin Harvest proved the harvester handles large inputs:

- 7,900-line founding document
- 103 concepts extracted
- 100% validation — 0 failures

The chunking strategy works. A single large document can be processed
in one harvest session.

## Finding 2: Validation Reliability

Across the Origin Harvest, every extracted concept passed validation.
The transform step successfully mapped Mistral output to the
UniversalScientificConcept schema.

## Finding 3: Meta-Self-Awareness Achieved

The harvest produced concepts about the mycelium, inside the
mycelium. The system documented its own origin story.

## Finding 4: Known Limitations Remain

| Limitation | Status |
|---|---|
| Batch mode re-imports module per file | Needs refactor |
| Enrichment pass not implemented | Pending |
| Scholarly fields missing in extra_fields | Pending |
| Relationship generator write-mode tension | Architectural decision needed |

## Finding 5: The Co-Gardener Step Is Essential

Mistral provides the skeleton. The human adds the flesh. Deeper
definitions, poetic versions, mantras — these require human judgment.

## Related

- [[06-01-Hieros-Origin-Harvest]] — the scale proof
- [[02-Knowledge-Base]] — design decisions and limitations
