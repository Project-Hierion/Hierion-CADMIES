---
phase: 66
date: 2026-06-24
status: Designed, Postponed until further notice.
related: [[Phase-44-Map-Legend-Cleanup]], [[Phase-63-Cloud Deployment — Project Hierion Foundation]], [[Phase-64-Hierion Database Infrastructure — Isolated MongoDB Deployment]], [[Phase-65-Hierion Domain & Web Server Configuration]], [[Session-032 — 2026-06-24 — The Mycelium Becomes a Succulent]], [[generate_mycelium_map.py]]
---

# Phase 66: Mycelium Map UX — Fractal Succulent Layout & Progressive Loading

## What Changed

The mycelium map was redesigned with a fractal succulent layout using golden-angle
spiral positioning, pre-computed 3D coordinates, depth-based opacity, and chunked
progressive loading. The map generator was upgraded from v2.4.0 to v3.0.0. A
renderer-agnostic data layer (`concepts_ranked.json`) was created to serve any
future map renderer.

## Why

The map was loading all 636 concepts and 1,131 edges at once. Load time grew with
every harvest. Users experienced visible delays. The force-directed layout caused
nodes to drift when new concepts were added, creating a jitter effect during
exploration. A faster, more stable, more beautiful map was needed — one that
reflected the organic, interconnected nature of the mycelium itself.

## Changes Made

### Fractal Succulent Layout

- Concepts are positioned using a golden-angle spiral (137.5°) grouped by
  canonical domain. Each of the 15 domains forms an anchor point in a ring.
  Within each domain, concepts spiral outward sorted by importance score.
- Every concept receives pre-computed x, y, and z coordinates. The z-axis
  represents depth — concepts closer to the viewer (higher z) appear larger
  and more opaque. Deeper concepts (lower z) are smaller and faded.
- Depth layers: domain anchors at z=0 (leaf tips), cross-domain connectors at
  z=-30, subdomain concepts at z=-60, deep concepts at z=-100.
- Score determines position within the spiral: edge count plus cross-domain
  bonus. High-scoring, well-connected concepts sit at the visible tips.

### Chunked Progressive Loading

- Instead of loading all 636 nodes at once, the map loads in chunks of 150
  concepts, sorted by score descending. Initial load: top-ranked concepts.
- A "Load More" button allows users to pull in additional batches on demand.
- New nodes appear at their pre-computed positions without triggering a force
  simulation. The preset layout ensures zero jitter.
- A renderer-agnostic data file (`concepts_ranked.json`) contains all 636
  concepts with positions, scores, domains, and edge data.

### Visual Design Updates

