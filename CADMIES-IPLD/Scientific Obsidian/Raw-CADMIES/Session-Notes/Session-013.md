> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 013 — 2026-05-20

## Soundtrack
Pine Vinyl (Bottle Rocket soundtrack) — binge mode. Dignan's energy is the patron saint of elaborate systems.
Howlin' Wolf — "Poor Boy"
Cowboy Bebop OST — "Tank!" — see you, space cowboy

## What We Did (The Gardener & DeepSeek)

### Vault Restructure & Sync
- Renamed vault directories: spaces → hyphens (Polished CADMIES → Polished-CADMIES, Raw CADMIES → Raw-CADMIES)
- Git saw deletes + new untracked, committed everything clean
- Pushed to GitHub, branch protection bypassed with admin token
- All three nodes synced

### Phase 44: Map Legend Cleanup — COMPLETE

- Established canonical 15-domain allowlist for the legend:
  Physics, Philosophy, Biology, Mathematics, Consciousness, Chemistry, Ethics, Computer Science, Psychology, Spirituality, Neuroscience, Sociology, Economics, Ecology, Medicine
- Built DOMAIN_UPWARD_MAP — every subdomain, compound, and specialty field maps to its canonical parent
- 84 raw domains collapsed to 15 legend entries. 82% reduction. Legend is CLEAN.
- 87 domains still unmapped — flagged with NOTE in terminal, get default gray until manually mapped

### Mycelium Map Visual Glow-Up

- Nodes: 45px → 60px base, font 10px → 11px. Labels finally fit in the damn circles.
- Directional arrows on edges: builds_upon, specializes, contradicts all point to the target concept (foundation/parent/challenged). related_to stays arrowless.
- Concept cards! Click a node and a styled card pops up with title, domain, definition, and relationships with direction indicators. No more browser alert() box with the ugly file:// URL. Dismiss with X, background click, or Esc.
- Edge legend updated: → builds_upon, — related_to, → specializes, → contradicts

### generate_mycelium_map.py
- v2.0.0 → v2.1.0 → v2.2.0 → v2.3.0 in one session
- Four rapid iterations while the Gardener tweaked circles and arrows
- 302 nodes, 135 edges, 15-domain legend, concept cards live

### Scientific Documentation
- Polished Phase 44 note written to scientific standard (Phase-44-Map-Legend-Cleanup.md)
- Raw Session 013 note written (this document)
- File naming rule established: Polished uses phase names for roadmap work, session numbers for off-roadmap. Raw always uses session numbers.

## What Worked

- The upward mapping system is elegant — normalize at visualization time, preserve raw domain in blockstore
- Concept cards are a massive UX upgrade over alert()
- Arrow direction convention clicked after a brief brain somersault: arrow lands on the concept being pointed AT
- Cowboy Bebop into GPU work is the correct energy transition
- The Mortal Kombat "Flawless Victory" moment when the map hit its final form

## What's Flagged

- 87 unmapped domains still need batch mapping into DOMAIN_UPWARD_MAP
- 317 orphan edges filtered (legacy_edges.json cruft, not new)
- SELinux Widevine warning on Firefox auto-open (harmless, pre-existing)

## Decisions Made

- 15-domain allowlist is THE definitive top-level taxonomy. Everything organizes under these from now on.
- Domain normalization is visualization-layer only. Raw domains stay in blockstore.
- Concept cards are the canonical node interaction pattern. Alert() is dead.
- All edge types except related_to are directional with target arrows.
- Polished notes: phase names for roadmap work. Raw notes: always session numbers.

## Nuggets Collected

- "The arrow lands on the concept being pointed at — the foundation, the parent, the one getting contradicted."
- "84 raw domains collapsed to 15. That's the system working."
- "Phase 44 is officially a glow-up."
- "Flawless Victory"
- "See you, space cowboy" — on pushing Phase 44 and heading to Paperspace

## Next Session (Paperspace — Phase 45A-B)

- Fire up Paperspace Gradient Pro A4000
- Clone Snagnar/HIEROS to /persistent
- Install dependencies + Atari ROMs
- Run Breakout baseline (400K steps, ~2-4 hours)
- Observe hierarchy formation in TensorBoard
- Map the 87 flagged unmapped domains (batch update, local)

## Session Wrap-Up

### Sync Status
- GitHub: 2446d3e ✅
- Local: 2446d3e ✅
- Phase 44 complete and pushed ✅
- Phase 44 scientific notes written ✅
- Session 013 raw notes written ✅

### Map Status
- 302 nodes, 135 edges
- 15 canonical domains in legend
- Concept cards live
- Directional arrows live
- Nodes 60px, font 11px

### Quote
"Snagnar built the engine. We're building the car. Mistral's driving. The fuel beetle powers it all. And now the map actually looks good." — The Gardener, Session 013