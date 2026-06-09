---
phase: 45 v2.0
date: 2026-06-05
status: 🔄 In Progress — v2.0 Plan
related: [[Phase-45A]], [[Phase-45B]], [[Phase-45C]], [[Phase-45D]], [[Session-028]]
---

# Phase 45 v2.0: Teaching Mistral via Snagnar HIEROS — Revised Plan

## What Changed

The original Phase 45 plan (Session 012, May 20, 2026) has been updated based on three deployment cycles, 97,000+ steps of training, and the discovery of a critical ball spawning bug in the custom atari.py wrapper. The core vision remains intact: use HIEROS world model latent states to teach Mistral grounded philosophical concepts. The implementation path has been revised to account for real-world complexity.

## Completed Phases

### 45A: Environment Setup — ✅ Complete

Three successful deployments across two GPU types (A4000, A6000). Key discoveries:
- HIEROS requires a dedicated Paperspace project with a single notebook
- Clone to `/notebooks`, not `/storage` — prevents cross-project contamination
- `pip install --no-deps` strategy eliminates version drift across container resets
- Custom atari.py wrapper required for ale-py compatibility
- Reproducible startup scripts created and tested

Documented in: Phase 45A, Phase 45B, Phase 45C

### 45B: Baseline Training — 🔄 In Progress (Blocked by Bug)

97,508 environment steps accumulated across multiple sessions. However, a critical bug was discovered: the ball never spawns in our patched Breakout environment. The agent learned to predict an empty screen (image loss 0.03) and hold the paddle still (entropy 0.05). Zero meaningful gameplay occurred.

The training is scientifically valid as an environment test but produced no gameplay learning. The world model and policy performed optimally given the broken environment — there was nothing to interact with.

Documented in: Phase 45D

## Revised Phase Sequence

### 45D: Environment Debug — 🔴 Active

**Goal:** Fix the ball spawning bug in atari.py wrapper.

**Approach:**
1. Test with Pong to determine if bug is Breakout-specific or general
2. Compare wrapper against original gym.envs.atari implementation
3. Verify FIRE action mapping, screen rendering, ROM loading
4. Fix and verify with rollout videos (not just metrics)

### 45E: Baseline Training (Real) — 📋 Pending

**Goal:** Train HIEROS on Breakout with actual ball spawning.

**Configuration (A4000):**
python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_breakout --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500


**Success criteria:**
- Rollout videos show ball appearing and agent interacting with it
- Non-zero rewards
- Agent demonstrates intentional paddle-ball interaction
- Actor entropy stays above 0.1 (avoid policy collapse)

### 45F: Latent State Extraction — 📋 Pending

**Goal:** Extract and analyze latent states at each hierarchy level.

**Method:**
1. Load trained checkpoint
2. Run inference, capture latent states at each hierarchy level
3. Map: Subactor-0 (pixels) → Subactor-1 (objects) → Subactor-2 (causal events, if max_hierarchy=3)
4. Confirm hierarchy performs conceptual abstraction

### 45G: Custom Cup Environment — 📋 Pending

**Goal:** Replace Breakout with a minimal physics scene for philosophical grounding.

- MuJoCo/DM Control scene: cup object, pusher agent, gravity
- States: upright, tilted, on_side, broken
- Agent actions: push, nudge, strike
- Target concepts: emptiness, breakage, causality, object permanence

### 45H: Latent → Language Bridge — 📋 Pending

**Goal:** Connect world model latent states to Mistral for grounded philosophical understanding.

1. Extract latent vectors for key moments
2. Train mapping network: latent_vector → natural language description
3. Feed grounded representations as training pairs to Mistral

### 45I: Mistral Fine-Tuning — 📋 Pending

**Goal:** Permanently encode grounded knowledge into Mistral's weights.

1. Collect dataset of (latent states, human descriptions)
2. Fine-tune Mistral 7B on A6000 using LlamaFactory/Unsloth
3. Export fine-tuned model as GGUF
4. Backup GGUF to local storage (PNY, SanDisk)

## Key Lessons Learned

1. **Rollout videos are essential.** Metrics alone showed a "healthy" agent. Video revealed an empty game.
2. **Test environments independently.** A quick Pong test would have caught the ball bug months ago.
3. **Dedicated project isolation is non-negotiable.** Shared projects cause CUDA initialization failures.
4. **--no-deps or die.** Pip's dependency resolver will break reproducible environments.
5. **The original vision was sound.** The implementation was fragile. The vision survives.

## Deployment Requirements (Canonical)

1. Dedicated Paperspace project per HIEROS instance
2. Clone to `/notebooks`, never `/storage`
3. Use `--no-deps` startup script with all transitive dependencies pinned
4. Verify screen dimensions: `height, width = getScreenDims()`
5. Always verify environment with rollout video before extended training