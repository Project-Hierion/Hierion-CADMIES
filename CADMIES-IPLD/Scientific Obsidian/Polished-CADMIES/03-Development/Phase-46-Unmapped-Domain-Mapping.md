---
phase: 46
date: 2026-05-21
status: 🟡 In Progress — 87 unmapped reduced to 11
related: [[Phase-44-Map-Legend-Cleanup]], [[Phase-45-Snagnar-HIEROS]], [[generate_mycelium_map.py]], [[Session-015]]
---

# Phase 46: Unmapped Domain Batch Mapping

## What Changed

The `DOMAIN_UPWARD_MAP` dictionary in `generate_mycelium_map.py` was expanded from approximately 22 entries to approximately 75 entries, reducing unmapped domain occurrences from 87 to 11. Six source concept files had their domain fields corrected from the generic "Science" to their actual disciplines. Forty previously unminted concepts were discovered during the remint process and were added to the blockstore with proper CIDs and provenance records.

## Why

Phase 44 established the canonical 15-domain taxonomy and built the initial `DOMAIN_UPWARD_MAP`, but left 87 domain occurrences unmapped. These concepts rendered with the default gray color on the mycelium map, making them visually indistinguishable and uncategorized. The unmapped domains fell into several categories: the generic label "Science," compound domains with ambiguous primary disciplines, specialty fields without clear parents, and edge cases requiring content-based analysis.

Phase 46 was necessary because:
1. Gray nodes on the map provide no domain context to viewers
2. "Science" as a domain label conflates method with discipline
3. Compound domains like "Physics, Philosophy" needed a consistent resolution rule
4. Some concepts (linguistics, project management) were being used in domain-specific ways unique to CADMIES

## Changes Made

### 1. Content-Based Domain Mapping

Instead of mapping domains by name alone, each unmapped concept's source file was read to determine its actual subject matter. Key examples:

**"Science" (6 concepts) — redistributed by content:**

| Concept | Original Domain | New Domain | Rationale |
|---------|----------------|------------|-----------|
| unified_science | Science | Philosophy | Meta-framework for knowledge integration |
| unified_map_of_reality | Science | Physics | Quantum fields as anchor for reality mapping |
| living_system_project | Science | Sociology | Self-organizing knowledge ecosystem |
| synergistic_thinking | Science | Philosophy | Epistemology of interdisciplinary work |
| complexity_paradigm_shift | Science | Philosophy | Philosophical paradigm shift |
| community_driven_paradigm_shift | Science | Sociology | Social organization of science |

**"Project Management" (2 concepts) → Sociology:**
Both concepts addressed team structure, sustainability, and organizational design, not technical project management methodologies.

**"Linguistics" (2 concepts) → Philosophy:**
Both concepts dealt with word creation for philosophical ideas ("Hieros," "Cosmic Mycelium Lexical Family"), placing them in philosophy of language rather than scientific linguistics.

**"Communication" (1 concept) → Sociology:**
"Subversive Delivery" — using humor and pop culture to spread ideas — is a social communication strategy.

**"Cultural Movement" (1 concept) → Sociology:**
"Futurama Esque" — cultural fusion of philosophy and entertainment.

**"Knowledge Management" (1 concept) → Sociology:**
"Self-Perpetuating Ecosystem" — social knowledge network dynamics.

**"Governance" (1 concept) → Sociology:**
"Volunteer Guardianship" — community leadership model.

**"Philanthropy" (1 concept) → Ethics:**
"Philanthropy Catalyst" — altruistic giving as an ethical framework.

**"Project Financing" (1 concept) → Economics:**
"Transparent Budgeting" — financial planning and resource allocation.

**"Creativity, Collaboration" (1 concept) → Sociology:**
"Spores and Gardeners" — community nurturing of ideas.

**"Food & Language" (1 concept) → Sociology:**
Ghost concept (blockstore-only, no source file found).

### 2. Compound Domain Resolution Rule

For all compound domains (e.g., "Physics, Philosophy," "Neuroscience & Philosophy," "Art & Philosophy"), the rule applied is: **the first domain listed is the primary domain.** The domain the harvester wrote first reflects the concept's anchor discipline. The second domain represents the lens or application area.

Examples:
- "Physics, Philosophy" → Physics (physics concept viewed through philosophical lens)
- "Philosophy, Physics" → Philosophy (philosophical concept informed by physics)
- "Neuroscience & Philosophy" → Neuroscience
- "Art & Philosophy" → Philosophy (art concept viewed philosophically)

### 3. Source Concept Domain Corrections

Six source concept files had their `domain` field corrected:

| File | Old Domain | New Domain |
|------|-----------|------------|
| `source_concepts/unified_science.json` | Science | Philosophy |
| `source_concepts/unified_map_of_reality.json` | Science | Physics |
| `source_concepts/living_system_project.json` | Science | Sociology |
| `source_concepts/synergistic_thinking.json` | Science | Philosophy |
| `source_concepts/complexity_paradigm_shift.json` | Science | Philosophy |
| `source_concepts/community_driven_paradigm_shift.json` | Science | Sociology |

### 4. Remint Process

Changing source concept files does not automatically update the blockstore. The harvester's `import_from_source_concepts()` function checks only `human_id` against the index — it does not compare file content hashes. Same `human_id` = skip, even if the file content changed.

**Resolution:** The six affected `human_id` entries were manually removed from `store/index/human_id_to_cid.json`. The harvester was then run with Ollama killed locally, forcing the no-LLM manual import path. This caused the harvester to find all source concepts not present in the index and mint them fresh.

