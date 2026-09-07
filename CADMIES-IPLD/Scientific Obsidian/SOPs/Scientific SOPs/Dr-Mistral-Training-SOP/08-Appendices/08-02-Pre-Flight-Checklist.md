---
sop: Dr-Mistral-Training-SOP
section: Appendices
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-01-Environment-Setup]]"
---

# 08-02 — Pre-Flight Checklist

Verify everything before executing the first training run.

## Before First Training Run

- [ ] Base model downloaded — `base-mistral.gguf` exists and is Q4_K_M
- [ ] Ollama installed — `which ollama` returns a path
- [ ] zstd installed — `which zstd` returns a path
- [ ] Tokenizer verified — v0.2 vs v0.3 compatibility confirmed
- [ ] Environment snapshot created — `/notebooks/.env` exists, `source` works
- [ ] Directory structure created — all folders from [[05-01-Directory-Structure]] exist
- [ ] Baseline evaluation complete — `base-0.0` scores logged to `evaluation_log.csv`
- [ ] All five pair-building scripts ready
- [ ] Validation script ready and tested
- [ ] Modelfile ready — includes safety additions and `num_predict 512`
- [ ] Dry run passed — pipeline verified with 10 pairs
- [ ] Time budget allocated — plan for 8–10 hours total GPU time
- [ ] Backup strategy confirmed — can restore base model if everything fails
- [ ] Recovery procedures understood — know where base model lives and how to roll back

## Before Each Adapter

- [ ] Training data validated — no format errors
- [ ] Dataset hash recorded — for version tracking
- [ ] Solo validation planned — test before full merge
- [ ] Training log ready — training_log.csv accessible

## Before Deployment

- [ ] Dynamic LoRA tested — not merge
- [ ] Scale sweet spot documented
- [ ] Modelfile versioned
- [ ] Sanity check passed
- [ ] merge_log.csv updated

## Emergency Recovery Check

- [ ] Base model location known
- [ ] Rollback procedure understood — see [[08-03-Version-History]]
- [ ] Previous good model available
- [ ] Password manager accessible for any credentials needed

## Related

- [[04-01-Environment-Setup]] — setup procedure
- [[08-01-Estimated-Times]] — time budget
- [[05-01-Directory-Structure]] — directory reference