# CADMIES Changelog

## 2026-05-26 — Session 022
- **generate_public_gateway.py v2.0.1:** Fixed OUTPUT_DIR from `public_concepts_gateway/` to `../docs/`. Updated SITE_URL. Deploy message corrected.
- **harvest_full_pipeline.py v4.2.2:** Added prose-stripping before JSON parse (strip everything before first `{`). Reduced chunk size from 1000 to 750 words. Removed broken apostrophe escape regex. Added missing comma fix between JSON array elements. Mycelium search import fixed (`llm_mycelium_reader` → `cadmies_concept_reader`).
- **car_utils.py v1.0.3:** Added `read_car_index()` function to extract human_id → CID mapping from CAR files.
- **Moved `harvest/` into `tools/harvest/`.** Updated PROJECT_ROOT path in harvest_full_pipeline.py. Updated GUI and startup.sh references.

## 2026-05-25 — Session 021
- **import_from_car.py v1.2.0:** Automatic index update on every block save during CAR import. No more manual index rebuild required.
- **import_from_car.py v1.1.0:** CID change on import now preserves provenance. Original CAR CID and import date stored in extra_fields. 103 blocks reminted with provenance.
- **car_utils.py v1.0.2:** Moved from `tools/` to `tools/core/`. Updated imports in export_to_car.py and import_from_car.py.
- **startup.sh v2.0:** Hardened for bare Paperspace machines. Now installs Ollama, Python packages (`ollama`, `dag_cbor`, `multiformats`), pulls Mistral. 5 steps.
- **generate_mycelium_map.py:** Added 15+ unmapped domains to DOMAIN_UPWARD_MAP. Map legend clean.
- **Merged 4 case-variant duplicates** (Asian_Depth, Asian_Philosophical_Deep, Eternal_Evolution, Interconnectedness_of_Life → lowercase canonicals).
- **Enriched 3 concepts** with missing difficulty levels (dna_human_chromosome_1_reference, human_genome_project_overview, pcr_polymerase_chain_reaction).
- **Codestral audit:** 337 source concepts reviewed, zero structural issues remaining.

## 2026-05-24 — Session 020
- **harvest_full_pipeline.py v4.1.0:** Three-tier difficulty levels (beginner/intermediate/expert).
- **generate_relationships.py v1.2.4:** Orphan prevention gate active. 92 edges generated, zero orphans.
- **strip_all_orphans.py:** Created for orphan edge resolution.
- **CAR export/import pipeline proven:** 342 concepts exported, imported, verified.
- **CAR import verification:** 153 CID mismatches documented (HOG-era artifacts + code alignment discrepancy).
- **remint_existing_concepts.py v2.0.0:** 153 HOG-era blocks reminted with proper CIDv1.
- **GitHub Release v0.5.0:** "The Happy Little Accidents" — first CAR distribution published.