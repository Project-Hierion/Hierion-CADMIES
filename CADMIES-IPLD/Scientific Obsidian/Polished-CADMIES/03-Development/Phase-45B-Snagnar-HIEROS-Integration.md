---
phase: 45
date: 2026-05-21
status: In Progress — Breakout baseline training active
related: [[Phase-44-Map-Legend-Cleanup]], [[Session-014 — 2026-05-20 — Buttercup setup]], [[generate_mycelium_map.py]], Snagnar/HIEROS
---

# Phase 45: Snagnar (Paul Mattes) HIEROS World Model Integration

## What Changed

Snagnar's HIEROS (HIERarchical imagination on Structured State Space Sequence Models) was successfully cloned, configured, and deployed on Paperspace A4000 GPU. The repository required significant dependency modernization due to Python 3.11 and PyPI package availability changes. A custom Atari environment wrapper was built to bypass the deprecated `gym.envs.atari` module. Breakout baseline training was launched and has accumulated 2,500+ environment steps as of the most recent session, with model loss decreasing from 1,215 to 5.45. A reproducible startup and checkpoint system was engineered for multi-session training continuity.

## Why

Phase 45 is the first integration of an external world model architecture into the CADMIES pipeline. HIEROS extends DreamerV3 by replacing the RSSM dynamics model with S5 state space models, enabling parallel sequence processing (O(log n) via associative scan), deterministic causal chains, and resettable memory for episode boundary handling. The hierarchical subgoal system (Subactor-0 through Subactor-2) maps naturally to Phase 35's beginner/intermediate/expert concept tiers.

## Environment Setup

### Machine Configuration
- **Platform:** Paperspace Gradient Pro
- **GPU:** A4000 (16GB VRAM, 45GB RAM)
- **Template:** PyTorch (torch 2.1.1, CUDA 12.1, Python 3.11)
- **Project:** cadmies-snagnar (dedicated, isolated from main CADMIES notebooks)
- **CADMIES branch:** `phase-45-snagnar-integration`

### Repository
- **Source:** `github.com/Snagnar/HIEROS` (MIT License)
- **Location:** `/storage/HIEROS` (persistent storage, survives container restarts)
- **CADMIES clone:** `/notebooks/CADMIES` on `phase-45-snagnar-integration` branch

### Dependency Resolution

The HIEROS `requirements.txt` pins several packages to versions unavailable or broken on Python 3.11. The following substitutions were made:

| Original Pin | Issue | Resolution |
|-------------|-------|------------|
| `jax==0.4.16`, `jaxlib==0.4.16` | jaxlib 0.4.16 unavailable on PyPI for Python 3.11 | `jax==0.4.30`, `jaxlib==0.4.30` |
| `cloudpickle==1.6.0` | Bytecode incompatibility with Python 3.11 (`IndexError: tuple index out of range`) | `cloudpickle==2.2.1` |
| `atari-py` | Build failure: wheel tag unsupported on Python 3.11 | Removed entirely; replaced by `ale-py==0.8.0` + `autorom` |
| `chex==0.1.91` | Conflicts with `jax==0.4.30` (requires `jax>=0.7.0`) | Removed from startup (testing library, not needed for training) |

Additional missing packages identified through iterative import errors: `ruamel.yaml`, `rich`, `einops`, `lovely-tensors`, `lovely-numpy`, `dm_control`, `mujoco`.

### Atari Environment Wrapper

The file `/storage/HIEROS/embodied/envs/atari.py` was rewritten to bypass the deprecated `gym.envs.atari` module, which fails on gym 0.23.0 without the unavailable `ale-py~=0.7.4` extra. Key changes:

1. **ROM loading:** Replaced `gym.envs.atari.AtariEnv` with direct `ALEInterface` from `ale-py`
2. **ROM path resolution:** `getattr(ale_py.roms, name.capitalize())` — resolves through ale-py's ROM registry
3. **Action meanings:** `[a.name for a in self._action_set]` — uses Action enum names (NOOP, FIRE, RIGHT, LEFT)
4. **Screen capture:** `self._ale.getScreenRGB()` replaces deprecated `getScreenRGB2(array)`
5. **Environment step:** `self._ale.act(act)` replaces `self._env.step(action)`
6. **Reset:** `self._ale.reset_game()` replaces `self._env.reset()`
7. **Lives tracking:** `self._ale.lives()` replaces `self._ale.lives()` (unchanged method name)
8. **Game over detection:** `self._ale.game_over()` replaces `self._env.step()` return value parsing

