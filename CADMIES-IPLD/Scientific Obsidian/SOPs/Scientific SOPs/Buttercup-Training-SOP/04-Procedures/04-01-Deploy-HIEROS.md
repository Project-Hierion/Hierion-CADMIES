---
sop: Buttercup-Training-SOP
section: Procedures
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[03-Prerequisites]]"
---

# 04-01 — Deploy HIEROS

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The procedure documented here
reflects the deployment method used during active development.

## When to Use

- First time deploying HIEROS
- After a Paperspace container restart
- When building a fresh Buttercup training environment

## Procedure

### Step 1: Create a dedicated Paperspace project

Create a new project with a single notebook. Do not add other
notebooks. Do not share with other CADMIES work.

The isolation rule is non-negotiable. See [[07-02-CUDA-Init-Failure]]
for what happens when it's violated.

### Step 2: Clone HIEROS to /notebooks

```bash
git clone https://github.com/Snagnar/HIEROS.git /notebooks/HIEROS
```

Clone to /notebooks, never /storage. /storage is shared across
all projects. /notebooks is scoped per-project.

### Step 3: Run the startup script
```bash
bash /notebooks/HIEROS/startup.sh
```

The startup script installs every package with --no-deps, with all
transitive dependencies pinned. It is idempotent — safe to run on any
fresh container.

See [[05-03-Dependency-Manifest]] for the full package list.

### Step 4: Verify imports
```bash
python -c "import numpy; print(numpy.__version__)"
python -c "import jax; print(jax.__version__)"
python -c "import ale_py; print('ale_py OK')"
```

Expected versions:

numpy: 1.26.0

jax: 0.4.30

ale_py: import succeeds

### Step 5: Verify the screen dimension assignment

Open embodied/envs/atari.py and verify:

```python
height, width = self._ale.getScreenDims()
```

The order matters. getScreenDims() returns (height, width), not
(width, height). See [[07-03-Screen-Dimension-Bug]].

### Step 6: Verify GPU availability
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Must print True.

### Step 7: Dry run

Run a short training test to confirm the environment works:

```bash
cd /notebooks/HIEROS && python hieros/train.py \
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

Let it run for a few hundred steps. Confirm no crashes.

### Step 8: Verify with rollout video

After the first checkpoint, retrieve a rollout video and confirm the
environment is correct. The ball must appear in Breakout. Paddle must
move. Game must play.

This step is critical. See [[06-03-Ball-Bug]] for what happens when
it's skipped.

## Verification

- [ ] Dedicated project, single notebook
- [ ] Repo cloned to /notebooks/HIEROS
- [ ] All imports clean with correct versions
- [ ] Screen dimensions verified
- [ ] GPU available
- [ ] Dry run completed without crashes
- [ ] Rollout video shows correct environment

## Related

- [[02-Knowledge-Base]] — the three rules
- [[05-03-Dependency-Manifest]] — dependency details
- [[04-02-Train-from-Scratch]] — next step
