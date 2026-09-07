---
sop: Buttercup-Training-SOP
section: Troubleshooting
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-03-Resume-from-Checkpoint]], [[06-01-First-Deployment]]"
---

# 07-05 — Checkpoint Not Saving

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This troubleshooting entry
documents checkpoint behavior discovered during active development.

## Symptom

Ctrl+C during training did not save a checkpoint. The first 4,100
steps of training were lost when the notebook was stopped.

## Cause

HIEROS saves checkpoints on scheduled intervals, not on interrupt.
Ctrl+C does not trigger a checkpoint save.

## Resolution

Use `--save_every 500` in the training command:

```bash
--save_every 500
```

This writes a checkpoint every 500 environment steps.

## Checkpoint Details

| Property | Value |
|---|---|
| File name | checkpoint.ckpt |
| Size | ~353 MB |
| Contents | Model state, optimizer state, replay buffer |
| Save behavior | Overwrites on each save — single checkpoint |
| Persistence | Survives container restart |

## Resume Detail
--from_checkpoint requires the path to the checkpoint FILE, not the
log directory. Passing the directory results in IsADirectoryError.

Correct:

```bash
--from_checkpoint /notebooks/HIEROS/logs/atari_breakout-YYYYMMDD-HHMMSS/checkpoint.ckpt
```

Incorrect:

```bash
--from_checkpoint /notebooks/HIEROS/logs/atari_breakout-YYYYMMDD-HHMMSS/
```

## Future Enhancement

A dual-checkpoint rotation system (checkpoint_A.ckpt /
checkpoint_B.ckpt) was identified as a potential improvement to
provide redundancy against corruption during save operations.

## Related
- [[04-03-Resume-from-Checkpoint]] — resume procedure
- [[06-01-First-Deployment]] — where the lesson was learned
- [[02-Knowledge-Base]] — checkpoint behavior summary
