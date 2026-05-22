---
phase: 47
date: 2026-05-21
status: ✅ Complete
related: [[Phase-46-Unmapped-Domain-Mapping]], [[Phase-38-Ferdinand-Easter-Egg]], [[generate_mycelium_map.py]], [[Session-016]]
---

# Phase 47: Orphan Edge Resolution

## What Changed

All 316 orphan edges were identified, categorized, and stripped from the mycelium graph. The map now displays 342 nodes and 167 edges with zero orphan edge warnings and zero unmapped domain warnings. A reusable stripping tool with backup capability was created at `tools/strip_all_orphans.py`. The root cause was identified: the relationship generator writes edges referencing target concepts without verifying those targets exist in the blockstore.

## Why

The mycelium map generator had been filtering 316 orphan edges — edges where the `target` human_id does not resolve to any concept in the blockstore. These edges appeared in the terminal output as `Filtered 316 orphan edge(s)` but were never visible on the map, creating a discrepancy between the reported edge count (481 total) and the displayed edge count (165 valid). 

The orphans fell into several categories:
1. **Dead CIDs (5):** Blocks that had been deleted during prior cleanup but whose edges were never removed
2. **Thunderclap variants (3):** `the_silent_thunderclap`, `The_Silent_Thunderclap`, `silent_thunderclap` — a duplicate concept that had been partially cleaned up
3. **Case mismatches (~1):** TitleCase references pointing to existing snake_case concepts
4. **Unminted references (remaining):** Valid concept names referenced in relationships but never created as blocks (e.g., `general_relativity`, `abiogenesis`, `bayesian_inference`)

The root cause was identified in the relationship generation pipeline: `generate_relationships.py` writes edges to whatever targets Mistral suggests without verifying those targets exist in the blockstore index. Mistral correctly identifies conceptual connections ("abiogenesis relates to astrobiology") but the pipeline does not check whether `abiogenesis` and `astrobiology` have been minted before writing the edge.

## Changes Made

### 1. Orphan Edge Extraction (Diagnostic)

A diagnostic script (`tools/extract_orphan_edges.py`) replicated the map generator's edge validation logic to produce a complete catalog of orphan edges. Results:

| Metric | Count |
|--------|-------|
| Total unique edges | 481 |
| Valid edges | 165 |
| Orphan edges | 316 |
| Unique missing targets | 267 |

**Orphan edge types:**

| Type | Count |
|------|-------|
| related_to | 155 |
| builds_upon | 88 |
| specializes | 50 |
| contradicts | 23 |

### 2. First Pass: Known Bad Targets (8 edges)

Five dead CIDs and three thunderclap variants were stripped manually. These were unambiguous — the target blocks no longer existed or were duplicates marked for deletion.

| Target | Reason |
|--------|--------|
| `bafyreiftvhx64umvh3j...` | Block deleted |
| `bafyreigcii5de4qhwnn...` | Block deleted |
| `bafyreignxp73ooqeiwd...` | Block deleted |
| `bafyreihlh4vwiexvuq6...` | Block deleted |
| `bafyreiht7rhfuixpxqt...` | Block deleted |
| `the_silent_thunderclap` | Duplicate — removed |
| `The_Silent_Thunderclap` | Duplicate — removed |
| `silent_thunderclap` | Duplicate — removed |

### 3. Ghost Minting Attempt (Abandoned)

An attempt was made to mint 260 "ghost" placeholder concepts for the remaining orphan targets. These concepts would have domain "Ghost" and a definition clearly marking them as placeholders awaiting formal minting. The approach was abandoned because:

1. The custom script conflicted with `cid_generator.py`'s internal index management
2. The resulting blocks were not reliably written or indexed
3. The approach introduced complexity (ghost concepts in the blockstore) to solve a problem better addressed by stripping edges and fixing the root cause

**Lesson:** The pipeline tools (`cid_generator.py`, harvester) are the correct path for concept creation. Custom scripts that bypass or duplicate their logic introduce more problems than they solve.

### 4. Complete Strip (306 edges)

All remaining orphan edges were stripped in a single operation on Paperspace (A6000 GPU). The operation:

1. Created a backup tarball of `store/blocks/` at `store/index/backups/blocks_pre_orphan_strip_TIMESTAMP.tar.gz`
2. Scanned all source concepts for edges pointing to non-existent targets
3. Removed those edges from the source concepts' relationship lists
4. Rewrote the affected CBOR blocks

