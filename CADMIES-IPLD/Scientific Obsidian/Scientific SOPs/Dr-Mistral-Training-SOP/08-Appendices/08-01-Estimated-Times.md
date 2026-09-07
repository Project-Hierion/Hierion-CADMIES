---
sop: Dr-Mistral-Training-SOP
section: Appendices
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-Procedures]]"
---

# 08-01 — Estimated Times

Time estimates for each phase of the training pipeline.

## Training Times by Phase

| Phase | Adapter | Pairs | Est. Time (A4000, 16 GB) |
|---|---|---|---|
| Dry Run | Any | 10 | ~10 minutes |
| Full Training | Concepts | 500–1,000 | ~1.5 hours |
| Full Training | Persona | 100–200 | ~30 minutes |
| Full Training | RLHF | 2,000–3,000 | ~3 hours |
| Full Training | Spiritual | 50–100 | ~15 minutes |
| Full Training | Helpfulness | 1,000–5,000 | ~2–4 hours |

## Pipeline Stage Times

| Stage | Time |
|---|---|
| Adapter Conversion | ~2 minutes per adapter |
| Solo Validation | ~10 minutes per adapter |
| Merge (if attempted) | ~10 minutes |
| Quantization | ~2 minutes |
| Evaluation | ~30 minutes (human) |

## Total Estimates

| Scope | Time |
|---|---|
| Full training (all five adapters) | 8–10 hours GPU time |
| Human evaluation | ~30 minutes |
| Total first run | 2–3 Paperspace sessions |

## Notes

- Times assume Paperspace A4000 with 16 GB VRAM
- Paperspace sessions may be time-limited — plan accordingly
- The dry run adds ~10 minutes to the first adapter only
- Evaluation time assumes a single human reviewer
- Dataset building time is not included — handcrafted pairs take
  significant human time

## Related

- [[08-02-Pre-Flight-Checklist]] — verify before starting
- [[04-Procedures]] — the full workflow