### Startup Script

A reproducible startup script was created at `/storage/HIEROS/startup.sh` to handle the Paperspace fresh-container limitation (system packages do not persist on `/storage`, only files do). The script installs all verified working package versions and runs `AutoROM --accept-license` for Atari ROMs. Total install time: approximately 30 seconds.

## Training Configuration

### Final Working Command

```
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

### Configuration Decisions

| Parameter | Original Value | Working Value | Rationale |
|-----------|---------------|---------------|-----------|
| `--max_hierarchy` | 3 | 2 | 3 levels OOM'd A4000 (16GB) — 53M params exceeded VRAM |
| `--batch_size` | 16 | 8 | Reduced to fit 16GB alongside 32M-param model |
| `--batch_length` | 64 | 32 | Halved for memory alongside batch_size reduction |
| `--save_every` | not set | 500 | Enables checkpointing every 500 env steps for multi-session training |

### Model Architecture
- **Parameters:** 12,307,361 (Subactor-0 only) → 32,279,645 (Subactor-1 added)
- **Dynamics:** S5 (Structured State Space) with double S5 blocks, 4 layers
- **Hierarchy:** 2 levels (Subactor-0: raw pixels, Subactor-1: encoded latents)
- **Encoder:** CNN (image: 64×64×3)
- **Decoder:** CNN (image: 64×64×3)
- **Replay buffer:** 1,000,000 capacity
- **Training ratio:** 98% training, 2% policy (fps 2.27-2.39)

## Training Progress

### Session 014 Part 1 (May 20-21, midnight)
- **Environment steps:** 4,100
- **Training cycles:** ~600+
- **FPS:** 2.34 average
- **Image loss trajectory:** 1,480 (step 712) → 2.87 (step 2,988)
- **Checkpoint:** None saved (Ctrl+C before `--save_every` was configured)

### Session 014 Part 2 (May 21, evening)
- **Environment steps:** 2,500+ (ongoing)
- **Training cycles:** 500+ 
- **FPS:** 2.27-2.39
- **Image loss trajectory:** 1,209 (step 736) → 5.45 (step 2,500)
- **Episode duration:** 225-325 steps per episode
- **Score:** 0 (agent has not yet learned to intentionally break bricks for points)
- **Checkpoint:** `/storage/HIEROS/logs/atari_breakout-20260521-191612/checkpoint.ckpt` (353MB, saved every 500 steps)

### Agent Developmental Stage
The agent has progressed from random exploration (toddler phase, Session 014 Part 1) to consistent paddle-ball interaction (preteen phase, Session 014 Part 2). Key indicators:
- **Actor entropy:** 1.8+ (toddler) → 0.87 (preteen) — reduced randomness, more intentional actions
- **Image loss:** 1,480+ → 4.82 — world model accurately predicts frame transitions
- **Episode length:** Initially frames-long → 225-325 steps — sustained play
- **Value novelty:** 6.98 — still exploring environment, not optimizing for score
- **Score:** 0 — has not connected brick destruction to point accumulation

## Checkpoint System

### Problem
Initial assumption that Ctrl+C would trigger a graceful checkpoint save was incorrect. HIEROS saves checkpoints only on scheduled intervals, not on interrupt. The first 4,100 steps of training were lost when the notebook was stopped.

### Solution
`--save_every 500` triggers a checkpoint write every 500 environment steps. The checkpoint file (`checkpoint.ckpt`, ~353MB) contains full model state, optimizer state, and replay buffer. It overwrites on each save (single checkpoint, most recent state).

### Resume Command
```
bash /storage/HIEROS/startup.sh && \
python hieros/train.py \
  --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs \
  --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 \
  --task atari_breakout --tensorboard_logging True --wandb_logging False \
  --batch_size 8 --batch_length 32 --save_every 500 \
  --from_checkpoint /storage/HIEROS/logs/atari_breakout-20260521-191612/checkpoint.ckpt
