---
sop: Buttercup-Training-SOP
section: Experiments
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[07-01-Dependency-Hell]]"
---

# 06-01 — First Deployment

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This experiment note documents
the first deployment cycle as recorded in Session 014.

## Experiment

**Date:** May 20-21, 2026
**Session:** Session 014 — Midnight Cowboy Run
**GPU:** Paperspace A4000 (16GB VRAM)

## What Was Done

First HIEROS deployment on Paperspace. The Snagnar HIEROS repository
was cloned to `/storage/HIEROS` in a project named `cadmies-snagnar`.

Dependency conflicts were resolved:

- JAX 0.4.30 / jaxlib 0.4.30 (pinned 0.4.16 unavailable)
- cloudpickle 2.2.1 (pinned 1.6.0 broken on Python 3.11)
- ale-py 0.8.0 + AutoROM (atari-py broken)
- Custom atari.py wrapper built to bypass deprecated gym.envs.atari

Breakout baseline training launched with:

--max_hierarchy 2 --batch_size 8 --batch_length 32


Three hierarchy levels OOM'd the A4000. Reduced to two.

## Results

| Metric | Value |
|---|---|
| Environment steps | 4,100 |
| FPS | 2.34 average |
| Model parameters | 12.3M → 32M |
| Rollout videos | 4 saved as .npz |

## Key Findings

1. **Checkpoint failure** — Ctrl+C did not save a checkpoint. Only
   metrics and videos survived. Lesson: HIEROS saves periodically, not
   on interrupt.

2. **Buttercup named** — The Foundations' "Build Me Up, Buttercup"
   played during training. French Buttercup canonized.

3. **Toddler phase observed** — random paddle movement, replay buffer
   filling, learning pixels.

## Second Session (Same Deployment)

**Date:** May 21, 2026, evening

A second session on the same deployment established the checkpoint
system:

- `--save_every 500` verified — checkpoint.ckpt (353MB) every 500 steps
- `--from_checkpoint` requires the file path, not directory
- Checkpoint survives container restart
- Training hit 2,500+ steps
- Image loss dropped: 1209 → 5.45
- Episodes lasting 225-325 steps
- Actor entropy down to 0.87

## Known Issues

This deployment used `/storage/HIEROS` which later proved problematic
for cross-project contamination. See [[07-02-CUDA-Init-Failure]].

The custom atari.py wrapper had a latent screen dimension bug that
surfaced in the A6000 redeploy. See [[07-03-Screen-Dimension-Bug]].

## Related

- [[06-02-A6000-Redeploy]] — second deployment cycle
- [[07-01-Dependency-Hell]] — dependency resolution battles
- [[07-05-Checkpoint-Not-Saving]] — the Ctrl+C lesson
