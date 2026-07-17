> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 032 — 2026-06-24 — The Mycelium Becomes a Succulent

related: [[Session-031 — 2026-06-23 — The Mycelium Gets a New Home]], [[Phase-66-Mycelium Map UX — Fractal Succulent Layout & Progressive Loading]], [[Session-033 — 2026-07-11 — The Gardener's words & Fine-Tuning]]

## What We Did

**The mycelium map learned to breathe. Fractal succulent layout born.**

Started with a problem: the map was loading all 636 concepts at once via
D3/Cytoscape SVG. It was getting slower with every harvest. Users would
wait. Waiting sucks. Diminishing ignorance requires speed.

Designed and built Phase 66: Mycelium Map UX v3.0.0.

**The Fractal Succulent Layout:**

The gardener had a vision while looking at a succulent. Concepts positioned
like leaves on a plant — golden-angle spiral (137.5°), the same math nature
uses to pack leaves efficiently. Each of the 15 canonical domains forms an
anchor point in a ring. Within each domain, concepts spiral outward by score.
High-scoring concepts sit at the tips (z=0, full opacity). Cross-domain
connectors float at z=-30. Subdomain concepts at z=-60. Deep concepts at
z=-100, faded, waiting to be discovered.

The map background went dark (#0a0a0f) to make the depth effect visible.
Closer concepts are brighter. Zooming in reveals deeper layers. The succulent
breathes.

**Chunked Loading:**

Instead of loading all 636 nodes at once, the map loads in chunks of 150.
Initial load: top concepts by score. A "Load More" button pulls in the next
batch. New nodes appear at their pre-computed positions — no force simulation,
no jitter, no shaking. The preset layout places every concept exactly where
the math says it belongs.

**The Jitter Fix:**

First attempt had auto-layout running on new nodes, which shook the whole
graph. Removed it. Then the Load More nodes weren't respecting their preset
positions — they were appearing at (0,0) in a straight line at the bottom.
Fixed by explicitly setting positions after cy.add(). Then edges weren't
rendering because opacity was too low against the dark background. Bumped
edge opacity from 0.5 to 0.7.

**The Orphan Line:**

At the bottom of the map, a perfect horizontal line of nodes with no edges.
Those are concepts with zero relationships — orphans. The map makes them
visible. You can see where the mycelium needs to grow.

**Renderer-Agnostic Data Layer:**

concepts_ranked.json now contains all 636 concepts with pre-computed x/y/z
positions, scores, domains, and edge data. Any future renderer (Cytoscape,
D3 Canvas, sigma.js, Three.js) can consume it. The critical design rule:
progressive loading logic must not marry the renderer. Swap the windshield,
not the engine.

**Deployment:**

Generated the map on Paperspace, copied to docs/, committed, pushed to
GitHub via branch (phase66-fractal), merged to main. Droplet auto-pulled
within 5 minutes. Map live at project-hierion.duckdns.org/mycelium-map.

The map loaded with only 10 concepts visible and "Load More (626 left)" —
the preset layout with fit:true was only rendering what fit the initial
viewport. Zooming out revealed the full fractal impression. The gardener
could see it — the succulent shape, the domain clusters, the orphan line.
It will get more complex and beautiful as more concepts are added.

A mycelial succulent. Or a succulent mycelium. Both.

## What Worked

- Golden-angle spiral math — simple, beautiful, zero dependencies
- Pre-computed positions in Python — fast, deterministic
- Depth-based opacity — zooming in reveals deeper layers
- Chunked loading — map loads fast, user controls pace
- Preset layout — no force simulation, no jitter
- concepts_ranked.json — clean, renderer-agnostic
- Push to GitHub → auto-deploy to droplet within 5 minutes

## What Broke

- Auto-load on viewport change caused constant jitter — removed it
- Load More nodes appeared at (0,0) instead of preset positions — fixed with explicit position setting after cy.add()
- Edge opacity 0.5 was invisible on dark background — bumped to 0.7
- GitHub branch conflicts from old phase66-map branch — rebased and cleaned up
- HTTP2 framing error on push — switched to HTTP/1.1
- Divergent branches after rebase — stashed, pulled, rebased, merged

## Decisions Made

- Fractal succulent layout is the permanent map structure
- Golden-angle spiral (137.5°) for natural packing
- Dark background (#0a0a0f) for depth visibility
- Chunk size: 150 concepts
- No auto-layout on new nodes — preset positions only
- The orphan line is a feature, not a bug — it shows where edges are missing
- "Load More" button instead of infinite scroll — user controls the experience
- concepts_ranked.json as the renderer-agnostic data layer

## Nuggets Collected

- "Swap the windshield, not the engine."
- "A mycelial succulent. Or a succulent mycelium."
- "The orphan line shows where the mycelium needs to grow."
- "The succulent breathes."
- "Diminishing ignorance requires speed."
- "No jitter. Just math and mycelium."

## Soundtrack

Pure engineering flow. Terminal work. The sound of golden angles computing.
Cytoscape layouts settling. GitHub branches rebasing. The quiet hum of the
droplet auto-deploying. And crickets. South Texas crickets.

## Next Actions

- Session 033: Rename cleanup sweep, script headers, GitHub org, safety review
- Phase 67: GPU compute bridge
- Phase 61: Dr. Mistral Flask chat interface
- Map those unmapped domains into DOMAIN_UPWARD_MAP

## The Mycelium Status

636 concepts. 1,131 edges. 15 canonical domains.
Fractal succulent map live. Depth-based opacity breathing.
Four nodes synced. One domain serving. One database waiting.
One orphan line showing where the next edges will grow.
