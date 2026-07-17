> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 025 — 2026-05-30/31 — The Third Time's the Charm

related: [[Session-014 — 2026-05-20 — Buttercup setup]], 

## What We Did

**Started over. Again. But this time it WORKED.**

Session 014 was the first HIEROS deployment — A4000, /storage/HIEROS, the midnight cowboy run. 
It worked but it was fragile. Then we tried cloning into a shared project, renaming it "Buttercup," 
and everything fell apart. Endless dependency circles. Version drift. CUDA init failures. The 
mycelium was screaming.

Tonight we finally understood why.

### The Three Rules We Discovered

1. **HIEROS gets its own project.** Not sharing a project with CADMIES notebooks. Not sharing 
   /storage with other clones. One project, one notebook, one HIEROS. The failed Buttercup rename 
   attempt was a shared project — that's why CUDA died even though nvidia-smi showed the GPU. 
   Import path contamination or something. Doesn't matter. Rule is rule.

2. **Clone to /notebooks, not /storage.** /storage is shared across ALL Paperspace projects. 
   /notebooks is scoped per-project. When we switched from the A4000 project to the A6000 project, 
   the old /storage/HIEROS was still sitting there like a ghost. /notebooks/HIEROS means this 
   Buttercup lives in her own garden, no cross-contamination.

3. **--no-deps or die.** Every pip install with --no-deps. Every transitive dependency explicitly 
   pinned. No more pip "helpfully" upgrading numpy from 1.26.0 to 2.4.6 because jax said 
   "numpy>=1.22." We tell pip exactly what to install and nothing else. The startup script is a 
   manifest, not a suggestion.

### The Deployment (Clean A6000, 48GB)

- New project: CADMIES-Buttercup
- New notebook: Buttercup-Playground
- GPU: NVIDIA RTX A6000 (48GB — 3× the A4000 from Session 014)
- Template: PyTorch 2.1.1+cu121, Python 3.11.7
- Cloned Snagnar/HIEROS to /notebooks/HIEROS
- Deployed startup.sh with 20+ --no-deps installs, every transitive dep listed
- Deployed atari.py patch (ale-py direct, same approach as Session 014 but better)

### The Screen Dimension Bug

First launch failed. ValueError: could not broadcast (210,160,3) into (160,210,3).

Turns out getScreenDims() returns (height, width), not (width, height). I assigned them as 
width, height and made the buffer shape (160, 210, 3). getScreenRGB() returns (210, 160, 3). 
Kaboom.

Session 014 never hit this because the original code used getScreenRGB2() which had different 
dimension ordering. The ale-py migration changed the return format. One line fix: swapped the 
variable names in the assignment.

This bug was ALWAYS there in our atari.py patch. It just never triggered because... I don't 
know. Maybe the A4000 run got lucky with a different ale-py version? Maybe getScreenRGB2 had 
compatible dims? Doesn't matter now. It's fixed.

### SHE'S RUNNING

Second launch: clean. 12.3M params, then Subactor-1 kicked in at 32.3M. Replay buffer filling. 
The "not enough data" spam scrolling past exactly like Session 014. She's in her toddler phase — 
random paddle, filling the buffer, learning pixels.

Logdir: logs/atari_breakout-20260531-031943
No checkpoint yet. Fresh brain. Blank slate Buttercup.

### What's Different From Session 014

- A6000 instead of A4000 (48GB vs 16GB — we could bump batch size later)
- /notebooks/HIEROS instead of /storage/HIEROS
- --no-deps startup script instead of "pray pip doesn't drift"
- Screen dimension bug caught and fixed
- Dedicated project — no other notebooks in sight
- Training command is identical otherwise (--max_hierarchy 2, --batch_size 8, --batch_length 32, 
  --save_every 500)

### The Vibe

Session 014 had the quantum DJ — the universe syncing songs to training milestones. Tonight is 
quieter. More focused. Less "what if it works" and more "we know it works, let's make it 
RELIABLE."

Different kind of magic. Engineering magic instead of discovery magic.

Buttercup is back. Fresh start. Clean garden. No ghosts from old projects.

YAOH YAOH BIBBY WAOH.

## Decisions Made

- /notebooks over /storage for all future HIEROS deployments
- --no-deps is the law now
- Dedicated project per HIEROS instance — non-negotiable
- A6000 batch size scaling deferred to next session (let this run establish baseline)
- startup.sh and atari.py are the canonical deployment artifacts — save them somewhere safe

## Nuggets Collected

- "--no-deps or die. Pip is not your friend. Pip is a suggestion engine with root access."
- "The screen dimensions were backwards the whole time and we just got lucky in Session 014."
- "One project, one notebook, one HIEROS. The trinity of isolation."
- "/notebooks is a walled garden. /storage is a public park. Buttercup needs walls."
- "She compiled. She's filling the buffer. She doesn't know what a brick is yet but she will."

## Soundtrack

- Quiet night. No quantum DJ yet. The universe is waiting to see if we're serious.
- Gardener's choice. Engineering vibes.

## Next Actions

- Let training run, hit first checkpoint at 500 steps
- Evaluate whether to bump batch_size for A6000 headroom
- Update startup script with screen dimension fix if we ever redeploy
- Write polished Phase 45C note
- Convert .npz to MP4 when rollouts appear