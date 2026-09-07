---
sop: Buttercup-Training-SOP
section: Knowledge Base
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[01-Overview]], [[04-01-Deploy-HIEROS]]"
---

# 02 — Knowledge Base

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The findings documented here
reflect the state of knowledge during active development.

## The Three Rules

Discovered during the third deployment cycle. These are canonical for
all future HIEROS deployments.

### Rule 1: HIEROS Gets Its Own Project

One HIEROS instance = one Paperspace project = one notebook.

A shared project caused CUDA initialization failure even when
nvidia-smi showed the GPU. Import path contamination from other
notebooks in the same project was the root cause.

**The rule:** Never deploy HIEROS in a project with other notebooks.
Dedicated project, single notebook, complete isolation.

### Rule 2: Clone to /notebooks, Not /storage

`/storage` is shared across all Paperspace projects. A HIEROS clone in
`/storage` from one project is visible to all others, creating stale
file risks and cross-project contamination.

`/notebooks` is scoped per-project. Each project has its own
`/notebooks` filesystem.

**The rule:** Clone HIEROS to `/notebooks/HIEROS`. The walled garden,
not the public park.

### Rule 3: --no-deps or Die

Every pip install with `--no-deps`. Every transitive dependency
explicitly pinned. No more pip silently upgrading numpy from 1.26.0 to
2.4.6 because jax said "numpy>=1.22."

**The rule:** The startup script is a manifest, not a suggestion. Pip
is not your friend. Pip is a suggestion engine with root access.

## Canonical Deployment Requirements

Established in Phase 45 v2.0. These are the non-negotiable requirements
for any HIEROS deployment:

1. Dedicated Paperspace project per HIEROS instance
2. Clone to `/notebooks`, never `/storage`
3. Use `--no-deps` startup script with all transitive dependencies pinned
4. Verify screen dimensions: `height, width = getScreenDims()`
5. Always verify environment with rollout video before extended training

## Checkpoint Behavior

- HIEROS saves checkpoints on schedule, not on interrupt
- Ctrl+C does NOT save a checkpoint
- Use `--save_every 500` to save every 500 environment steps
- `--from_checkpoint` requires the path to the FILE, not the directory
- Checkpoint survives container restart

See [[07-05-Checkpoint-Not-Saving]] for the full lesson.

## Rollout Videos Are Essential

Metrics alone showed a "healthy" agent. Video revealed an empty game.

The ball-spawning bug was invisible in every metric — loss was low,
entropy was low, training was stable. Only a rollout video revealed
the truth: there was no ball.

**The lesson:** Always verify environment with rollout video before
extended training. Metrics can lie.

## Batch Size by GPU

| GPU | VRAM | batch_size | batch_length | Notes |
|---|---|---|---|---|
| A4000 | 16GB | 8 | 32 | Working config. 3 hierarchy levels OOM. |
| A6000 | 48GB | 16 | 64 | Headroom for larger batches. |

See [[05-02-Batch-Size-Table]] for details.

## Key Lessons

1. **Rollout videos are essential** — metrics alone showed a healthy
   agent playing an empty game
2. **Test environments independently** — a quick Pong test would have
   caught the ball bug early
3. **Dedicated project isolation is non-negotiable** — shared projects
   cause CUDA initialization failures
4. **--no-deps or die** — pip's dependency resolver breaks reproducible
   environments
5. **The original vision was sound** — the implementation was fragile,
   the vision survives

## Related

- [[04-01-Deploy-HIEROS]] — the deployment procedure using these rules
- [[07-Troubleshooting]] — every bug that produced these lessons
- [[06-Experiments]] — the deployment cycles as evidence
