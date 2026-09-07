---
sop: Buttercup-Training-SOP
section: References
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-02-Train-from-Scratch]], [[04-03-Resume-from-Checkpoint]]"
---

# 05-01 — Training Commands

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The commands documented here
reflect the training configurations used during active development.

## Resume from Checkpoint — All Games

### Enduro

```bash
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_enduro --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_enduro-20260628-213411/checkpoint.ckpt
```

### Space Invaders

```bash
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_space_invaders --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_space_invaders-20260624-012126/checkpoint.ckpt
```

### Boxing

```bash
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_boxing --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_boxing-0260623-200024/checkpoint.ckpt
```

### Q*bert

```bash
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_qbert --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_qbert-20260620-030255/checkpoint.ckpt
```

### Pong

```bash
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_pong --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_pong-20260619-010949/checkpoint.ckpt
```

### Breakout

```bash
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_breakout --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_breakout-20260605-011153/checkpoint.ckpt
```

### Train from Scratch
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

Replace atari_breakout with the target game.

## Available Tasks

From the HIEROS README, the available Atari tasks are:

atari_alien, atari_amidar, atari_assault, atari_asterix,
atari_bank_heist, atari_battle_zone, atari_boxing, atari_breakout,
atari_chopper_command, atari_crazy_climber, atari_demon_attack,
atari_freeway, atari_frostbite, atari_gopher, atari_hero,
atari_jamesbond, atari_kangaroo, atari_krull, atari_kung_fu_master,
atari_ms_pacman, atari_pong, atari_private_eye, atari_qbert,
atari_road_runner, atari_seaquest

## Related
- [[04-02-Train-from-Scratch]] — training procedure
- [[04-03-Resume-from-Checkpoint]] — checkpoint resume
- [[05-02-Batch-Size-Table]] — GPU settings
