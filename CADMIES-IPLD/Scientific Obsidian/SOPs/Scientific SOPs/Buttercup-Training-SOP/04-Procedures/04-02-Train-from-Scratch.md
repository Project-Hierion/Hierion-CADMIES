---
sop: Buttercup-Training-SOP
section: Procedures
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-01-Deploy-HIEROS]], [[05-01-Training-Commands]]"
---

# 04-02 — Train from Scratch

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The procedure documented here
reflects the training method used during active development.

## When to Use

- After deployment is verified
- When starting a new Buttercup training run
- When training on a different Atari game

## Procedure

### Step 1: Navigate to HIEROS

```bash
cd /notebooks/HIEROS
```

### Step 2: Launch training

```bash
python hieros/train.py \
  --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs \
  --max_hierarchy 2 \
  --subgoal_visualization True \
  --dynamics_model s5 \
  --task atari_breakout \
  --tensorboard_logging True \
  --wandb_logging False \
  --batch_size 8 \
  --batch_length 32 \
  --save_every 500
```

Replace atari_breakout with the target game. See
[[05-01-Training-Commands]] for all game commands.

### Step 3: Monitor training

The training loop produces environment steps, FPS metrics, and loss
values. Key indicators:

- **Image loss** — world model prediction quality. Should drop rapidly
  in early training, then approach an asymptote.
- **Actor entropy** — policy randomness. High at start (1.8+), should
  decrease as the agent learns intentional behavior. Below 0.1 may
  indicate policy collapse.
- **Episode length** — should increase as the agent learns to sustain
  play.
- **Score** — should eventually become non-zero if the environment is
  correct.

### Step 4: Watch for checkpoints

With `--save_every 500`, a checkpoint is written every 500 environment
steps. The checkpoint file is `checkpoint.ckpt` in the log directory.

## Configuration Decisions

| Parameter | Value | Rationale |
|---|---|---|
| --max_hierarchy | 2 | 3 levels OOM on A4000 (16GB) |
| --batch_size | 8 | Fits 16GB alongside 32M-param model |
| --batch_length | 32 | Halved for memory |
| --save_every | 500 | Checkpoint every 500 env steps |

## Model Architecture During Training

- **Parameters:** 12,307,361 (Subactor-0 only) → 32,279,645
  (Subactor-1 added)
- **Dynamics:** S5 with double S5 blocks, 4 layers
- **Hierarchy:** 2 levels (Subactor-0: pixels, Subactor-1: latents)
- **Encoder:** CNN (64×64×3)
- **Decoder:** CNN (64×64×3)
- **Replay buffer:** 1,000,000 capacity

## Verification

- [ ] Training launches without errors
- [ ] Model compiles at 12.3M parameters
- [ ] Subactor-1 activates at ~32M parameters
- [ ] Image loss decreasing
- [ ] First checkpoint written at 500 steps
- [ ] Rollout video shows correct environment

## Related

- [[05-01-Training-Commands]] — commands for all games
- [[05-02-Batch-Size-Table]] — GPU configuration
- [[04-03-Resume-from-Checkpoint]] — resuming training
