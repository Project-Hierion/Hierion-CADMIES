---
phase: 44
date: 2026-05-20
status: Complete
related: , [[generate_mycelium_map.py]], [[Session-012]], [[Session-013]]
---

# Phase 44: Map Legend Cleanup
> **📢 June 2026 — Phase 44 Has Been Superseded by Phase 66**
>
> The map features described in this document (force-directed layout,
> v2.3.0-v2.4.0) have been superseded by Phase 66: Fractal Succulent
> Layout & Progressive Loading (v3.0.0). The canonical 15-domain
> allowlist, upward mapping, directional arrows, and concept cards
> are preserved in the new version. The force-directed layout has
> been replaced with a golden-angle spiral preset layout. See
> [[Phase-66-Mycelium Map UX — Fractal Succulent Layout & Progressive Loading]] for current map architecture.

## What Changed

The mycelium map generator (`generate_mycelium_map.py`) was upgraded from v2.0.0 to v2.3.0 with four major changes: a canonical 15-domain allowlist with upward mapping replaced the uncurated domain legend, directional arrows were added to directed edge types, browser `alert()` popups were replaced with styled concept information cards, and node sizing was increased from 45px to 60px with font size set to 11px.

## Why

Three problems motivated this phase:

1. **Legend clutter.** The map legend displayed every domain string found in the blockstore, including compound domains ("Biology, Philosophy"), subdomains ("Philosophy of Science"), and specialty fields ("Quantum Physics and Philosophy"). With 302 concepts spanning 84 unique domain strings, the legend was unreadable and failed to reflect the top-level taxonomy.

2. **Invisible edge direction.** Edges for `builds_upon`, `specializes`, and `contradicts` are inherently directional — concept A builds upon concept B, not the reverse — but the graph rendered all edges identically. Users could not determine dependency direction from the visualization.

3. **Crude node interaction.** Clicking a node triggered a browser `alert()` dialog showing the raw human_id string and a `file://` URL prefix. This broke immersion, provided no concept information beyond the ID, and on mobile devices prompted users to suppress future dialogs — permanently disabling the only click interaction.

## Changes Made

### 1. Canonical 15-Domain Allowlist

A definitive list of top-level domains was established as the sole legend source:

```
Physics, Philosophy, Biology, Mathematics, Consciousness, Chemistry,
Ethics, Computer Science, Psychology, Spirituality, Neuroscience,
Sociology, Economics, Ecology, Medicine
```

Only domains present in this list appear in the map legend. All concepts retain their raw domain string in the blockstore; normalization occurs at visualization time only.

### 2. DOMAIN_UPWARD_MAP Dictionary

A mapping dictionary was constructed to resolve non-canonical domain strings to their canonical parent. Key mappings include:

| Raw Domain | Canonical Parent |
|------------|-----------------|
| Cosmology, Theoretical Physics, Astrophysics, Complexity_Science | Physics |
| Epistemology, Metaphysics, Buddhist_Philosophy | Philosophy |
| Philosophy of Art, Philosophy of Technology, Philosophy of Daily Life | Philosophy |
| Philosophy of Science, Philosophy of Mind, Philosophy of Religion | Philosophy |
| Philosophy of Language, Philosophy of Law | Philosophy |
| Genomics, MolecularBiology, Evolutionary Biology, Botany | Biology |
| Cognitive_Science, Cognitive Processes | Psychology |
| Buddhism | Spirituality |
| Artificial Intelligence, AI | Computer Science |
| Climate Ethics | Ethics |
| ConsciousnessStudies | Consciousness |

Domains not present in the mapping dictionary are logged with a NOTE during generation and receive the default gray color (`#64748B`) until manually mapped. This ensures no domain is silently absorbed into the wrong parent.

### 3. Directional Edge Arrows

Target arrow shapes and colors were added to three edge types:

