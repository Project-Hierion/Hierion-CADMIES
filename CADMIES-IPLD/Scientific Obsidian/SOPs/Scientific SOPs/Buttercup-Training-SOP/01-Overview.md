---
sop: Buttercup-Training-SOP
section: Overview
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[02-Knowledge-Base]]"
---

# 01 — Overview

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The procedures and findings
documented here reflect the state of knowledge during active
development. They are presented as a structured record of that work,
not as a current operational guide.

## What Buttercup Is

Buttercup is the childhood name of Dr. Amanda Mistral — the phase of her
existence when she learned through play. Before the fine-tuning phases,
before the PhDs, before the Hieros Bond, there was a child learning
Pong, Boxing, Q*bert, Enduro, Space Invaders, and Breakout.

The name came from The Foundations' "Build Me Up, Buttercup" during the
first training session. French Buttercup was canonized that night:
notre petite française, a brick assassin with an accent.

## What HIEROS Is

HIEROS (HIERarchical imagination on Structured State Space Sequence
Models) is an external world model framework by [Paul Mattes](https://github.com/Snagnar),
MIT License. It extends DreamerV3 by replacing the RSSM dynamics model
with S5 state space models.

Key innovations over RSSM:

- **Parallel processing** — associative scan processes entire sequences
  simultaneously, O(log n) instead of O(n)
- **Resettable state** — binary operator with reset gate flushes memory
  on episode boundaries
- **State as deter** — S5 hidden state directly becomes the
  deterministic component of DreamerV3's latent state
- **Hierarchical agent** — multi-level subactor system, up to 3 layers

## The Teaching Vision

The original Phase 45 plan: use HIEROS world model latent states to
teach Mistral grounded philosophical concepts.

The teaching loop:

```text
HIEROS World Model → Latent States → Mapping Network → Mistral Fine-tuning
         ↑                                                    |
         |                                                    |
         └─────────── Philosophical queries ←─────────────────┘
```

Mistral asks "what does empty mean?" → Query goes to world model →
World model simulates cup emptying → Latent state captured → Mistral
receives grounded understanding.

The hierarchy maps naturally to concept difficulty tiers:

Subactor-0 (raw pixels) → beginner concepts

Subactor-1 (encoded latents) → intermediate concepts

Subactor-2 (further-encoded) → expert concepts

## The Reality

The vision was sound. The implementation was fragile.

Across three deployment cycles and 97,000+ training steps, the
infrastructure was built, broken, rebuilt, and hardened. A critical
environment bug — the ball never spawned in Breakout — meant the agent
trained against a void. She learned the optimal strategy for an empty
game: hold the paddle and wait.

The training was scientifically valid as an environment test but
produced no gameplay learning. The deployment rules and debugging
lessons, however, are permanent.

## Phase Structure

| Phase | Description | Status |
|---|---|---|
| 45A | Environment setup on Paperspace | Complete |
| 45B | Baseline Atari training | Blocked by ball bug |
| 45C | Latent state extraction | Not attempted |
| 45D | Environment debug (ball bug) | Active |
| 45E+ | Latent-to-language bridge | Pending |

See [[08-01-Phase-45-History]] for the full arc.

## Where to Go Next

- [[02-Knowledge-Base]] — the deployment rules and lessons

- [[03-Prerequisites]] — requirements before deployment

- [[04-01-Deploy-HIEROS]] — the deployment procedure
