## Step 1: Start the machine

## Step 2: Run the startup script

```
bash /notebooks/HIEROS/startup.sh
```

## Step 3: Pull required models

```
ollama pull mistral:7b
```
```
ollama pull tinyllama:latest
```
```
ollama pull codestral:22b
```

## Step 4: Chat directly with a model (optional)

```
ollama run mistral:7b
```

## Launch Training

From scratch:

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

Resume from checkpoint:

```
cd /notebooks/HIEROS  
python hieros/train.py  
--configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs  
--max_hierarchy 2  
--subgoal_visualization True  
--dynamics_model s5  
--task atari_breakout  
--tensorboard_logging True  
--wandb_logging False  
--batch_size 16  
--batch_length 64  
--save_every 500  
--from_checkpoint /notebooks/HIEROS/logs/atari_breakout-20260531-031943/checkpoint.ckpt
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