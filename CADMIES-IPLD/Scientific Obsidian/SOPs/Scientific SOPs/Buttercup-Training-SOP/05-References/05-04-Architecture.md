---
sop: Buttercup-Training-SOP
section: References
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[01-Overview]]"
---

# 05-04 — Architecture

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The architecture documented
here reflects the HIEROS codebase as analyzed during active
development.

## HIEROS Architecture

HIEROS (HIERarchical imagination on Structured State Space Sequence
Models) is built on DreamerV3, replacing the RSSM dynamics model with
S5 state space models.

## Core Components

| Component | File | Function |
|---|---|---|
| S5 SSM Engine | resettable_s5/s5.py | State space model replacing RSSM; resettable hidden state |
| HiPPO Initialization | resettable_s5/init.py | Diagonalized HiPPO matrix construction |
| Associative Scan | resettable_s5/jax_compat.py | Parallel sequence processing, O(log n) |
| Hierarchical Agent | hieros/hieros.py | Multi-level subactor system, up to 3 layers |
| S5 Dynamics | hieros/networks.py | Seq2SeqDynamics wrapping S5 blocks |
| World Model | hieros/models.py | Encoder → S5 Dynamics → Decoder pipeline |
| Training Loop | hieros/train.py | Config composition, environment dispatch |
| Exploration | hieros/exploration.py | Random and Plan2Explore agents |

## Data Flow

```text
Image → CNN Encoder → S5 Dynamics (Double S5 Blocks, 4 layers) → Deter/Stoch State → Decoder predicts next frame + reward + continue
```

## Hierarchy Levels

Three hierarchy levels are built incrementally during training:

| Level | Input | Role |
|---|---|---|
| Subactor-0 | Raw pixels | Operates on pixel-level dynamics |
| Subactor-1 | Encoded latent states | Compresses to latent representations |
| Subactor-2 | Further-encoded states | Highest abstraction level |

Each level produces subgoals (8×8 grids) that feed down to the level
below. The subgoal autoencoder compresses and decompresses these
representations.

## S5 Innovations Over RSSM

- Parallel processing — associative scan processes entire sequence
simultaneously, O(log n) instead of O(n)
- Resettable state — binary operator with reset gate flushes memory
on episode boundaries
- State as deter — S5 hidden state directly becomes the
deterministic component of DreamerV3's latent state
- Double architecture — two S5 layers per block with GEGLU
activation
- Config flexibility — FF layers, activation functions, dropout,
output squashing all toggleable

## Model Specs During Training

| Property | Value |
|---|---|
| Base parameters | 12,307,361 |
| With Subactor-1 | 32,279,645 |
| Encoder | CNN (64×64×3) |
| Decoder | CNN (64×64×3) |
| Replay buffer | 1,000,000 capacity |
| Training ratio | 98% training, 2% policy |

## Source
The architecture analysis was performed during Session 012, a
file-by-file mapping of the Snagnar HIEROS repository.

## Related
- [[01-Overview]] — the teaching vision
- [[04-02-Train-from-Scratch]] — how training uses this architecture
- [[06-Experiments]] — deployment evidence
