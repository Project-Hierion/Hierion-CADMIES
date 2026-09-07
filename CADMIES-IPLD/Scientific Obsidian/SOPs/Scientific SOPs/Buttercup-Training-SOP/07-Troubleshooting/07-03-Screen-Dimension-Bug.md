---
sop: Buttercup-Training-SOP
section: Troubleshooting
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-01-Deploy-HIEROS]], [[06-02-A6000-Redeploy]]"
---

# 07-03 — Screen Dimension Bug

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. This troubleshooting entry
documents the screen dimension bug encountered during active
development.

## Symptom

First launch on the A6000 failed:

ValueError: could not broadcast (210,160,3) into (160,210,3)


## Root Cause

`getScreenDims()` returns dimensions as `(height, width)`, not
`(width, height)`. The custom atari.py wrapper assigned the returned
values as width, height, creating a buffer of shape `(160, 210, 3)`.
The screen capture method returned `(210, 160, 3)`.

The mismatch caused the broadcast error.

## Why It Surfaced on A6000 and Not A4000

The first deployment used `getScreenRGB2()` which had different
dimension ordering. The ale-py migration in the custom wrapper changed
the return format to `getScreenRGB()`, introducing the mismatch.

The bug was present in the wrapper from the first deployment. It did
not trigger during the A4000 run.

## Fix

Swapped the variable assignment:

```python
height, width = self._ale.getScreenDims()
```

One line. The buffer shape then matched the screen capture output.

## Verification

After the fix, the second launch completed without errors. Model
compiled, training began.

## Related

- [[04-01-Deploy-HIEROS]] — deployment verification includes this check
- [[06-02-A6000-Redeploy]] — where the bug surfaced
- [[03-Prerequisites]] — verification checklist