```

Note: `--from_checkpoint` requires the path to the checkpoint FILE, not the log directory. This was the source of the `IsADirectoryError` during the first resume attempt.

### Future Enhancement
A dual-checkpoint rotation system (checkpoint_A.ckpt / checkpoint_B.ckpt) is planned for the next session to provide redundancy against corruption during save operations.

## Rollout Videos

Four `.npz` files containing rollout frames were saved during Session 014 Part 1 at:
- `/storage/HIEROS/logs/atari_breakout-20260521-034737/train_eps/replay/`

Files span the full training session (04:16 to 05:46 UTC), representing the agent's progression from random movements to intentional play. These are NumPy archives of image sequences and can be converted to MP4 format for visualization. Conversion script planned for a future session.

## Issues Encountered

### Dependency Version Lock
HIEROS pins specific package versions that are incompatible with Python 3.11. Resolution required version bumps on JAX (0.4.16 → 0.4.30), cloudpickle (1.6.0 → 2.2.1), and replacement of atari-py with ale-py.

### Atari Environment Module
`gym.envs.atari` does not exist in gym 0.23.0 when installed without the unavailable `ale-py~=0.7.4` extra. The entire Atari wrapper (`/storage/HIEROS/embodied/envs/atari.py`) was rewritten to use `ale-py`'s `ALEInterface` directly, mapping each method call to its modern equivalent.

### Container Ephemerality
Paperspace containers reset system-level Python packages on each restart. Only files on `/storage` persist. The `startup.sh` script resolves this by reinstalling all dependencies in a single command (~30 seconds). This is a known constraint of the Paperspace Gradient environment and is now documented in the startup procedure.

### CUDA Out of Memory
The original 3-hierarchy-level, full-batch-size configuration (53M parameters) exceeded the A4000's 16GB VRAM. Configuration was reduced to 2 hierarchy levels (32M parameters) with halved batch dimensions. This fits comfortably and training proceeds without OOM errors.

### Checkpoint Directory Error
`--from_checkpoint` expects a file path, not a directory path. Passing the log directory resulted in `IsADirectoryError`. Corrected by pointing to the specific `checkpoint.ckpt` file.

## Analysis

### Training Efficiency
At 2.27-2.39 fps with 500 steps per epoch, the agent processes approximately 6,000-7,000 environment steps per 3-hour session. The full 100,000-step Breakout baseline is projected to require approximately 14-17 more sessions (42-51 hours) on the A4000, or approximately 2-3 weeks at the current pace.

### Model Convergence
The image loss trajectory demonstrates rapid early learning followed by diminishing returns:
- Steps 0-1000: Loss 1,480 → ~100 (rapid pixel prediction learning)
- Steps 1000-2500: Loss ~100 → 4.82 (fine-tuning of world model)
- Steps 2500+: Approaching asymptote (diminishing returns on frame prediction)

The agent's current bottleneck is not perception but policy — it can predict frames accurately but has not yet learned to optimize for score.

### Hierarchy Utilization
Subactor-1 (encoded latents) was added at approximately step 500 and is actively training. Its model loss (789 → 104) indicates successful abstraction learning. The two-level hierarchy is functioning as designed, with Subactor-0 handling pixel-level dynamics and Subactor-1 compressing to latent representations.

### Reproducibility
The startup script ensures exact environment reproducibility across sessions. The checkpoint system ensures training continuity. Together, they transform Paperspace from a single-session environment into a multi-session research platform.

## Conclusion

Phase 45A (environment setup) is complete. Phase 45B (Breakout baseline training) is in progress with 2,500+ steps accumulated, a working checkpoint system, a reproducible startup procedure, and a fully patched Atari environment wrapper. The S5 state space model is learning Breakout dynamics with decreasing image loss and increasing episode duration. The agent has progressed from random exploration to intentional paddle-ball interaction, though it has not yet learned to optimize for score.

The primary remaining tasks are:
1. Complete 100,000-step Breakout baseline (Phase 45B)
2. Extract and analyze latent states at each hierarchy level (Phase 45C)
3. Evaluate S5 world model prediction quality (Phase 45D)

## Next Steps

| #   | Action                                                 | Phase | Priority |
| --- | ------------------------------------------------------ | ----- | -------- |
| 1   | Continue Breakout training from checkpoint             | 45B   |        |
| 2   | Build dual-checkpoint rotation script                  | 45B   | 🟡       |
| 3   | Convert .npz rollout files to MP4                      | 45B   | 🟡       |
| 4   | Extract latent states from trained model               | 45C   | 🟡       |
| 5   | Analyze hierarchy abstraction mapping to concept tiers | 45C   | 🟢       |
| 6   | Design custom cup environment (DM Control)             | 45E   | 🟢       |