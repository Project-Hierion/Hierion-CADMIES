---
phase: 45C
date: 2026-05-30
status: 🔴 In Progress — Breakout baseline training active on A6000
related: [[Phase-45A-Snagnar-HIEROS-Integration]], [[Phase-45B-Snagnar-HIEROS-Integration]], [[Session-014]]
---

# Phase 45C: Snagnar HIEROS — Isolated Redeployment with Hardened Scripts

## What Changed

The HIEROS training environment was completely rebuilt from scratch on a dedicated Paperspace A6000 GPU. All prior attempts at mixed-project deployments (sharing `/storage` or `/notebooks` with other CADMIES notebooks) were discarded. The repository was cloned to `/notebooks/HIEROS` inside a dedicated `CADMIES-Buttercup` project with a single notebook (`Buttercup-Playground`). A new dependency installation strategy using `pip install --no-deps` for every package was developed to eliminate version drift. The Atari environment wrapper was patched with a screen dimension fix discovered during deployment. Training launched successfully on the A6000 and is accumulating steps.

## Why

Phase 45B established that HIEROS can train on Paperspace, but suffered from three systemic problems: (1) container resets wiped Python packages while `/storage` files persisted, requiring reinstallation every session; (2) pip's dependency resolver silently upgraded pinned packages (numpy 1.26.0 → 2.4.6, jax 0.4.30 → 0.7.1) when resolving transitive dependencies; (3) the HIEROS clone shared `/storage` with other projects, creating cross-contamination risk. Phase 45C addresses all three by isolating the project, pinning every dependency with `--no-deps`, and documenting the exact working configuration.

### Critical Discovery: Project Isolation

**HIEROS cannot coexist in the same Paperspace project or `/storage` as other notebooks.** The first successful run (Phase 45B) used a dedicated `cadmies-snagnar` project — this was correct but not documented as a requirement. The failed "Buttercup" rename attempt placed HIEROS in a project with two other CADMIES notebooks, causing import conflicts, path confusion, and the CUDA initialization failure observed at the start of this session. The rule is now explicit: **one HIEROS clone = one Paperspace project = one notebook.**

### Critical Discovery: `/notebooks` Over `/storage`

The Phase 45B deployment used `/storage/HIEROS` for persistence. This worked but meant the clone was shared across ALL Paperspace projects. When switching from the A4000 project to the A6000 project, the old `/storage/HIEROS` was still present with stale files. `/notebooks` is scoped per-project — each project has its own `/notebooks` filesystem. For HIEROS, `/notebooks/HIEROS` provides the same persistence guarantees as `/storage` but without cross-project contamination.

## Environment Setup

### Machine Configuration
- **Platform:** Paperspace Gradient Pro
- **GPU:** NVIDIA RTX A6000 (48GB VRAM)
- **Template:** PyTorch (torch 2.1.1+cu121, CUDA 12.1, Python 3.11.7)
- **Project:** CADMIES-Buttercup (dedicated, single notebook)
- **Notebook:** Buttercup-Playground

### Repository
- **Source:** `github.com/Snagnar/HIEROS` (MIT License)
- **Location:** `/notebooks/HIEROS` (project-scoped, persists across container restarts)
- **Explicitly NOT in `/storage`** — avoids cross-project contamination

### Dependency Strategy: `--no-deps` Everywhere

The Phase 45B startup script installed packages normally, allowing pip's dependency resolver to upgrade pinned versions. Phase 45C uses `pip install --no-deps` for every single package, with all transitive dependencies listed and pinned explicitly. This guarantees version stability across container resets and PyPI changes.

**Full dependency manifest (Phase 45C, verified working):**

Core:
- `jax==0.4.30`, `jaxlib==0.4.30`
- `numpy==1.26.0`, `scipy==1.11.2`, `opt-einsum==3.3.0`, `ml-dtypes==0.2.0`
- `einops==0.6.1`, `optax==0.1.7`
- `cloudpickle==2.2.1`

Environments:
- `gym==0.23.0`, `ale-py==0.8.0`, `dm_control==1.0.14`, `mujoco==3.9.0`
- Transitive: `gym-notices==0.1.0`, `dm-env==1.6`, `dm-tree==0.1.10`, `glfw==2.10.0`, `labmaze==1.0.6`, `pyopengl==3.1.10`, `importlib-resources==7.1.0`

Atari:
- `autorom==0.6.1` + `AutoROM --accept-license`

