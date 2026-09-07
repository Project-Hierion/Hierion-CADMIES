---
sop: Buttercup-Training-SOP
section: Prerequisites
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[05-03-Dependency-Manifest]]"
---

# 03 — Prerequisites

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The requirements documented
here reflect the state of knowledge during active development.

## Hardware

| Component | A4000 Deployment | A6000 Deployment |
|---|---|---|
| GPU | NVIDIA RTX A4000, 16 GB VRAM | NVIDIA RTX A6000, 48 GB VRAM |
| Platform | Paperspace Gradient Pro | Paperspace Gradient Pro |
| Template | PyTorch 2.1.1+cu121 | PyTorch 2.1.1+cu121 |
| Python | 3.11.7 | 3.11.7 |
| CUDA | 12.1 | 12.1 |

Both GPUs work. The A6000 provides 3× VRAM headroom for potential
batch size increases and hierarchy expansion.

## Paperspace Project Requirements

Per the three rules in [[02-Knowledge-Base]]:

1. Dedicated project per HIEROS instance
2. Single notebook in the project
3. Clone to `/notebooks/HIEROS`, never `/storage`

## Repository

| Item | Value |
|---|---|
| Source | https://github.com/Snagnar/HIEROS |
| License | MIT |
| Author | Paul Mattes |
| Clone location | /notebooks/HIEROS |

## Dependency Strategy

Every package installed with `--no-deps`. All transitive dependencies
explicitly pinned. The startup script is the manifest.

The full dependency manifest is in [[05-03-Dependency-Manifest]].

Key version decisions:

| Package | Version | Notes |
|---|---|---|
| jax / jaxlib | 0.4.30 | Pinned 0.4.16 unavailable on Python 3.11 |
| cloudpickle | 2.2.1 | Pinned 1.6.0 broken on Python 3.11 |
| ale-py | 0.8.0 | Replaces broken atari-py |
| numpy | 1.26.0 | pip wants to upgrade to 2.4.6 — do not allow |
| chex | excluded | Conflicts with jax 0.4.30 |

## Atari ROMs

Install via AutoROM:

```bash
autorom --accept-license
```

The ROMs are required for Atari environment training.

## Custom Atari Wrapper

The file embodied/envs/atari.py was rewritten to use ale-py's
ALEInterface directly, bypassing the deprecated gym.envs.atari
module.

Critical detail: getScreenDims() returns (height, width), not
(width, height). Verify this assignment before training.

See [[07-03-Screen-Dimension-Bug]] for the full story.

## Verification Checklist

Before training:

- [ ] Dedicated project, single notebook
- [ ] Repo cloned to /notebooks/HIEROS
- [ ] Startup script run with --no-deps installs
- [ ] numpy 1.26.0, jax 0.4.30, ale_py import clean
- [ ] Screen dimension assignment verified
- [ ] Rollout video verified after first checkpoint

## Related

- [[05-03-Dependency-Manifest]] — full package list
- [[04-01-Deploy-HIEROS]] — deployment procedure
- [[05-02-Batch-Size-Table]] — GPU configuration
