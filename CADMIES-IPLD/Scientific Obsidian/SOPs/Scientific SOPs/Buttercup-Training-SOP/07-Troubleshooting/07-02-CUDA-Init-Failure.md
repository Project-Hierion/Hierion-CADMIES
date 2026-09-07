---
sop: Buttercup-Training-SOP
section: Troubleshooting
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[04-01-Deploy-HIEROS]]"
---

# 07-02 — CUDA Init Failure

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This troubleshooting entry
documents CUDA initialization issues encountered during active
development.

## Symptom

HIEROS deployed in a Paperspace project shared with other notebooks
produced:

RuntimeError: No CUDA GPUs are available


The error occurred even though `nvidia-smi` showed the GPU and
PyTorch could see it.

## What Was Tried

A rename attempt — cloning HIEROS into a shared project and naming it
"Buttercup" — resulted in the CUDA initialization failure. The shared
project had two other CADMIES notebooks.

## Resolution

Dedicated project with a single notebook. The CUDA failure did not
recur after deployment to an isolated project.

The root cause was not definitively determined. Import path conflicts
or environment variable contamination from other notebooks in the
shared project were noted as possible factors, but no causal
determination was made.

## The Rule

One HIEROS instance = one Paperspace project = one notebook.

This is Rule 1 in [[02-Knowledge-Base]].

## Related

- [[02-Knowledge-Base]] — the three rules
- [[04-01-Deploy-HIEROS]] — deployment procedure
- [[06-02-A6000-Redeploy]] — the isolated redeploy that worked