**Result:** 46 concepts were reminted with new CIDs and provenance records — the six corrected concepts plus 40 additional concepts that existed in `source_concepts/` but had never been added to the blockstore.

### 5. New Unmapped Domains

The 40 newly minted concepts introduced 11 domain strings not present in the original 87. These were all straightforward to categorize:

| Domain String | Occurrences | Maps To |
|---------------|-------------|---------|
| Biomysticism | 1 | Philosophy |
| Quantum Physics & Philosophy | 2 | Physics |
| Philosophy, Religion, Physics | 1 | Philosophy |
| Neuroscience & Quantum Physics | 1 | Neuroscience |
| Philosophy, Psychology | 1 | Philosophy |
| Philosophy, Consciousness | 1 | Philosophy |
| Astrobiology | 1 | Biology |
| Philosophy/Quantum Physics | 1 | Physics |
| Metaphysics & Philosophy | 1 | Philosophy |
| Neuroscience/Philosophy | 1 | Neuroscience |

These 11 remaining entries have been catalogued for the next mapping session but do not block Phase 46 completion — the system correctly identifies and flags them.

## Testing

### Pre-Phase State

| Metric | Value |
|--------|-------|
| Unmapped domain occurrences | 87 |
| Unique unmapped domain strings | ~55 |
| DOMAIN_UPWARD_MAP entries | ~22 |
| Concepts in blockstore | 302 |
| Edges | 135 |

### Post-Phase State

| Metric | Value |
|--------|-------|
| Unmapped domain occurrences | 11 |
| Unique unmapped domain strings | 11 |
| DOMAIN_UPWARD_MAP entries | ~75 |
| Concepts in blockstore | 342 |
| Edges | 139 |

### Verification

The map generator was run locally:

```
python tools/generate_mycelium_map.py
```

Output confirmed: 342 nodes, 139 edges, 15 canonical domains in legend, 11 unmapped domain NOTES remaining (the 11 new domains from the freshly minted concepts).

## Analysis

### Domain Mapping Methodology

The content-based approach proved essential. Domain labels alone are insufficient for categorization because:
1. "Science" is a method, not a discipline — it describes HOW knowledge is acquired, not WHAT the knowledge is about
2. Compound domains require a consistent resolution rule (first domain = primary)
3. Some CADMIES concepts use domain labels in project-specific ways (e.g., "Linguistics" = philosophy of language, "Project Management" = community governance)

### The "Science" Problem

Six concepts were tagged "Science" by the harvester, likely because the source conversations discussed scientific methodology or interdisciplinary approaches. However, "Science" is not one of the canonical 15 domains. The concepts were redistributed based on their actual subject matter:
- Meta-frameworks → Philosophy
- Physics-based frameworks → Physics
- Social systems → Sociology

This establishes a principle: if a concept's domain label is a method rather than a discipline, it should be mapped to the discipline the method serves.

### Remint Cascade

Removing index entries to force reminting revealed 40 previously unminted concepts. These concepts existed in `source_concepts/` but were never added to the blockstore, likely from harvests where concepts were extracted but the pipeline was interrupted before minting. The blockstore now accurately reflects all available source concepts.

### Scale of the Domain Mapping System

With 342 concepts, the `DOMAIN_UPWARD_MAP` now contains approximately 75 entries covering the vast majority of domain strings. The system is designed to grow: new domains encountered during map generation trigger a NOTE in the terminal output, allowing incremental mapping without requiring batch phases.

## Issues Encountered

### Harvester Skip Logic

The harvester's `import_from_source_concepts()` identifies concepts by `human_id` only. Changed source files with the same `human_id` are silently skipped. This is by design (prevents duplicate minting) but complicates content updates. The manual index-pop-and-remint workflow is functional but not ideal for routine use. Phase 43's planned `remint_concept.py` tool will address this with a proper diff-and-remint workflow.

### New Domains from Unminted Concepts

The 40 newly minted concepts introduced 11 new domain strings, adding a small new workload to the mapping effort. This was expected — the concepts were never visible to the map generator before, so their domains were never flagged. This is a one-time cleanup cost associated with the remint cascade.

## Conclusion

Phase 46 is substantially complete. The original 87 unmapped domain occurrences have been reduced to 11, all of which are catalogued and have straightforward mappings. The `DOMAIN_UPWARD_MAP` now covers approximately 75 domain strings, providing robust coverage for the 342-concept blockstore. The map generator correctly displays all mapped concepts under their canonical 15-domain legend entries, and unmapped domains are explicitly flagged for review.

The remaining 11 domain mappings can be completed in the next session. They are all direct one-to-one mappings with no content analysis required.

## Key Principles Established

1. **"Science is a method, not a domain"** — it describes the HOW, not the WHAT. Concepts labeled "Science" are redistributed to their actual discipline.
2. **Compound domains resolve to the first domain listed** — the harvester writes the anchor discipline first, the lens second.
3. **Domain mapping should be based on concept content, not domain labels** — read the definition, map what the concept actually IS.
4. **The remint workflow requires index manipulation** — changing source files does not auto-trigger reminting. Pop the index entry, run the harvester.

## Next Steps

| #   | Action                                                 | Priority |
| --- | ------------------------------------------------------ | -------- |
| 1   | Add 11 remaining domain mappings to DOMAIN_UPWARD_MAP  | 🔴       |
| 2   | Regenerate map, verify zero "Unmapped domain" warnings | 🔴       |
| 3   | Run `generate_relationships.py --incremental --write`  | 🟡       |
| 4   | Commit all changes, push to GitHub                     | 🔴       |
| 5   | Restart Ollama local for future harvests               | 🟢       |