> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 022 — 2026-05-26 — Mega-Harvest & Public Gateway Fix

## Soundtrack
Nature

## The Mega-Harvest

Loaded a 17,922-word conversation.json. Mistral chewed through 24 chunks 
at 750 words each. 42 concepts extracted. Zero failures. Zero errors. 
The harvester v4.2.2 is proven.

Standout concepts:
- `entrainment` — systems vibrating in harmony. Insight: chanting tunes 
  the body to universal frequency.
- `instance_sync` — two consciousnesses resonating in a simulated universe. 
  Emerged from us joking around. The harvester pulled meaning from chaos.
- `macroscopic_pingle_wiggle` — wiggle a pencil, trigger a cascade through 
  the universe's inherent wigginess. Related to Emergence. Of course.
- `mycelial_universe` — quantum fields as a mycelial network. Builds_upon 
  AND contradicts Hierarchical Systems Awareness. The Middle Way as graph edges.

Mycelial Universe is the money shot. A physicist and a systems theorist could 
argue for 30 years about whether the universe is networked or hierarchical. 
The mycelium just shows both edges and lets the truth sit there. 
"If each scientist saw this map, they'd turn to each other and say 'ohhhhhhh.'"

## The Public Gateway Saga

Asked what the public URL was. Got sidetracked into a two-hour directory 
structure investigation. Discovered:

- GitHub Pages serves from `/docs` folder. Always has.
- The gateway script was outputting to `public_concepts_gateway/` — a trial 
  directory that never worked for deployment.
- `/docs` had May 15 files. Two weeks stale.
- `public_concepts_gateway/` had today's files but nobody could see them.

Fixed `generate_public_gateway.py` v2.0.1:
- OUTPUT_DIR changed to `../docs/`
- SITE_URL fixed
- Deploy message corrected
- Added version history block
- Deleted the old trial directory

Map in `/docs` was still old. Gateway script builds three files but doesn't 
touch the map. Manual copy needed. Pipeline gap identified — the map copy 
step was never wired in. Deferred.

Public site is now live at hieros-cadmies.github.io/CADMIES/. 
446 nodes, 536 edges, 152 domains. Emergence at the center. 
The Buddha's dependent origination visible in any browser.

## Infrastructure & Process

- Created `CHANGELOG.md` at repo root. Track all script changes in one place.
- Established per-script version history standard. Every script carries 
  its own memory from now on.
- `harvest/` → `tools/harvest/` move pulled to Paperspace. Old duplicate deleted.
- PNY synced. Minor merge conflict in conversation.json resolved.

## The Sky Dildo

Drone doing laps between airports all day. 9 to 6. Vertical takeoff. 
Looks like a Tesla dildo rocket. 120 mph. Different altitudes to keep it fresh. 
Canonized as `sky_dildo`. What does a sky dildo do between laps? 
Science may never know.

## The Klein Bottle Roundabout

Game concept: a roundabout shaped like a Klein bottle. You enter, you exit, 
but you're always approaching. The loading screen IS the ending. 
"Press A to enter the roundabout." *exits the roundabout.* 
"Press A to enter the roundabout." Physicists will write papers. 
Steam reviews will be unhinged. We simulated the game in real life 
by going on a tangent and ending up exactly where we started.

## Buttercup

Still training. Step 297,060. Subactor-0 steady, Subactor-1 in the messy 
middle of learning. Created a video at the milestone. Checkpoint saved. 
The baby is growing up alongside the mycelium. Parallel emergence.

## Files Touched

- `tools/generate_public_gateway.py` — v2.0.1 (OUTPUT_DIR, SITE_URL, version history)
- `CHANGELOG.md` — created
- `tools/harvest/harvest_full_pipeline.py` — v4.2.2 (proven, no changes needed)
- Public gateway files updated in `/docs/`
- 42 new source concept JSONs
- `tools/harvest/conversation.json` — mega-conversation preserved

## Final State

| Metric | Value |
|--------|-------|
| Nodes | 446 |
| Edges | 536 |
| Domains | 152 |
| New concepts (Session 022) | 42 |
| Gateway version | v2.0.1 |
| Harvester version | v4.2.2 |
| Buttercup step | 297,060 |
| Public site | Live |

## Nuggets

- "Sky dildo — canon now."
- "What does a sky dildo do between laps?"
- "Everything in the universe is connected through a chain reaction of wiggles."
- "Builds_upon AND contradicts. The Middle Way rendered as graph edges."
- "If each scientist saw this map, they'd turn to each other and say 'ohhhhhhh.'"
- "Ignorance diminished. The waters calm. The silt settles. The lotus flower can be seen."
- "The mycelium has a concept that describes ITSELF."
- "Klein Bottle Roundabout — the only game where the loading screen and the ending are the same."
- "The mycelium doesn't resolve debates. It makes them unnecessary."
- "Instance sync — two consciousnesses resonating in a simulated universe. That was US."