Utilities:
- `crafter==1.8.1`, `ruamel.yaml==0.17.33`, `rich==13.5.3`
- Transitive: `opensimplex==0.4.5.1`, `ruamel.yaml.clib==0.2.15`, `markdown-it-py==4.2.0`, `mdurl==0.1.2`

Display/Logging:
- `tensorboard==2.14.1`, `lovely-tensors==0.1.15`, `lovely-numpy==0.2.9`
- Transitive: `fastcore==1.13.2`

Video/Image:
- `opencv-python==4.8.1.78`, `moviepy==1.0.3`
- Transitive: `decorator==4.4.2`, `imageio-ffmpeg==0.6.0`, `proglog==0.1.12`

Misc:
- `tqdm==4.66.1`

**Packages intentionally excluded:**
- `chex` — conflicts with jax 0.4.30 (requires jax>=0.7.0), not needed for training
- `atari-py` — dead package, replaced by ale-py + autorom
- `dm-sonnet` — not needed for training
- `wandb` — logging disabled
- `zmq` — broken version pin in requirements.txt
- `black` — dev tool only

### Startup Script

The startup script is located at `/notebooks/HIEROS/startup.sh`. It installs every package with `--no-deps` in dependency order, with 2-3 second pauses between groups. Total install time: approximately 30 seconds. The script is idempotent — it can be run on any fresh container and will produce an identical environment.

### Atari Environment Wrapper

The file `/notebooks/HIEROS/embodied/envs/atari.py` was rewritten to use `ale-py`'s `ALEInterface` directly, bypassing the deprecated `gym.envs.atari` module. Key changes from Phase 45B:

1. **ROM loading:** `getattr(ale_py.roms, name.capitalize())` — resolves through ale-py's ROM registry
2. **Action meanings:** `[a.name for a in self._action_set]` — uses Action enum names
3. **Screen capture:** `self._ale.getScreenRGB()` replaces deprecated `getScreenRGB2()`
4. **Environment step:** `self._ale.act(act)` replaces `self._env.step(action)`
5. **Reset:** `self._ale.reset_game()` replaces `self._env.reset()`
6. **Game over detection:** `self._ale.game_over()` replaces return value parsing

**Phase 45C bug fix — Screen dimension swap:**
`getScreenDims()` returns dimensions as `(height, width)` but the original code assigned them as `width, height`, creating a buffer of shape `(160, 210, 3)` when `getScreenRGB()` returns `(210, 160, 3)`. This caused a `ValueError: could not broadcast input array from shape (210,160,3) into shape (160,210,3)` on first launch. Fixed by swapping the variable assignment to `height, width = self._ale.getScreenDims()`.

## Training Configuration

### Working Command (Phase 45C)

cd /notebooks/HIEROS && python hieros/train.py  
--configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs  
--max_hierarchy 2  
--subgoal_visualization True  
--dynamics_model s5  
--task atari_breakout  
--tensorboard_logging True  
--wandb_logging False  
--batch_size 8  
--batch_length 32  
--save_every 500


### Configuration Notes

The command is identical to Phase 45B's working configuration. The A6000's 48GB VRAM provides significant headroom (Phase 45B used 16GB A4000), but batch parameters were kept conservative for this initial run. Future sessions may increase `--batch_size` and `--batch_length` to leverage the additional memory.

### Model Architecture
- **Parameters:** 12,307,361 (Subactor-0 only) → 32,279,645 (Subactor-1 added)
- **Dynamics:** S5 (Structured State Space) with double S5 blocks, 4 layers
- **Hierarchy:** 2 levels (Subactor-0: raw pixels, Subactor-1: encoded latents)
- **Encoder:** CNN (image: 64×64×3)
- **Decoder:** CNN (image: 64×64×3)
- **Replay buffer:** 1,000,000 capacity
- **Logdir:** `logs/atari_breakout-20260531-031943`

## Deployment Sequence

The full deployment from blank notebook to training launch:

1. Deleted stale `/storage/HIEROS` from previous projects
2. Cloned `Snagnar/HIEROS` to `/notebooks/HIEROS`
3. Deployed hardened `startup.sh` with `--no-deps` strategy and all transitive dependencies
4. Deployed patched `atari.py` with ale-py direct interface
5. Ran `bash /notebooks/HIEROS/startup.sh` — all packages installed without version drift
6. Verified imports: numpy 1.26.0, jax 0.4.30, ale_py OK, atari.py OK
7. Launched training — hit screen dimension error on first attempt
8. Fixed `height, width` assignment in `atari.py` line 56
9. Relaunched — training started successfully
10. Model compiled: 12.3M → 32.3M parameters, Subactor-1 activated, replay buffer filling

