
## Step 1: Start the machine


## Step 2: Run the startup script
```
bash /notebooks/HIEROS/startup.sh
```

## Step: 3 Launch Training

Resume from checkpoint for **Space Invaders**:
```
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_space_invaders --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_space_invaders-20260624-012126/checkpoint.ckpt
```

Resume from checkpoint for **Boxing**:
```
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_boxing --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_boxing-0260623-200024/checkpoint.ckpt
```

Resume from checkpoint for **Qbert**:
```
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_qbert --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_qbert-20260620-030255/checkpoint.ckpt
```

Resume from checkpoint for **Pong**:
```
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_pong --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_pong-20260619-010949/checkpoint.ckpt
```

Resume from checkpoint for **Breakout**:
```
cd /notebooks/HIEROS && python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_breakout --tensorboard_logging True --wandb_logging False --batch_size 8 --batch_length 32 --save_every 500 --from_checkpoint /notebooks/HIEROS/logs/atari_breakout-20260605-011153/checkpoint.ckpt
```

From **scratch**:

```
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

## Batch Size Settings by GPU

|GPU|VRAM|batch_size|batch_length|Notes|
|---|---|---|---|---|
|A4000|16GB|16|64|Paper default. Works.|
|A6000|48GB|16|64|Paper default. 7+ FPS. Stable.|

## Retrieve Rollout Videos

# Find latest log directory
ls -d /storage/HIEROS/logs/atari_breakout-*/
# Convert .npz replays to MP4
python -c "
import numpy as np, os, subprocess, tempfile
from PIL import Image
logdir = '/storage/HIEROS/logs/atari_breakout-YYYYMMDD-HHMMSS/'
replay_dir = logdir + 'train_eps/replay/'
files = sorted([f for f in os.listdir(replay_dir) if f.endswith('.npz')])
count = 0
for f in files:
    data = np.load(os.path.join(replay_dir, f))
    if 'image' not in data:
        continue
    count += 1
    timestamp = f[:15]
    outname = f'/notebooks/buttercup_rollout_{count}_{timestamp}.mp4'
    frames = data['image']
    reward = data['reward'].sum()
    terms = data['is_terminal'].sum()
    print(f'[{count}] {timestamp} - {len(frames)} frames, reward={reward:.1f}, terminal={int(terms)}')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for j, frame in enumerate(frames):
            Image.fromarray(frame).save(f'{tmpdir}/frame_{j:04d}.png')
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error',
            '-framerate', '25', '-i', f'{tmpdir}/frame_%04d.png',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', outname
        ], check=True)
print(f'\nDone! {count} videos in /notebooks/')
"

Download: Paperspace file browser → /notebooks/ → download buttercup_rollout_*.mp4