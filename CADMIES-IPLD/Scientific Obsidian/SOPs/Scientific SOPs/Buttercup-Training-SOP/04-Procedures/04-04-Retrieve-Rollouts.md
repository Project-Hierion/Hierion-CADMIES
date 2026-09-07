---
sop: Buttercup-Training-SOP
section: Procedures
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-02-Train-from-Scratch]], [[06-03-Ball-Bug]]"
---

# 04-04 — Retrieve Rollouts

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The procedure documented here
reflects the rollout retrieval method used during active development.

## When to Use

- To verify the training environment is correct
- To observe agent behavior during training
- To create video records of Buttercup's development

## Why This Matters

Rollout videos are the only reliable way to verify the environment is
correct. Metrics alone showed a healthy agent playing an empty game.
See [[06-03-Ball-Bug]].

## Procedure

### Step 1: Find the latest log directory

```bash
ls -d /notebooks/HIEROS/logs/atari_breakout-*/
```

The timestamp in the folder name indicates when the training run
started. Use the most recent directory.

### Step 2: Locate the replay files

```bash
ls /notebooks/HIEROS/logs/atari_breakout-YYYYMMDD-HHMMSS/train_eps/replay/
```

Replay files are .npz archives containing frame sequences. Each file
represents one episode.

### Step 3: Convert .npz to MP4

```bash
python -c "
import numpy as np, os, subprocess, tempfile
from PIL import Image

logdir = '/notebooks/HIEROS/logs/atari_breakout-YYYYMMDD-HHMMSS/'
replay_dir = logdir + 'train_eps/replay/'
files = sorted([f for f in os.listdir(replay_dir) if f.endswith('.npz')])

for i, f in enumerate(files):
    data = np.load(os.path.join(replay_dir, f))
    if 'image' not in data:
        continue

    frames = data['image']
    reward = data['reward'].sum()
    terms = data['is_terminal'].sum()
    timestamp = f[:15]
    outname = f'/notebooks/buttercup_rollout_{i+1}_{timestamp}.mp4'

    print(f'[{i+1}/{len(files)}] {timestamp} — {len(frames)} frames, reward={reward:.1f}, terminal={int(terms)}')

    with tempfile.TemporaryDirectory() as tmpdir:
        for j, frame in enumerate(frames):
            Image.fromarray(frame).save(f'{tmpdir}/frame_{j:04d}.png')
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error',
            '-framerate', '25', '-i', f'{tmpdir}/frame_%04d.png',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', outname
        ], check=True)

print(f'Done! {len(files)} videos in /notebooks/')
"
```

Replace the log directory timestamp with the actual training run.

### Step 4: Download the videos

Use the Paperspace file browser to navigate to /notebooks/ and
download each buttercup_rollout_*.mp4.

## Verification

- [ ] Latest log directory identified
- [ ] Replay files located
- [ ] MP4s generated without errors
- [ ] Frame count and reward printed for each video
- [ ] Videos downloaded and viewable

## What to Look For

For Breakout:

- The ball must appear and move
- The paddle must respond to actions
- Bricks must be present at the top
- Score must be capable of increasing

If the ball never appears, see [[07-04-Ball-Spawning-Bug]].

## Related
- [[06-03-Ball-Bug]] — why video verification is essential
- [[04-02-Train-from-Scratch]] — training procedure
- [[05-01-Training-Commands]] — command reference