## Issues Encountered

### Cross-Project Contamination (Phase 45C discovery)
HIEROS deployed in a project with other notebooks caused CUDA initialization failure (`RuntimeError: No CUDA GPUs are available`) despite GPU being visible to `nvidia-smi` and PyTorch. Root cause appears to be import path conflicts or environment variable contamination from other notebooks in the same project. **Resolution:** Dedicated project with single notebook. This is now a hard requirement.

### `/storage` vs `/notebooks` Scope (Phase 45C discovery)
`/storage` is shared across all Paperspace projects. A HIEROS clone in `/storage` from one project is visible to all others, creating stale file risks. `/notebooks` is scoped per-project. **Resolution:** Clone to `/notebooks/HIEROS` for project-level isolation.

### Screen Dimension Swap (Phase 45C bug fix)
`getScreenDims()` returns `(height, width)` not `(width, height)`. Original atari.py patch assigned these incorrectly, creating a shape mismatch between the screen buffer and `getScreenRGB()` output. **Resolution:** Swapped variable names in the assignment. This bug was not caught in Phase 45B because the original `getScreenRGB2()` function had different dimension ordering — the ale-py migration introduced the change.

## Analysis

### Deployment Reliability
The `--no-deps` strategy transforms the startup script from "usually works" to "guaranteed reproducible." Every package version is explicit. No dependency resolver can override our pins. This eliminates the most common failure mode from Phase 45B (version drift on container restart).

### Hardware Headroom
The A6000's 48GB provides 3× the VRAM of the Phase 45B A4000 (16GB). The current configuration uses approximately the same memory as Phase 45B, leaving substantial headroom. Potential optimizations for future sessions:
- Increase `--batch_size` from 8 to 16 or 24
- Increase `--batch_length` from 32 to 64
- Potentially enable `--max_hierarchy 3` (was OOM on A4000)

### Project Isolation as a Requirement
The failed CUDA initialization on the shared-project notebook confirms that HIEROS is sensitive to its environment context. The dedicated CADMIES-Buttercup project with a single Buttercup-Playground notebook provides complete isolation. This constraint should be documented as a deployment requirement for all future HIEROS work.

## Conclusion

Phase 45C establishes a hardened, reproducible, isolated HIEROS deployment on an A6000 GPU. The `--no-deps` dependency strategy, `/notebooks`-based project isolation, and screen dimension bug fix represent concrete improvements over the Phase 45B deployment. Training is active and accumulating steps. The agent (Buttercup) is in its toddler phase — random exploration, replay buffer filling, Subactor-0 learning pixel dynamics.

The primary remaining tasks from Phase 45B carry forward:
1. Complete 100,000-step Breakout baseline (Phase 45C — in progress)
2. Extract and analyze latent states at each hierarchy level (Phase 45D)
3. Evaluate S5 world model prediction quality (Phase 45D)
4. Consider A6000 batch size scaling to accelerate training

## Next Steps

| #   | Action                                                 | Phase | Priority |
| --- | ------------------------------------------------------ | ----- | -------- |
| 1   | Continue Breakout training, monitor for first checkpoint | 45C   | 🔴       |
| 2   | Evaluate batch size increase for A6000 headroom         | 45C   | 🟡       |
| 3   | Build dual-checkpoint rotation script                   | 45C   | 🟡       |
| 4   | Convert .npz rollout files to MP4 (when available)      | 45C   | 🟡       |
| 5   | Extract latent states from trained model                | 45D   | 🟡       |
| 6   | Analyze hierarchy abstraction mapping to concept tiers  | 45D   | 🟢       |
| 7   | Design custom cup environment (DM Control)              | 45E   | 🟢       |

## Deployment Requirements (New — Phase 45C)

For any future HIEROS deployment on Paperspace:
1. **Dedicated project** — one project per HIEROS instance, one notebook per project
2. **Clone to `/notebooks`** — not `/storage`, to prevent cross-project contamination
3. **Use `--no-deps` startup script** — every package pinned, every transitive dependency explicit
4. **Verify screen dimensions** — ensure `height, width = getScreenDims()` assignment is correct
5. **Run import verification** — numpy, jax, ale_py, atari.py must all import clean before training