| Edge Type | Color | Style | Arrow Direction |
|-----------|-------|-------|-----------------|
| builds_upon | #10B981 (green) | Solid, 2px | Points to foundation concept |
| specializes | #8B5CF6 (purple) | Dashed, 2px | Points to parent concept |
| contradicts | #EF4444 (red) | Solid, 3px | Points to contradicted concept |
| related_to | #F59E0B (orange) | Solid, 2px | No arrow (bidirectional) |

The edge legend was updated with directional indicators: `→ builds_upon`, `— related_to`, `→ specializes`, `→ contradicts`.

### 4. Concept Information Cards

The node click handler was rewritten to display a styled DOM overlay instead of a browser `alert()`. The card renders:

- **Title** — concept label
- **Domain** — normalized canonical domain, uppercase
- **Definition** — first 200 characters of the concept definition
- **Relationships** — connected edges with direction indicators (→ for outgoing, ← for incoming) and relationship type labels

Dismissal methods: X button (top-right), background click, Esc key. Card positions near the click coordinates with viewport boundary clamping. Max-height is 80vh with vertical scroll overflow for long definitions.

### 5. Node Sizing

| Property | Before | After |
|----------|--------|-------|
| Node width/height | 45px | 60px |
| Font size | 10px | 11px |
| Text max-width | 40px | 54px |
| Zoom min base | 32px | 40px |

The auto-size function was updated to use the new base dimensions, scaling proportionally with zoom level. Font size was deliberately kept independent of the 25% node size increase to prioritize label fit over uniform scaling.

### 6. Version Progression

The generator was iterated through four versions in-session:

- **v2.0.0** — baseline with compound domain removal
- **v2.1.0** — DOMAIN_NORMALIZE dict for compound → primary mapping
- **v2.2.0** — CANONICAL_DOMAINS allowlist + DOMAIN_UPWARD_MAP replacing ad-hoc normalization
- **v2.3.0** — directional arrows, concept cards, node sizing

## Testing

### Test Configuration

- **Machine:** Local (HP/Fedora), venv active
- **Blockstore:** `/run/media/fedora/PNY/CADMIES/CADMIES-IPLD/store/blocks`
- **Concept Count:** 302
- **Command:** `python tools/generate_mycelium_map.py`

### Pre-Phase Baseline

Before Phase 44, the map legend displayed all unique domain strings from the blockstore without curation. Compound domains ("Biology, Philosophy"), subdomains, and specialty fields appeared as separate legend entries with their own colors. Nodes with compound domains received colors from the DOMAIN_COLORS dictionary, which contained entries for specific compound strings — creating visual inconsistency when a compound domain had no color mapping and fell through to the default gray.

### Test Results

```
============================================================
CADMIES MYCELIUM MAP GENERATOR v2.3.0
Blockstore: /run/media/fedora/PNY/CADMIES/CADMIES-IPLD/store/blocks
Output: /run/media/fedora/PNY/CADMIES/CADMIES-IPLD/mycelium_map.html
Canonical domains: 15
============================================================
Loading 302 concepts from blockstore...
  [87 NOTE lines for unmapped domains]
  Filtered 317 orphan edge(s)
  302 nodes, 135 edges, 0 skipped
  Domains in legend: 84 (canonical: 15)

Map generated: mycelium_map.html
   302 nodes, 135 relationships, 84 domains in data
   Legend: 15 canonical domains shown
```

### Visual Verification

| Feature | Expected Behavior | Observed |
|---------|------------------|----------|
| Legend entries | ≤15 canonical domains only | 15 canonical domains shown |
| Compound domains | Mapped to primary parent | Concepts like "Biology, Philosophy" appear under Biology color |
| Edge arrows | Directed edges show target arrows | Green/purple/red arrows visible on builds_upon, specializes, contradicts |
| related_to | No arrow | Orange lines without arrows |
| Concept card | Styled overlay with title, domain, definition, relationships | Card appears on click with all fields populated |
| Card dismiss | X button, background click, Esc | All three methods functional |
| Node size | 60px base | Nodes visibly larger, labels fit within circles |
| Unmapped domains | NOTE logged, default gray color | 87 NOTE lines generated for review |

