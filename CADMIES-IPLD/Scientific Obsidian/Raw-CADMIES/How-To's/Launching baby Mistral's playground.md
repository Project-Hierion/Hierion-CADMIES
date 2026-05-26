ALWAYS MAKE SURE GPU is selected, NOT CPU
Run machine
Open terminal

```
cd /storage/HIEROS && bash startup.sh
```

```
python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_breakout --tensorboard_logging True --wandb_logging False --batch_size 16 --batch_length 32 --save_every 500 --from_checkpoint /storage/HIEROS/logs/atari_breakout-20260525-025214/checkpoint.ckpt
```

