---
sop: Concept-Harvesting-SOP
section: Procedures
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-03-Review-and-Mint]], [[05-02-Workflow-Commands]]"
---

# 04-04 — Generate Outputs

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
procedure documented here reflects the pipeline as of the August 2026
script audit.

## When to Use

After concepts are minted. These commands generate the public-facing
outputs and backup files.

## Procedure

### Step 1: Generate the mycelium map

```bash
python tools/generate_mycelium_map.py
```

Produces the interactive Cytoscape.js map. Current version: v2.4.1.

### Step 2: Generate the public gateway

```bash
python tools/generate_public_gateway.py
```

Produces the public website — concept cards, search, translate.js,
ORCID badges, JSON-LD, sitemap. Current version: v3.2.1.

### Step 3: Export backup CAR

```bash
python tools/export_to_car.py --all --output cadmies_latest.car
```

Exports all concepts with provenance to a CAR file for sharing and
backup.

## Output Summary

| Command | Output |
|---|---|
| generate_mycelium_map.py | mycelium_map.html |
| generate_public_gateway.py | docs/index.html, docs/concepts.json, docs/sitemap.xml |
| export_to_car.py | cadmies_latest.car |

## Verification

- [ ] Map generated without errors
- [ ] Gateway generated with current concepts
- [ ] CAR export completed

## Related
- [[04-05-Sync-Nodes]] — pushing outputs to other nodes
- [[05-02-Workflow-Commands]] — full workflow reference
- [[05-04-Script-Inventory]] — script details
