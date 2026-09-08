---
sop: Concept-Harvesting-SOP
section: References
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-Procedures]]"
---

# 05-02 — Workflow Commands

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
workflows documented here reflect the pipeline as of the August 2026
script audit.

## Workflow 1: Full Harvest Pipeline

```text
conversation.json → Harvester → source_concepts/ → Validate → Mint → Blockstore → Relationships → Map → Gateway
```

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
python tools/generate_mycelium_map.py
python tools/generate_public_gateway.py
python tools/export_to_car.py --all --output cadmies_latest.car
git add -A && git commit -m "Harvest: description of changes" && git push origin main
```

## Workflow 2: External Source Harvest

For published work requiring citation. Fill metadata in
conversation.json. The harvester injects metadata into proofs.

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
```

## Workflow 3: CAR Import and Sync

```text
Paperspace → export_to_car.py → cadmies_latest.car → import_from_car.py → Blockstore updated
```

```bash
python tools/export_to_car.py --all --output cadmies_latest.car
python tools/import_from_car.py incoming_cars/cadmies_latest.car
python tools/generate_mycelium_map.py
python tools/generate_public_gateway.py
```

## Workflow 4: Quality Control

```bash
python tools/remint_existing_concepts.py --apply
python tools/generate_mycelium_map.py
python audits/scientific_audit.py
python tools/strip_all_orphans.py --apply
python tools/export_to_car.py --all --output cadmies_latest.car
```

## Workflow 5: Concept Enrichment

```bash
python tools/enrich_concepts.py
python tools/enrich_concepts.py --concept=entropy
python tools/enrich_concepts.py --dry-run
```

## Workflow 6: ORCID Verification

```bash
python tools/core/orcid_device_flow.py <concept_cid>
python tools/core/orcid_stamper.py <concept_cid> <orcid_id>
python tools/core/verification_manager.py --status <concept_cid>
```

## Workflow 7: Session Sync

```bash
cd /notebooks/CADMIES/CADMIES-IPLD
git add -A
git commit -m "Session XXX: description of changes"
git push origin main
```

## Related
- [[04-Procedures]] — detailed procedures for each workflow
- [[05-04-Script-Inventory]] — script details
