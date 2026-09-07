---
sop: Buttercup-Training-SOP
section: Troubleshooting
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-01-Deploy-HIEROS]], [[05-03-Dependency-Manifest]]"
---

# 07-01 — Dependency Hell

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This troubleshooting entry
documents dependency issues encountered during active development.

## Symptom

The HIEROS `requirements.txt` pinned packages to versions unavailable
or broken on Python 3.11. Installation failed or produced runtime
errors.

## Root Causes

Specific version incompatibilities:

| Package | Pinned Version | Issue |
|---|---|---|
| jax / jaxlib | 0.4.16 | jaxlib 0.4.16 unavailable on PyPI for Python 3.11 |
| cloudpickle | 1.6.0 | Bytecode incompatibility with Python 3.11 |
| atari-py | unspecified | Build failure — wheel tag unsupported on Python 3.11 |
| chex | 0.1.91 | Conflicts with jax 0.4.30 (requires jax>=0.7.0) |

Additional missing packages identified through iterative import
errors: ruamel.yaml, rich, einops, lovely-tensors, lovely-numpy,
dm_control, mujoco.

## Resolution

Version substitutions:

| Original Pin | Resolution |
|---|---|
| jax==0.4.16 | jax==0.4.30, jaxlib==0.4.30 |
| cloudpickle==1.6.0 | cloudpickle==2.2.1 |
| atari-py | ale-py==0.8.0 + autorom |
| chex==0.1.91 | Removed entirely — testing library, not needed for training |

## The --no-deps Strategy

The deeper issue was pip's dependency resolver silently upgrading
pinned packages during transitive dependency resolution. Example:
numpy 1.26.0 upgraded to 2.4.6 because jax said "numpy>=1.22."

Resolution: every package installed with `--no-deps`, every transitive
dependency explicitly pinned. The startup script is a manifest, not a
suggestion.

## Full Resolution

See [[05-03-Dependency-Manifest]] for the complete verified working
package list.

## Related

- [[04-01-Deploy-HIEROS]] — deployment procedure
- [[05-03-Dependency-Manifest]] — the full manifest
- [[03-Prerequisites]] — dependency strategy overview
