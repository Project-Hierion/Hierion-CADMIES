---
sop: Concept-Harvesting-SOP
section: Troubleshooting
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-05-Sync-Nodes]]"
---

# 07-04 — Sync Issues

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
maintained in the CADMIES repository. This troubleshooting entry
documents sync failure modes observed during active development.

## Symptom

Nodes fall out of sync. GitHub, Paperspace, the droplet, and local
machines do not have the same concepts.

## Possible Causes

1. Git push failed
2. Git pull not run
3. CAR import not completed
4. Droplet auto-pull failed

## Diagnostic Steps

### Step 1: Check git status

```bash
cd /notebooks/CADMIES/CADMIES-IPLD
git status
```

### Step 2: Check remote

```bash
git log --oneline -5
```

### Step 3: Verify blockstore

Compare concept counts across nodes.

### Step 4: Check CAR import logs

If using CAR sync, verify the import completed without errors.

## Resolution

## Git sync

```bash
git add -A
git commit -m "Sync: description"
git pull --rebase
git push origin main
```

## CAR sync

```bash
python tools/import_from_car.py incoming_cars/cadmies_latest.car
python tools/generate_mycelium_map.py
python tools/generate_public_gateway.py
```

## Related
- [[04-05-Sync-Nodes]] — sync procedure
- [[05-02-Workflow-Commands]] — workflow reference
