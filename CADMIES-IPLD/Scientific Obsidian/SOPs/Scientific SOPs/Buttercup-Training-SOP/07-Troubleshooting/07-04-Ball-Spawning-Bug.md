---
sop: Buttercup-Training-SOP
section: Troubleshooting
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[06-03-Ball-Bug]], [[04-04-Retrieve-Rollouts]]"
---

# 07-04 — Ball Appearance Issue

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This troubleshooting entry
documents the ball appearance issue observed during active development.

## Symptom

Across short rollout videos — approximately 12 seconds each — the
Breakout ball appeared inconsistently:

- In some videos, the ball did not appear
- In others, the ball appeared once and did not reappear
- In at least one video, the ball appeared and gameplay occurred

Frame analysis of 100 consecutive frames from a replay file counted
zero white pixels above a threshold of 200 in the sampled frames.

## What Was Observed

The agent's training metrics were consistent with an environment where
the ball did not reliably appear:

| Metric | Observation |
|---|---|
| Extrinsic rewards | Zero |
| Actor entropy | 0.05 |
| Image loss | 0.03 |

The agent's behavior — holding the paddle and waiting — was rational
given an environment with unreliable ball appearance.

## Investigation

The custom atari.py wrapper — patched to use ale-py directly instead
of the deprecated gym.envs.atari — was identified as an area requiring
investigation.

Additional factors noted for evaluation:

- GPU resource limitations
- Training duration
- Whether the issue was Breakout-specific or general to the patched
  wrapper

No causal determination was made.

## Recommended Next Actions

1. Test with a different game (Pong, Space Invaders) to isolate whether
   the issue is Breakout-specific or general
2. Compare the wrapper against the original gym.envs.atari
   implementation
3. Verify FIRE action mapping, screen rendering, ROM loading
4. Verify with rollout videos, not just metrics

## Related

- [[06-03-Ball-Bug]] — the experiment note
- [[04-04-Retrieve-Rollouts]] — how to verify with video
- [[02-Knowledge-Base]] — the rollout video lesson
