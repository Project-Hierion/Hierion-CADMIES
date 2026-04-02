# Source Concepts Directory

This directory contains human-readable JSON source files for concepts stored in CADMIES-IPLD.

## Purpose
- Keep editable source files for concepts
- Track concept evolution over time
- Provide backup for IPLD blocks

## Relationship to Store
- Source JSON → CID Generator → IPLD blocks in `store/blocks/`
- Source files are NOT required for retrieval (CIDs work standalone)

## File Naming Convention
- Use lowercase with underscores: `concept_name.json`
- Include human_id in the file for clarity

## Example
```json
{
  "schema_version": "1.0.0",
  "human_id": "Domain:Type/SpecificConcept",
  "title": "Concept Title",
  ...
}
```
## Workflow

    Edit/create JSON in this directory

    Run: python tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/your_concept.json

    Concept is stored in IPLD with auto-generated provenance
