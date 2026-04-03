# Source Concepts Directory

This directory contains human-readable JSON source files for concepts stored in CADMIES-IPLD.

## Purpose
- Keep editable source files for concepts
- Track concept evolution over time
- Provide backup for IPLD blocks
- Serve as templates for creating new PhD-level concepts

## Current Status
- **20 PhD-level concepts** loaded with full provenance
- **Domains covered:** Physics, Philosophy, Biology, Mathematics, Psychology, Epistemology, Cosmology
- **Concept types:** ScientificLaw, PhilosophicalHypothesis, MathematicalTheorem, CognitiveBias, Paradox, ThoughtExperiment, etc.

## Relationship to Store
- Source JSON → CID Generator → IPLD blocks in `store/blocks/`
- Source files are NOT required for retrieval (CIDs work standalone)
- Each concept generates auto-provenance (timestamp, author) and version history

## File Naming Convention
- Use lowercase with underscores: `concept_name.json`
- human_id in JSON should match filename (snake_case format per v2.0.0 spec)

## PhD-Level Concept Template

```json
{
  "schema_version": "1.0.0",
  "human_id": "concept_name_in_snake_case",
  "title": "Human Readable Title",
  "definition": "Clear, concise one-paragraph definition",
  "type": "ScientificLaw",
  "domain": "Physics",
  "subdomain": "Classical Mechanics",
  "formula": "Mathematical expression (optional)",
  "proofs": [
    {
      "type": "theoretical",
      "description": "Theoretical basis",
      "confidence": 0.95,
      "reference": "Author, A. (Year). Title."
    }
  ],
  "relationships": {
    "builds_upon": ["prerequisite_concept"],
    "contradicts": [],
    "related_to": ["related_concept"],
    "specializes": ["specialized_concept"]
  },
  "difficulty_levels": {
    "beginner": "Simple explanation",
    "intermediate": "Detailed explanation",
    "expert": "Advanced treatment with limitations"
  },
  "learning_path": {
    "prerequisites": ["required_concept"],
    "next_steps": ["advanced_concept"]
  },
  "metadata": {
    "created": "2026-04-03T00:00:00Z",
    "creator": "CADMIES PhD Template v1.0",
    "certainty_score": 0.95,
    "version": 1,
    "license": "CC BY-SA 4.0",
    "purpose": "educational"
  },
  "extra_fields": {
    "historical_context": "Who discovered it, when, and under what circumstances",
    "limitations": "Where the concept breaks down or doesn't apply",
    "discoverer": "Name of discoverer(s)",
    "discovery_year": 0000,
    "applications": ["practical_use_1", "practical_use_2"]
  }
}

Example Concept (Conservation of Energy)
json

{
  "schema_version": "1.0.0",
  "human_id": "conservation_of_energy",
  "title": "Law of Conservation of Energy",
  "definition": "Energy cannot be created or destroyed within an isolated system; it can only transform from one form to another.",
  "type": "ScientificLaw",
  "domain": "Physics",
  "subdomain": "Classical Mechanics",
  "formula": "ΔE_system + ΔE_surroundings = 0",
  "metadata": {
    "creator": "CADMIES PhD Template v1.0",
    "certainty_score": 0.99,
    "version": 2,
    "purpose": "educational"
  }
}

Workflow
Adding a New Concept

    Create JSON file in this directory following the template above

    Run the CID generator:
    bash

cd /path/to/CADMIES-IPLD
python tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/your_concept.json

Concept is stored in IPLD with auto-generated provenance

Verify with the GUI or CLI:
bash

python tools/core/cbor_reader.py your_concept_name

Batch Processing Multiple Concepts
bash

cd /path/to/CADMIES-IPLD
for file in source_concepts/*.json; do
    python tools/core/cid_generator_v1_1_0.py --concept-file "$file"
done

Version History

When updating an existing concept:

    Edit the source JSON with new content

    Increment the version field in metadata

    Add supersedes field with the old CID

    Run the CID generator again

    New CID is created; old block remains immutable

v2.0.0 Specification Compliance

All concepts in this directory follow the CADMIES CID Structure Specification v2.0.0:

    human_id format: snake_case (lowercase with underscores)

    No embedded domain/type in human_id (separate fields in JSON)

    Domain and type are CamelCase in their respective fields

See Also

    CID Structure Specification v2.0.0

    GUI Documentation

    Main README
