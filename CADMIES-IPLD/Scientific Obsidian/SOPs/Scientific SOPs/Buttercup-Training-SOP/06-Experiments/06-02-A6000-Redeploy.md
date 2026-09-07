---
sop: Buttercup-Training-SOP
section: Experiments
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[06-01-First-Deployment]]"
---

# 06-02 — A6000 Redeploy

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This experiment note documents
the second deployment cycle as recorded in Session 025.

## Experiment

**Date:** May 30-31, 2026
**Session:** Session 025 — The Third Time's the Charm
**GPU:** Paperspace A6000 (48GB VRAM)

## What Was Done

Complete rebuild of the HIEROS training environment from scratch. All
prior attempts at mixed-project deployments were discarded.

Deployment details:

- New project: CADMIES-Buttercup
- New notebook: Buttercup-Playground
- Cloned HIEROS to /notebooks/HIEROS (not /storage)
- Deployed startup.sh with 20+ --no-deps installs
- Deployed patched atari.py with ale-py direct interface

## The Three Rules Discovered

1. **HIEROS gets its own project** — shared projects cause CUDA
   initialization failure even when nvidia-smi shows the GPU

2. **Clone to /notebooks, not /storage** — /storage is shared across
   all Paperspace projects; /notebooks is scoped per-project

3. **--no-deps or die** — every pip install with --no-deps, every
   transitive dependency explicitly pinned

These rules became canonical. See [[02-Knowledge-Base]].

## The Screen Dimension Bug

First launch failed:

ValueError: could not broadcast (210,160,3) into (160,210,3)


Root cause: `getScreenDims()` returns `(height, width)`, not
`(width, height)`. The original atari.py patch assigned them as
width, height. One-line fix.

This bug was always present in the custom wrapper. It never triggered
in Session 014 because the original code used `getScreenRGB2()` with
different dimension ordering. The ale-py migration changed the return
format.

See [[07-03-Screen-Dimension-Bug]] for full details.

## Results

Second launch clean:

| Metric | Value |
|---|---|
| Model parameters | 12.3M → 32.3M |
| Replay buffer | Filling |
| Training phase | Toddler — random paddle |
| Logdir | logs/atari_breakout-20260531-031943 |

## What Was Different From First Deployment

| Aspect | First Deploy | A6000 Redeploy |
|---|---|---|
| GPU | A4000 16GB | A6000 48GB |
| Clone location | /storage/HIEROS | /notebooks/HIEROS |
| Dependency strategy | Normal pip installs | --no-deps everywhere |
| Screen bug | Latent, untriggered | Caught and fixed |
| Project | Shared risk | Dedicated |

## Related

- [[06-01-First-Deployment]] — first deployment cycle
- [[02-Knowledge-Base]] — the three rules
- [[07-03-Screen-Dimension-Bug]] — the screen bug
