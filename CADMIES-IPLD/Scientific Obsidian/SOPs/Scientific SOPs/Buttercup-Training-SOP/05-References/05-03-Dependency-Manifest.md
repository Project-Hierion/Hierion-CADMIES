---
sop: Buttercup-Training-SOP
section: References
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-01-Deploy-HIEROS]], [[07-01-Dependency-Hell]]"
---

# 05-03 — Dependency Manifest

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The manifest documented here
reflects the verified working dependency set during active development.

## The --no-deps Strategy

Every package installed with `--no-deps`. Every transitive dependency
explicitly pinned. The startup script is a manifest, not a suggestion.

## Full Dependency Manifest

Core:

```text
jax==0.4.30
jaxlib==0.4.30
numpy==1.26.0
scipy==1.11.2
opt-einsum==3.3.0
ml-dtypes==0.2.0
einops==0.6.1
optax==0.1.7
cloudpickle==2.2.1
```

Environments:

```text
gym==0.23.0
ale-py==0.8.0
dm_control==1.0.14
mujoco==3.9.0
gym-notices==0.1.0
dm-env==1.6
dm-tree==0.1.10
glfw==2.10.0
labmaze==1.0.6
pyopengl==3.1.10
importlib-resources==7.1.0
```

Atari:

```text
autorom==0.6.1
```

Utilities:

```
crafter==1.8.1
ruamel.yaml==0.17.33
rich==13.5.3
opensimplex==0.4.5.1
ruamel.yaml.clib==0.2.15
markdown-it-py==4.2.0
mdurl==0.1.2
```

Display and Logging:

```text
tensorboard==2.14.1
lovely-tensors==0.1.15
lovely-numpy==0.2.9
fastcore==1.13.2
```

Video and Image:

```text
opencv-python==4.8.1.78
moviepy==1.0.3
decorator==4.4.2
imageio-ffmpeg==0.6.0
proglog==0.1.12
```

Misc:

```text
tqdm==4.66.1
```

## Explicitly Excluded

| Package | Reason |
|---|---|
| chex | Conflicts with jax 0.4.30 (requires jax>=0.7.0) |
| atari-py | Dead package, replaced by ale-py + autorom |
| dm-sonnet | Not needed for training |
| wandb | Logging disabled |
| zmq | Broken version pin in requirements.txt |
| black | Dev tool only |

## Version Substitutions

The HIEROS requirements.txt pins several packages to versions
unavailable or broken on Python 3.11:

| Original Pin | Issue | Resolution |
|---|---|---|
| jax==0.4.16 | jaxlib 0.4.16 unavailable for Python 3.11 | jax==0.4.30 |
| cloudpickle==1.6.0 | Bytecode incompatibility with Python 3.11 | cloudpickle==2.2.1 |
| atari-py | Build failure on Python 3.11 | ale-py==0.8.0 + autorom |

## Related
- [[04-01-Deploy-HIEROS]] — deployment procedure
- [[07-01-Dependency-Hell]] — the version conflict battles
- [[03-Prerequisites]] — requirements overview
