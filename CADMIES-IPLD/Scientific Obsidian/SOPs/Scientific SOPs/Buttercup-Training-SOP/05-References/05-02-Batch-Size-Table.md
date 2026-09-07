---
sop: Buttercup-Training-SOP
section: References
date: 2026-09-07
status: HISTORICAL
related: "[[SOP Landing]], [[04-02-Train-from-Scratch]], [[03-Prerequisites]]"
---

# 05-02 — Batch Size Table

## Compilation Note

This SOP was compiled on 2026-09-07 from working notes and session
records spanning May through June 2026. The settings documented here
reflect the configurations used during active development.

## GPU Settings

| GPU | VRAM | batch_size | batch_length | Notes |
|---|---|---|---|---|
| A4000 | 16GB | 8 | 32 | Working config. 3 hierarchy levels OOM. |
| A6000 | 48GB | 16 | 64 | Headroom for larger batches. |

## Configuration Details

### A4000 (16GB)

The original deployment GPU. The working configuration:

- `--batch_size 8`
- `--batch_length 32`
- `--max_hierarchy 2`

Three hierarchy levels exceeded VRAM (53M parameters). Two levels
(32M parameters) fit comfortably.

### A6000 (48GB)

The redeployment GPU. Three times the VRAM of the A4000. The initial
run used the same conservative settings as A4000 to establish a
baseline.

Potential optimizations for the A6000:

- Increase `--batch_size` from 8 to 16 or 24
- Increase `--batch_length` from 32 to 64
- Potentially enable `--max_hierarchy 3` (was OOM on A4000)

These optimizations were deferred to future sessions. The baseline
was established first.

## Memory Relationship

| Hierarchy Level | Parameters |
|---|---|
| 2 levels | 32,279,645 |
| 3 levels | 53M+ (OOM on A4000) |

The model grows as hierarchy levels are added during training:
- Subactor-0 only: 12,307,361 parameters
- Subactor-1 added: 32,279,645 parameters

## Related

- [[04-02-Train-from-Scratch]] — training procedure
- [[05-01-Training-Commands]] — full commands
- [[03-Prerequisites]] — hardware requirements
