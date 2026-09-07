---
sop: Buttercup-Training-SOP
section: Procedures
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-02-Train-from-Scratch]], [[07-05-Checkpoint-Not-Saving]]"
---

# 04-03 — Resume from Checkpoint

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The procedure documented here
reflects the checkpoint method used during active development.

## When to Use

- After a Paperspace container restart
- After training was interrupted
- When continuing a previous training run

## Procedure

### Step 1: Run the startup script

```bash
bash /notebooks/HIEROS/startup.sh
```

### Step 2: Resume training from checkpoint

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
  --save_every 500 \
  --from_checkpoint /notebooks/HIEROS/logs/atari_breakout-YYYYMMDD-HHMMSS/checkpoint.ckpt
```

Replace the log directory timestamp with the actual training run.

## Critical Detail

--from_checkpoint requires the path to the checkpoint FILE, not the
log directory. Passing the directory results in IsADirectoryError.

The checkpoint file is named checkpoint.ckpt and is approximately
353 MB.

## Checkpoint Behavior

- Saved every 500 environment steps when --save_every 500 is set
- Contains full model state, optimizer state, and replay buffer
- Overwrites on each save — single checkpoint, most recent state
- Survives container restart on /notebooks
- Does NOT save on Ctrl+C — see [[07-05-Checkpoint-Not-Saving]]

## Verification

- [ ] Startup script completed
- [ ] Checkpoint file exists at the specified path
- [ ] Training resumes without errors
- [ ] Loss values continue from previous run
- [ ] First new checkpoint written after 500 steps

## Related

- [[07-05-Checkpoint-Not-Saving]] — the Ctrl+C lesson
- [[04-02-Train-from-Scratch]] — starting fresh
- [[05-01-Training-Commands]] — full command reference
