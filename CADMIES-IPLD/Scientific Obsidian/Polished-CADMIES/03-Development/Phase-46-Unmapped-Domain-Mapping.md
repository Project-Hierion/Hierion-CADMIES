---
phase: 46
date: 2026-05-21
status: ✅ Complete
related: [[Phase-44-Map-Legend-Cleanup]], [[Phase-45-Snagnar-HIEROS]], [[generate_mycelium_map.py]], [[Session-015]]
---

# Phase 46: Unmapped Domain Batch Mapping

## What Changed

The `DOMAIN_UPWARD_MAP` dictionary in `generate_mycelium_map.py` was expanded from approximately 22 entries to over 85 entries, eliminating all unmapped domain occurrences from the mycelium map. Six source concept files had their domain fields corrected from the generic "Science" to their actual disciplines. Forty previously unminted concepts were discovered during the remint process and were added to the blockstore with proper CIDs and provenance records. The relationship generator produced 28 new edges across 24 concepts. The map now displays 342 nodes, 165 edges, and exactly 15 canonical domains in the legend with zero unmapped domain warnings.

## Why

Phase 44 established the canonical 15-domain taxonomy and built the initial `DOMAIN_UPWARD_MAP`, but left 87 domain occurrences unmapped. These concepts rendered with the default gray color on the mycelium map, making them visually indistinguishable and uncategorized. The unmapped domains fell into several categories: the generic label "Science," compound domains with ambiguous primary disciplines, specialty fields without clear parents, and edge cases requiring content-based analysis.

Phase 46 was necessary because:
1. Gray nodes on the map provide no domain context to viewers
2. "Science" as a domain label conflates method with discipline
3. Compound domains like "Physics, Philosophy" needed a consistent resolution rule
4. Some concepts (linguistics, project management) were being used in domain-specific ways unique to CADMIES

## Changes Made

### 1. Content-Based Domain Mapping (Local — Session 015 Part 1)

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

**Other category redistributions:**

| Original Domain | Concepts | Mapped To | Rationale |
|----------------|----------|-----------|-----------|
| Project Management | 2 | Sociology | Team structure, sustainability, organizational design |
| Linguistics | 2 | Philosophy | Philosophy of language (word creation for philosophical ideas) |
| Communication | 1 | Sociology | Social communication strategy |
| Cultural Movement | 1 | Sociology | Cultural fusion of philosophy and entertainment |
| Knowledge Management | 1 | Sociology | Social knowledge network dynamics |
| Governance | 1 | Sociology | Community leadership model |
| Philanthropy | 1 | Ethics | Altruistic giving as ethical framework |
| Project Financing | 1 | Economics | Financial planning and resource allocation |
| Creativity, Collaboration | 1 | Sociology | Community nurturing of ideas |
| Food & Language | 1 | Sociology | Ghost concept (blockstore-only) |

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

### 5. Final Domain Mapping Batch (Paperspace — Session 015 Part 2)

The 40 newly minted concepts introduced 11 domain strings not present in the original 87. These were all mapped on Paperspace:

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

### 6. Relationship Generation

After domain mapping was complete, `generate_relationships.py --incremental --write` was run on Paperspace with Mistral 7B. The run produced 28 new edges across 24 concepts, densifying the mycelium from 139 to 165 edges.

## Testing

### Phase 46 Part 1 (Local)

| Metric | Before | After |
|--------|--------|-------|
| Unmapped domain occurrences | 87 | 11 |
| Unique unmapped domain strings | ~55 | 11 |
| DOMAIN_UPWARD_MAP entries | ~22 | ~75 |
| Concepts in blockstore | 302 | 342 |
| Edges | 135 | 139 |

### Phase 46 Part 2 (Paperspace)

| Metric | Before | After |
|--------|--------|-------|
| Unmapped domain occurrences | 11 | 0 |
| DOMAIN_UPWARD_MAP entries | ~75 | 85+ |
| Edges | 139 | 165 |

### Final Verification (Local)

