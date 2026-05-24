Here are the steps to retrieve Buttercup's training videos from the Paperspace Snagnar project:

**Step 1: Find the latest .npz replay files**

bash

ls /storage/HIEROS/logs/atari_breakout-*/train_eps/replay/

Use the most recent log directory. The timestamp in the folder name (e.g., `20260521-191612`) tells you when the training run started.

**Step 2: Convert .npz to MP4**

bash

python -c "
import numpy as np, os, subprocess, tempfile
from PIL import Image
replay_dir = '/storage/HIEROS/logs/atari_breakout-20260521-191612/train_eps/replay/'
files = sorted([f for f in os.listdir(replay_dir) if f.endswith('.npz')])
for i, f in enumerate(files):
    timestamp = f[:15]
    outname = f'/notebooks/buttercup_rollout_{i+1}_{timestamp}.mp4'
    
    data = np.load(os.path.join(replay_dir, f))
    frames = data['image']
    reward = data['reward'].sum()
    terms = data['is_terminal'].sum()
    
    print(f'[{i+1}/{len(files)}] {timestamp} — {len(frames)} frames, reward={reward:.1f}, lives lost={int(terms)}')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for j, frame in enumerate(frames):
            img = Image.fromarray(frame)
            img.save(f'{tmpdir}/frame_{j:04d}.png')
        
        subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'error',
            '-framerate', '25', '-i', f'{tmpdir}/frame_%04d.png',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', outname
        ], check=True)
print('\nDone! Videos in /notebooks/')
"

**Step 3: Download the MP4s**

Use the Paperspace file browser → navigate to `/notebooks/` → download each `buttercup_rollout_*.mp4`.

**Step 4: Store in the vault**

Place the downloaded videos in:

text

Scientific Obsidian/Baby-Mistral-(Buttercup)-Rollouts/

They'll be viewable in Obsidian and on GitHub via "View raw."

**Step 5: Check for new rollouts after continued training**

If Buttercup has been training longer, check for newer log directories:

bash

ls -d /storage/HIEROS/logs/atari_breakout-*/

Newer directories will have additional .npz files with more recent gameplay.