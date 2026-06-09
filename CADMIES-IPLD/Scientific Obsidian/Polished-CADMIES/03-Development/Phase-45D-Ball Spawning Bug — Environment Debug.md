---
phase: 45D
date: 2026-06-05
status: 🔴 Critical Bug Discovered — Ball not spawning in Breakout environment
related: [[Phase-45C-Snagnar-HIEROS-Isolated-Redeployment]], [[Session-014]], [[Session-025]], [[Session-027]]
---

# Phase 45D: Ball Spawning Bug — Environment Debug

## What Was Discovered

At step 97,508 of Breakout training on A4000, a rollout video revealed that the ball never appears in the game environment. Frame analysis of 100 consecutive frames from a replay file confirmed zero white pixels above a threshold of 200 — the ball does not exist. The agent (Buttercup) has been training for ~97,000 steps against a broken environment where no ball ever spawns.

This explains all previously observed anomalies:
- **Zero extrinsic rewards** — cannot score without a ball to hit
- **Actor entropy at 0.05** — agent learned the optimal strategy is "hold paddle and wait" because there is nothing to interact with
- **Image loss at 0.03** — agent perfectly predicted a static, unchanging environment
- **"Staring at the ball" behavior from earlier runs** — there was no ball to stare at

## Why

The custom atari.py wrapper (`/notebooks/HIEROS/embodied/envs/atari.py`) was rewritten to use `ale-py`'s `ALEInterface` directly, bypassing the deprecated `gym.envs.atari` module. The wrapper handles ROM loading, action mapping, screen capture, environment step, reset, lives tracking, and game over detection. One of these methods is failing to spawn or render the ball specifically for Breakout.

The bug may be related to:
1. The FIRE action not being properly mapped or sent to launch the ball at the start of a life
2. The screen capture method (`getScreenRGB()`) not rendering the ball sprite
3. The ROM loading or action set initialization omitting the ball spawn logic
4. The screen dimension swap fix (height/width assignment) having an unintended side effect

## Testing Performed

Frame analysis on replay file `20260605T194717F543309-...npz`:

| Frame | Min Pixel | Max Pixel | White Pixels (>200) |
|-------|-----------|-----------|---------------------|
| 0 | 0 | 200 | 0 |
| 25 | 0 | 200 | 0 |
| 50 | 0 | 200 | 0 |
| 75 | 0 | 200 | 0 |
| 100 | 0 | 200 | 0 |

Total frames: 1,024. A standard Breakout ball is rendered in white (pixel value ~200-255). The complete absence of white pixels across sampled frames confirms the ball is never rendered.

## Impact

All Breakout training runs using the patched atari.py wrapper are affected:
- Session 014 (original A4000 run, 4,100 steps)
- Session 014 Part 2 (2,500+ steps)
- Session 025 (A6000 redeploy, ~3,000 steps)
- Current run (A4000, 97,508 steps)

The agent did not learn to play Breakout. It learned to exist in an empty environment. The world model learned to predict static frames. The policy learned that no action produces reward. The training is scientifically valid as an environment test but produced no gameplay learning.

## Next Steps

| #   | Action                                                              | Priority |
| --- | ------------------------------------------------------------------- | -------- |
| 1   | Debug ball spawning in atari.py wrapper                             | 🔴       |
| 2   | Test with Pong or Space Invaders to isolate Breakout-specific issue | 🔴       |
| 3   | Compare wrapper against original `gym.envs.atari` implementation    | 🟡       |
| 4   | Fix and restart Breakout training from scratch                      | 🔴       |
| 5   | Document fix for all future deployments                             | 🟡       |