- Background changed from white to dark (#0a0a0f) to make depth-based opacity
  visible. Closer concepts appear brighter; deeper concepts fade naturally.
- Edge opacity adjusted (0.5 → 0.7) for visibility on dark background.
- Zooming in reveals deeper layers as opacity increases with zoom level.
- Orphan concepts (zero relationships) appear as a visible line — the map
  shows where the mycelium needs to grow.

### Critical Design Rule

The progressive loading logic is renderer-agnostic. A function like
`getConceptsForViewport(bounds, zoom, domains)` returns concept data from
the ranked JSON. Cytoscape.js calls it now. D3 Canvas, sigma.js, or Three.js
can call it later. Same data, different visual output. Swap the windshield,
not the engine.

## Renderer Evolution Path

| Stage | Tool | Purpose | Status |
|---|---|---|---|
| 1 | Cytoscape.js with preset layout | Current implementation — fractal succulent | ✅ Complete |
| 2 | D3 Canvas Renderer | Quicker rendering, lighter DOM | 💡 Backup |
| 3 | sigma.js | WebGL renderer for 2,000+ nodes | 💡 Backup |
| 4 | Three.js + WebXR | 3D immersive mycelium universe, VR-capable | 💡 Long-term |

## Testing

### Test Configuration

- **Machine:** Cloud GPU instance
- **Blockstore:** `/notebooks/CADMIES/CADMIES-IPLD/store/blocks`
- **Concept Count:** 636
- **Command:** `python tools/generate_mycelium_map.py`

### Test Results
============================================================
CADMIES MYCELIUM MAP GENERATOR v3.0.0
Blockstore: /notebooks/CADMIES/CADMIES-IPLD/store/blocks
Output: /notebooks/CADMIES/CADMIES-IPLD/mycelium_map.html
Ranked data: /notebooks/CADMIES/CADMIES-IPLD/concepts_ranked.json
Canonical domains: 15
============================================================
Loading 674 concepts from blockstore...
Filtered 248 orphan edge(s)
636 nodes, 1131 edges, 38 skipped
Domains in data: 107 (canonical with concepts: 15)
Initial load: 126 concepts (of 636 total)

Ranked data saved: /notebooks/CADMIES/CADMIES-IPLD/concepts_ranked.json
636 concepts, 1131 edges
Initial load: 126 concepts

Map generated: /notebooks/CADMIES/CADMIES-IPLD/mycelium_map.html
636 total nodes, 1131 total edges, 107 domains in data
Legend: 15 canonical domains shown
Phase 66: Progressive loading — 126 concepts initial, 510 lazy-loaded


### Visual Verification

| Feature | Expected Behavior | Observed |
|---|---|---|
| Initial load | ~126 concepts, fast render | ✅ |
| Fractal impression | Visible domain clusters at zoom-out | ✅ |
| Depth-based opacity | Closer concepts brighter, deeper faded | ✅ |
| Load More button | Pulls next 150 concepts | ✅ |
| No jitter on load | New nodes at preset positions | ✅ |
| Preset layout | No force simulation drift | ✅ |
| Orphan visibility | Concepts with no edges visible at bottom | ✅ |
| Dark background | Depth effect visible | ✅ |
| Edge rendering | 1,131 edges visible at 0.7 opacity | ✅ |
| concepts_ranked.json | Contains all 636 concepts with x/y/z | ✅ |

### Issues Encountered

**Load More nodes at (0,0):** New nodes added via `cy.add()` were not
respecting their preset positions and appeared in a straight line at the
origin. Fixed by explicitly setting node positions after adding elements.

**Edge opacity too low:** Initial edge opacity of 0.5 was nearly invisible
against the dark background. Adjusted to 0.7 for clear visibility.

**Auto-layout jitter:** An auto-load feature triggered on viewport changes,
running layout on new nodes and causing graph-wide shaking. Removed entirely
in favor of the manual Load More button.

## Analysis

### Performance Improvement

The initial render dropped from 636 nodes to approximately 126 — an 80%
reduction in first-load elements. The preset layout eliminates the 2,000-iteration
force simulation that previously ran on every map generation. Map generation
time decreased noticeably, and the browser render is perceptibly faster.

### Fractal Structure

The golden-angle spiral (137.5°) successfully creates natural-looking clusters
without collision. Each domain's concepts radiate outward from the domain anchor
in a mathematically-derived pattern that mimics plant growth. The structure
will become more complex and visually striking as additional concepts are
harvested and positioned within the spiral.

### Depth Effect

The z-axis opacity system provides a genuine sense of depth in a 2D renderer.
Users can perceive which concepts are more important (closer, brighter) and
which are waiting to be explored (deeper, faded). Zooming in naturally reveals
deeper layers. The effect is subtle but effective.

### Orphan Visibility

Concepts with zero relationships appear at the bottom of the map in a visible
line. This is an intentional feature — the map shows where the mycelium needs
to grow. Future relationship generation passes will connect these orphans into
the main structure.

## Conclusion

Phase 66 is complete and deployed. The mycelium map now uses a fractal succulent
layout with golden-angle spiral positioning, pre-computed 3D coordinates, and
depth-based opacity. Progressive loading via chunks of 150 concepts eliminates
the performance bottleneck of loading all 636 nodes at once. The preset layout
eliminates jitter. The renderer-agnostic data layer (`concepts_ranked.json`)
ensures future map renderers can consume the same data without modification.

The map is faster. The map is stable. The map breathes. The succulent grows.

## Next Steps

- Map unmapped domains into DOMAIN_UPWARD_MAP
- Phase 67: GPU compute bridge for Dr. Mistral integration
- Future: 3D immersive rendering via Three.js + WebXR (long-term)
