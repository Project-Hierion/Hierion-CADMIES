---
sop: Dr-Mistral-Training-SOP
section: Appendices
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]]"
---

# 08-03 — Version History

Change history for the training SOP and the training pipeline.

## SOP Version History

| Date | Change |
|---|---|
| 2026-07-22 | Training Blueprint v4.1.0 created — full pipeline spec |
| 2026-07-23 | Captain Zara Steele pilot experiment completed |
| 2026-07-23 | Dr. Mistral persona test completed — Willie problem discovered |
| 2026-09-06 | All documents consolidated into Dr-Mistral-Training-SOP vault |

## Key Discoveries Timeline

| Date | Discovery |
|---|---|
| 2026-07-23 | GGUF merge fails for Mistral 7B — dynamic LoRA required |
| 2026-07-23 | Scale 1.25 works for Zara Steele (397 pairs) |
| 2026-07-23 | Scale 1.15 works for Dr. Mistral (344 pairs) — but wrong character |
| 2026-07-23 | Dataset bias discovered — Willie dominates librarian archetype |

## Model Versions

| Version | Description |
|---|---|
| base-0.0 | Base Mistral 7B Instruct v0.3 — baseline evaluation only |
| zara-test | Captain Zara Steele persona — pilot experiment |
| dr-mistral-test | Dr. Mistral persona — partial success, wrong character |

## Source Documents

This vault was built from:

- `Dr. Amanda Mistral Training Blueprint` v4.1.0 (July 22, 2026)
- `Persona Training Pipeline — Captain Zara Steele` (July 23, 2026)
- `Dr. Amanda Mistral Persona Training — Test Results` (July 23, 2026)

All three source documents are superseded by this vault.

## Next Steps

- Clean Dr. Mistral dataset to remove Willie bias
- Add more pairs reinforcing Dr. Mistral's unique identity
- Retrain persona adapter with cleaned dataset
- Test at scale 1.15
- Fine-tune scale in 0.01 increments between 1.10 and 1.20
- Deploy with dynamic LoRA

## Related

- [[SOP Landing]] — current status
- [[06-03-Findings]] — experimental findings
- [[07-03-Wrong-Character]] — the Willie problem