---
sop: Concept-Harvesting-SOP
section: References
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[05-03-Pipeline-Flow]]"
---

# 05-04 — Script Inventory

## Compilation Note

This SOP was compiled on 2026-09-07 from the script inventory
maintained in the CADMIES repository as of the August 2026 script
audit.

## Script Status Legend

| Status | Meaning |
|---|---|
| ACTIVE | Currently in use, required for pipeline |
| MAINTENANCE | Used occasionally, not part of core pipeline |
| DEPRECATED | Superseded or replaced, pending deletion |
| REFERENCE | Kept for documentation purposes only |

## Core Tools

| Script | Version | Status | Function |
|---|---|---|---|
| paths.py | 1.2.0 | ACTIVE | Centralized path management |
| cid_generator.py | 1.2.0 | ACTIVE | CID generation, blockstore save, index update |
| cbor_reader.py | 1.1.0 | ACTIVE | Reads concepts from blockstore |
| provenance_manager.py | 1.1.0 | ACTIVE | Provenance record creation and querying |
| verification_manager.py | 1.1.0 | ACTIVE | Four-tier verification system |
| scientific_validator.py | 1.1.0 | ACTIVE | Four-level validation before minting |
| car_utils.py | 1.1.0 | ACTIVE | CAR file read/write |
| orcid_stamper.py | 1.1.0 | MAINTENANCE | Public API ORCID verification |
| orcid_device_flow.py | 1.1.0 | MAINTENANCE | OAuth device flow ORCID verification |

## Pipeline Tools

| Script | Version | Status | Function |
|---|---|---|---|
| harvest_full_pipeline.py | 4.2.1 | ACTIVE | End-to-end harvester |
| generate_public_gateway.py | 3.2.1 | ACTIVE | Public website generation |
| generate_mycelium_map.py | 2.4.1 | ACTIVE | Interactive map generation |
| generate_relationships.py | 1.2.7 | ACTIVE | Relationship proposal via Codestral |
| export_to_car.py | 1.1.0 | ACTIVE | CAR export |
| import_from_car.py | 1.3.0 | ACTIVE | CAR import |
| import_from_github.py | 1.1.0 | MAINTENANCE | Remote CAR import |
| normalize_concept_schema.py | 1.1.0 | MAINTENANCE | Schema normalization |
| strip_all_orphans.py | 1.1.0 | MAINTENANCE | Orphan edge stripping |
| remint_existing_concepts.py | 2.0.1 | MAINTENANCE | Reminting changed concepts |
| enrich_concepts.py | 1.1.0 | MAINTENANCE | LLM concept enrichment |

## Legacy Scripts

| Script | Status | Notes |
|---|---|---|
| phase1_extract.py | MAINTENANCE | Superseded by harvest_full_pipeline.py |
| phase2_parse.py | MAINTENANCE | Superseded by harvest_full_pipeline.py |
| phase3_write.py | MAINTENANCE | Superseded by harvest_full_pipeline.py |
| extract_concepts.py | DEPRECATED | Pending deletion |

## Agent Scripts

| Script | Version | Status | Function |
|---|---|---|---|
| cadmies_concept_reader.py | 1.3.0 | ACTIVE | Willie — hybrid search and retrieval |
| philosophical_analyzer.py | 1.1.0 | ACTIVE | Pattern analysis, three depth levels |

## Audit Scripts

| Script | Version | Status | Function |
|---|---|---|---|
| scientific_audit.py | 1.1.0 | MAINTENANCE | Four-part system audit |

## Known Tension

`generate_relationships.py` write-mode mutates blocks in place without
new CIDs. Flagged during the August 2026 audit. Architectural decision
needed.

## Related

- [[05-03-Pipeline-Flow]] — how the scripts connect
- [[04-Procedures]] — how to use the scripts