Result: 306 edges stripped. Two stragglers (`general_relativity` and `kerr_metric` from Gravitomotive Gearbox) were manually removed in a follow-up pass.

### 5. Reusable Tool: `strip_all_orphans.py`

The stripping logic was preserved as `tools/strip_all_orphans.py` for future use. Features:
- Dry run mode (`--apply` flag required for actual writes)
- Automatic backup tarball creation before modification
- Clear undo instructions printed on completion
- Handles both `.cbor` extension and bare CID filenames

## Testing

### Before (Session 015)

python tools/generate_mycelium_map.py  
Filtered 316 orphan edge(s)  
342 nodes, 165 edges, 0 skipped

### After First Pass (8 stripped)

python tools/generate_mycelium_map.py  
Filtered 308 orphan edge(s)  
342 nodes, 165 edges, 0 skipped

### After Complete Strip (all stripped)

python tools/generate_mycelium_map.py  
342 nodes, 167 edges, 0 skipped

Zero orphan edge warnings. Zero unmapped domain warnings. Map displays exactly what the blockstore contains.

### Cross-Node Verification
| Node | Nodes | Edges | Orphans | Status |
|------|-------|-------|---------|--------|
| Paperspace (A6000) | 342 | 167 | 0 | ✅ Clean |
| Local (HP/Fedora) | 342 | 167 | 0 | ✅ Clean |
| GitHub | — | — | — | ✅ Synced |
All three nodes synchronized via git push, git pull, and tarball transfer (`cadmies_session016_clean.tar.gz`).
## Analysis
### Why the Edge Count Changed (165 → 167)
The edge count increased from 165 to 167 despite stripping 316 orphan edges. This is because the orphan edges were never counted in the displayed edge total — they were filtered before display. The increase of 2 edges reflects legitimate new relationships added during the session's synchronization process, not orphan resolution.
### The Relationship Generator Bug
The root cause is in the Phase 2-3 relationship pipeline. When Mistral generates relationship suggestions, it proposes edges between concepts based on semantic understanding. However, the pipeline writes these edges without verifying that both source and target concepts exist in the blockstore index.
**Current flow:**

Mistral suggests edge → Parse JSON → Write to source block

**Required flow:**

Mistral suggests edge → Parse JSON → Validate target exists in index → Write to source block

This validation step should be added to `generate_relationships.py` or `phase3_write.py`. Without it, every relationship generation cycle risks creating new orphan edges.
### What Was Lost
The 306 stripped edges represented genuine conceptual connections identified by Mistral 7B. The model correctly identified relationships like:
- `Gravitomotive Gearbox → General Relativity`
- `abiogenesis → astrobiology`
- `bayesian_inference → probability_theory`
These relationships are semantically valid and would be valuable additions to the mycelium — but only when the target concepts actually exist. Stripping them prioritizes graph integrity over graph density.
The harvester will naturally recreate many of these edges as new concepts are minted and relationship regeneration runs occur.
## Conclusion
Phase 47 is complete. The mycelium graph is clean: 342 nodes, 167 edges, zero orphans, zero unmapped domains. All three infrastructure nodes are synchronized. The `strip_all_orphans.py` tool provides reusable orphan cleanup capability.
The root cause remains unpatched. The relationship generator needs a target validation step to prevent future orphan creation. This is flagged for Phase 48 or as part of a broader relationship pipeline hardening effort.
## Key Principles Established
1. **Graph integrity over graph density.** An edge to a non-existent concept is not a connection — it's an error. Strip first, rebuild properly.
2. **Use the pipeline tools.** Custom scripts that bypass `cid_generator.py`, the harvester, or the relationship generator introduce inconsistency. The tools exist for a reason.
3. **Always backup before block modification.** The `store/index/backups/` directory (Phase 42) provides a natural location for pre-modification backups.
4. **Validate targets before writing edges.** The relationship generator must check the index before writing. This is a bug, not a missing feature.
## Next Steps
- **Phase 48:** Patch `generate_relationships.py` to validate target existence before writing edges
- **Phase 43:** Build `remint_concept.py` for proper concept editing workflow
- **Ongoing:** Harvester will naturally mint missing concepts and recreate legitimate edges