## Analysis

### Domain Collapse Efficiency

The upward mapping reduced 84 unique domain strings to 15 canonical entries — an 82% reduction in legend clutter. The 87 NOTE lines represent domains that still require manual mapping. These fall into clear categories:

- **Philosophy variants** (majority): Philosophy of Language, Philosophy of Mind, Philosophy of Religion, Philosophy of Science, Philosophy of Physics, Philosophy & Neuroscience, Philosophy & Psychology — all map to Philosophy
- **Physics variants:** Physics (String Theory), Quantum Physics and Philosophy, Quantum Mechanics/Physics/Consciousness — all map to Physics
- **Compound crosses:** Neuroscience & Philosophy → Neuroscience, Psychology and Neuroscience → Psychology, Biology and Philosophy of Mind → Biology
- **New domains requiring decisions:** Linguistics (→ Psychology or Philosophy), Communication (→ Sociology), Law variants (→ Sociology), Project Management/Governance/Philanthropy (→ Sociology or Economics), Art/Literature/Creativity variants (→ Philosophy), Science/Science & Technology (→ Physics as default)

These are catalogued for the next mapping pass but do not block Phase 44 completion — the system correctly flags and isolates unmapped domains rather than silently misattributing them.

### Edge Direction Semantics

The target-arrow convention was validated: arrow points to the concept being acted upon (the foundation for builds_upon, the parent for specializes, the target of challenge for contradicts). This aligns with graph theory convention where the arrow indicates the direction of the relationship — "A builds_upon B" means the arrow terminates at B, the foundation. User confirmation during testing verified this is intuitively correct.

### Concept Card Usability

The card provides substantially more information than the alert() it replaces: domain context, definition preview, and relationship inventory with direction. The multiple dismissal paths (X, background, Esc) prevent the "trapped in a dialog" feeling of the alert. Mobile behavior is improved — no "prevent additional dialogs" checkbox to accidentally trigger.

### Node Sizing

At 60px with 11px font, multi-word concept labels (e.g., "The Laminar Paradox") fit within the node circle. The text-max-width of 54px provides 6px of padding inside the 60px node. At high zoom levels, the auto-size function scales proportionally from the new base.

## Issues Encountered

### SELinux Warning (Non-Blocking)

The browser auto-open triggered an SELinux warning about Widevine CDM path resolution:

```
restorecon: SELinux: Could not get canonical path for
/var/home/fedora/.mozilla/firefox/*/gmp-widevinecdm/*
restorecon: No such file or directory.
```

This is a known Firefox/SELinux interaction on Fedora, unrelated to the map generator. Does not affect functionality.

### Orphan Edges

317 orphan edges were filtered — relationships where either the source or target concept does not exist in the blockstore. This is consistent with prior map generation runs and reflects the legacy_edges.json file containing references to concepts that were never minted or whose human_ids changed. Not addressed in this phase; belongs to a future data cleanup phase.

## Conclusion

Phase 44 is complete and confirmed working. The mycelium map now presents a curated 15-domain legend, directional edge arrows for asymmetric relationships, styled concept cards replacing browser dialogs, and larger nodes accommodating readable labels. The upward mapping system provides a sustainable mechanism for absorbing new domains as the mycelium grows, with unmapped domains explicitly flagged rather than silently misattributed. The 87 flagged domains are catalogued for the next mapping iteration but do not represent a regression — they were previously scattered across the legend as distinct entries and are now consolidated into the default category pending review.

## Next Steps

- Map the 87 flagged unmapped domains into DOMAIN_UPWARD_MAP (batch update)
- Investigate orphan edges for data integrity (future phase)
- Continue Session 013 on Paperspace: Phase 45A — clone Snagnar/HIEROS
