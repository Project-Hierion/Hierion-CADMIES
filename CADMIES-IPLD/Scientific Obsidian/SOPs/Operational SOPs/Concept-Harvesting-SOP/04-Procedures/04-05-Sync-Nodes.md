---
sop: Concept-Harvesting-SOP
section: Procedures
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-04-Generate-Outputs]], [[07-04-Sync-Issues]]"
---

# 04-05 — Sync Nodes

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
procedure documented here reflects the pipeline as of the August 2026
script audit.

## When to Use

After harvesting and generating outputs. These steps propagate the
mycelium across all nodes.

## Node Responsibilities

| Node | Role |
|---|---|
| Paperspace (GPU) | Harvest, extraction, relationship generation |
| Droplet | Public gateway, blockstore |
| GitHub | Source of truth, version control |
| Local | Backup, local access, development |

## Procedure — Paperspace to GitHub

### Step 1: Commit and push

```bash
cd /notebooks/CADMIES/CADMIES-IPLD
git add -A
git commit -m "Session XXX: description of changes"
git push origin main
```

## Procedure — GitHub to Local

### Step 2: Pull on local

```bash
cd /path/to/local/CADMIES/CADMIES-IPLD && source venv/bin/activate
git pull origin main
```

## Procedure — Droplet

The droplet auto-pulls from GitHub via cron. No manual step needed.
The public gateway updates automatically.

## Procedure — CAR Import

When syncing via CAR files instead of git:

## Export on Paperspace

```bash
python tools/export_to_car.py --all --output cadmies_latest.car
```

## Download to target machine

Place the CAR file in incoming_cars/.

## Import on target machine

```bash
python tools/import_from_car.py incoming_cars/cadmies_latest.car
python tools/generate_mycelium_map.py
python tools/generate_public_gateway.py
```

## Verification

- [ ] Git push successful
- [ ] Local pull successful
- [ ] Droplet auto-pull confirmed
- [ ] Public gateway reflects new concepts

##Related

- [[04-04-Generate-Outputs]] — outputs before sync
- [[07-04-Sync-Issues]] — troubleshooting
- [[05-02-Workflow-Commands]] — full workflow reference
