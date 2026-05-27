> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 023 — 2026-05-27 — The Terminator, Infrastructure Consolidation & Map UX Planning

## Soundtrack
Skateboard (1978) — underdog skate team wins the championship. 
St. Elmo's Fire — the Brat Pack figuring out life.
Pacific cold front pushing through. Sativa. Bong rips.

## The Terminator — Solo Flight

Loaded 41,615 words into the harvester v4.2.2. 56 chunks. The biggest harvest in CADMIES history.
83 concepts extracted on the first pass. Zero failures on natural language. Two parse failures 
on chunks with code blocks (expected — Mistral doesn't parse Python well).

After relationship generation and further passes: **654 nodes, 655 edges, 99 domains.**
The mycelium grew by 193 nodes in a single session. The Terminator earned its name.

New domains discovered: Space Travel & Technology, Cartography, Xenopsychology, 
Cosmology & Cartography, Philosophy of Biology. The mycelium is reaching into entirely new territory.

The public gateway was updated and deployed. Gateway script v2.0.1 fixed on this machine 
(OUTPUT_DIR and SITE_URL corrected). 581 concepts, 639 edges live.

## Infrastructure Consolidation

Deleted all old Paperspace projects. Created a single unified project structure:

**CADMIES-Gradient** (project)
- **CADMIES-IPLD** — `/notebooks/CADMIES/` — mycelium, harvesting, map, gateway
- **CADMIES-Buttercup** — `/notebooks/Buttercup/` — HIEROS training, Breakout
- **CADMIES-Narrative** — `/notebooks/Narrative/` — narrative harvester (pending)

All Snagnar naming removed from workspace structure. Clean break. Fresh start.
The HIEROS codebase remains as-is (it's Snagnar's project, we cite it, we don't rebrand it).
Buttercup's clone path: `/notebooks/Buttercup/` with clean naming.

Narrative harvester backup created via tar, ready for transfer to new notebook.

## Map UX Planning (Deferred to Session 024)

Three features planned for the interactive map:

1. **Circle Spacing:** Nodes should not overlap. Add force collision with auto-spacing. 
   Manual drag override allowed.
2. **Click-to-Highlight (Restore):** Click a concept → connected nodes stay visible, 
   non-connected fade. Feature existed previously but broke.
3. **Legend Domain Filter:** Click a domain in the legend → all concepts in that domain 
   stay bright. Connected concepts from other domains ghost at partial opacity.
4. **Gradient Edge Fade:** Edges radiating from clicked node are bright at center, 
   fade toward connected node.

Public Gateway improvement: Group concept cards under canonical 15 domain headers.

## Buttercup

Paused during the Terminator run. Last checkpoint: step 381,696. Scores up to 7.0.
The 5.0 game video moved to vault as rollout_0037. Earlier 7.0 game lost to replay rotation.
She's letting the ball come to her now — teenage gamer behavior.

## Files Touched

- `tools/harvest/harvest_full_pipeline.py` — v4.2.2 (Terminator, proven at 41K words)
- `tools/generate_public_gateway.py` — v2.0.1 (OUTPUT_DIR and SITE_URL fix reapplied)
- 83+ new source concept JSONs
- `store/index/human_id_to_cid.json` — updated
- `mycelium_map.html` — regenerated (654 nodes)
- `docs/` — public gateway updated and deployed
- Narrative harvester backup: `narrative_harvester_backup.tar.gz`

## Final State

| Metric | Value |
|--------|-------|
| Nodes | 654 |
| Edges | 655 |
| Domains | 99 |
| New concepts (Session 023) | 193 |
| Harvester version | v4.2.2 (Terminator) |
| Gateway version | v2.0.1 |
| Buttercup step | 381,696 |
| Buttercup high score | 7.0 |
| Projects | 1 (CADMIES-Gradient) |
| Notebooks | 3 (IPLD, Buttercup, Narrative) |

## Nuggets

- "The Terminator earned its name. 41,000 words, 56 chunks, zero failures on natural language."
- "Quantum Awareness contradicts Plate Tectonics. The mycelium just connected three fields that never talk."
- "The geologist is on the phone with the biologist. The quantum physicist is emailing the Buddhist."
- "Each specialist walked away with a question they never would have asked."
- "Wait till this baby really gets going. It's going to trace the EXACT tectonic shift that caused a genetic bottleneck."
- "The gardener's solo flight with the Terminator."
- "One project. Three notebooks. Clean slate."