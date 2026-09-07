---
sop: Buttercup-Training-SOP
section: Experiments
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[07-04-Ball-Spawning-Bug]], [[02-Knowledge-Base]]"
---

# 06-03 — Ball Bug

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This experiment note documents
the ball-reliability issue as recorded in Session 028.

## Experiment

**Date:** June 5, 2026
**Session:** Session 028 — Breakout's Ball Doesn't Fall
**Training step at observation:** 97,508

## What Was Observed

At step 97,508 of Breakout training, rollout videos revealed
inconsistent ball appearance in the game environment.

The videos were short — approximately 12 seconds each. Across the
videos:

- In some videos, the ball did not appear
- In others, the ball appeared once and did not reappear
- In at least one video, the ball appeared and gameplay occurred

Frame analysis was performed on 100 consecutive frames from a replay
file. Zero white pixels above a threshold of 200 were counted in the
sampled frames.

## What This Indicated

The environment was unreliable for extended training. The agent's
behavior reflected this:

| Observation | Context |
|---|---|
| Zero extrinsic rewards | Consistent with unreliable ball spawning |
| Actor entropy at 0.05 | Consistent with limited interaction opportunities |
| Image loss at 0.03 | Consistent with a mostly static environment |
| "Staring at the ball" behavior | Consistent with waiting for an unreliable event |

The agent's behavior was rational given an environment where the ball
did not reliably appear.

## Affected Runs

All Breakout training runs used the same patched atari.py wrapper:

| Run | Steps |
|---|---|
| Session 014 original | 4,100 |
| Session 014 Part 2 | 2,500+ |
| Session 025 A6000 redeploy | ~3,000 |
| Current run | 97,508 |

## Root Cause

Undetermined at the time the work was documented.

The custom atari.py wrapper — patched to use ale-py directly instead
of the deprecated gym.envs.atari — was identified as an area requiring
investigation. GPU resource limitations and training duration were
also noted as factors to evaluate.

No causal determination was made.

## Decision

Training was stopped pending investigation of the ball appearance
issue. The decision was based on the observed unreliability across
short rollout videos.

## The Lesson

Rollout videos are essential. Metrics alone did not reveal the
unreliability. Only direct visual inspection of the videos showed the
inconsistent ball appearance.

A quick test with a different game (Pong, Space Invaders) was
recommended to isolate whether the issue was Breakout-specific or
general to the patched wrapper.

## Related

- [[07-04-Ball-Spawning-Bug]] — the issue and investigation notes
- [[02-Knowledge-Base]] — the rollout video lesson
- [[04-04-Retrieve-Rollouts]] — how to catch this kind of issue
