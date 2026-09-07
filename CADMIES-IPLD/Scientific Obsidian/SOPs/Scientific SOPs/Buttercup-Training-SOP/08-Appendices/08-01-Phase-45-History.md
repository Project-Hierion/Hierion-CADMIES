---
sop: Buttercup-Training-SOP
section: Appendices
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[01-Overview]]"
---

# 08-01 — Phase 45 History

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This appendix documents the
complete Phase 45 arc as recorded during active development.

## Phase Structure

| Phase | Description | Status |
|---|---|---|
| 45A | Environment setup on Paperspace | Complete |
| 45B | Baseline Atari training | In progress — affected by ball appearance issue |
| 45C | Latent state extraction | Not attempted |
| 45D | Environment debug | Active |
| 45E+ | Latent-to-language bridge | Pending |

## Timeline

| Date | Event |
|---|---|
| 2026-05-20 | Session 012 — HIEROS architecture analysis, Phase 45 formalized |
| 2026-05-20/21 | Session 014 — First deployment on A4000, dependency hell resolved, Breakout launched |
| 2026-05-21 | Session 014 Part 2 — Checkpoint system built, 2,500+ steps |
| 2026-05-21 | Session 016 — First rollout videos, Buttercup age 2 |
| 2026-05-30/31 | Session 025 — A6000 isolated redeploy, three rules discovered, screen bug fixed |
| 2026-06-05 | Session 028 — Ball appearance issue discovered at step 97,508 |
| 2026-06-05 | Phase 45 v2.0 — Revised plan with canonical deployment requirements |

## Deployment Cycles

### First Deployment (A4000)

- `/storage/HIEROS` clone location
- Normal pip installs
- Custom atari.py wrapper
- Checkpoint lesson learned
- 4,100 + 2,500+ steps

### Second Deployment (A6000)

- `/notebooks/HIEROS` clone location
- `--no-deps` strategy
- Dedicated project, single notebook
- Screen dimension bug fixed
- ~3,000 steps

### Third Deployment (A4000 return)

- Continued from checkpoint
- 97,508 steps
- Ball appearance issue discovered
- Training stopped

## The Original Vision

The plan was to use HIEROS world model latent states to teach Mistral
grounded philosophical concepts. The teaching loop:

```text
HIEROS World Model → Latent States → Mapping Network → Mistral Fine-tuning
```

The vision remains intact. The implementation was fragile. The
deployment rules and debugging lessons are permanent.

## Related
- [[01-Overview]] — the teaching vision
- [[06-Experiments]] — deployment cycles as evidence
- [[02-Knowledge-Base]] — the lessons learned