```
python tools/generate_mycelium_map.py
============================================================
CADMIES MYCELIUM MAP GENERATOR v2.3.0
Canonical domains: 15
============================================================
Loading 342 concepts from blockstore...
  Filtered 316 orphan edge(s)
  342 nodes, 165 edges, 0 skipped
  Domains in legend: 15 (canonical: 15)

Map generated: mycelium_map.html
   342 nodes, 165 relationships, 15 domains in data
   Legend: 15 canonical domains shown
```

Zero unmapped domain warnings. Map legend displays exactly 15 canonical domains. All three nodes (local, Paperspace, GitHub) synchronized via git push, git pull, and tarball transfer.

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

With 342 concepts, the `DOMAIN_UPWARD_MAP` now contains over 85 entries covering all known domain strings. The system is designed to grow: new domains encountered during map generation trigger a NOTE in the terminal output, allowing incremental mapping without requiring batch phases. At this scale, new domain strings are expected to appear infrequently and will typically be straightforward one-to-one mappings.

## Issues Encountered

### Harvester Skip Logic

The harvester's `import_from_source_concepts()` identifies concepts by `human_id` only. Changed source files with the same `human_id` are silently skipped. This is by design (prevents duplicate minting) but complicates content updates. The manual index-pop-and-remint workflow is functional but not ideal for routine use. Phase 43's planned `remint_concept.py` tool will address this with a proper diff-and-remint workflow.

### New Domains from Unminted Concepts

The 40 newly minted concepts introduced 11 new domain strings, adding a small new workload to the mapping effort. This was expected — the concepts were never visible to the map generator before, so their domains were never flagged. This was a one-time cleanup cost associated with the remint cascade.

### Git Merge Conflict on Local

The locally regenerated map file conflicted with the version pushed from Paperspace. Resolved via `git stash`, `git pull`, and regeneration with the updated code. This is a routine synchronization artifact when map generation occurs on both machines before syncing.

## Conclusion

Phase 46 is complete. All 87 originally unmapped domain occurrences have been resolved. The `DOMAIN_UPWARD_MAP` now contains over 85 entries providing complete coverage for the 342-concept blockstore. The mycelium map displays exactly 15 canonical domains in the legend with zero unmapped domain warnings. The relationship generator added 28 new edges, bringing the total to 165 relationships across 342 concepts.

All three infrastructure nodes — local (HP/Fedora), Paperspace (A4000 GPU), and GitHub — are synchronized.

## Key Principles Established

1. **"Science is a method, not a domain"** — it describes the HOW, not the WHAT. Concepts labeled "Science" are redistributed to their actual discipline.
2. **Compound domains resolve to the first domain listed** — the harvester writes the anchor discipline first, the lens second.
3. **Domain mapping should be based on concept content, not domain labels** — read the definition, map what the concept actually IS.
4. **The remint workflow requires index manipulation** — changing source files does not auto-trigger reminting. Pop the index entry, run the harvester.
5. **Tarballs live in `/notebooks/` on Paperspace** — not `/root/`. File browser only shows `/notebooks/`.

### Session 015 Bonus — silent_thunderclap Deduplication

Two source concept files existed for the same concept: `silent_thunderclap.json` (minted, indexed) and `the_silent_thunderclap.json` (orphan, never minted). The orphan was removed. The minted concept has edges to two ghost concepts (`universal_truth`, `unspoken_axiom`) that do not exist in the index — these will be repaired during the next relationship regeneration pass.


### Session 022 Update — Continued Domain Growth

By May 26, 2026, the mycelium had grown to 461 nodes across 152 domains. The `DOMAIN_UPWARD_MAP` continues to expand incrementally. New domains discovered during Session 022 mega-harvests and the Rebentisch collaboration include:

| Domain String | Maps To |
|---------------|---------|
| Climate Science | Ecology |
| Plant Physiology | Biology |
| Oceanography | Physics |
| Geophysics | Physics |
| Environmental Science and Philosophy | Ecology |
| Biology, Ecology | Biology |
| Information Management | Computer Science |
| Learning Theory | Psychology |
| Knowledge Management | Sociology |

The incremental mapping system proved effective — new domains are flagged during map generation and added to `DOMAIN_UPWARD_MAP` without requiring dedicated phases. The system scales with the mycelium.