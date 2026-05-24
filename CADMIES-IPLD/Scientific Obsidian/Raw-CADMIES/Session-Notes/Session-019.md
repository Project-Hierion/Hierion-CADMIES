> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 019 — 2026-05-23 — Phase 43/50C: Remint & CAR Resolution + Buttercup A6000 Push

## Soundtrack
Gnarls Barkley — "Crazy." Warren Zevon — "Werewolves of London." 
The Rolling Stones — "Paint It Black." Jax Jones — "You Don't Know Me."
Texas two-week storm finally breaking. Lightning strikes. Thunder applause.
The universe DJ'd the entire session.

## Phase 43/50C: Remint & CAR Resolution

### The Remint

Reminted 153 HOG-era blocks with proper CIDv1 using `remint_existing_concepts.py` v2.0.0.
Script adapted from Phase 29 normalization tool. Scans all concepts, computes correct
CID via `hashlib.sha256(dag_cbor.encode(concept)) + multihash.wrap`, re-saves blocks
under new CIDs, deletes old files, updates index, preserves provenance.

Two ghosts remain: `ai_llm_mycelium_reader_willie_the_librarian_v1` and 
`epistemology_concept_perceptualframesasintelligencemultipliers` — index entries
without block files. Harmless. Map generator skips them gracefully (340 nodes, 2 skipped).

### The Persistent Verification Discrepancy

Discovered that `car_utils.calculate_cid()` and `remint_existing_concepts.compute_current_cid()`
produce different CID strings despite using identical algorithms. Both use `hashlib.sha256` +
`multihash.wrap` + `CID("base32", 1, "dag-cbor", mh)`. Codestral 22B consulted — confirmed
both methods SHOULD produce identical output. They don't.

Root cause narrowed to: the remint script hashes `dag_cbor.encode(concept)` where `concept`
is a freshly loaded dict. `car_utils` decodes raw bytes to a dict, re-encodes, then hashes.
Despite `raw == normalized` being True, the two code paths produce different multihash byte
structures. This is a code alignment bug, not data corruption. The CAR pipeline works.
The map generator works. The user never sees it. Deferred to future session.

### CAR Pipeline Status

CAR pipeline proven end-to-end: export, download, import, map generation all work for users.
Index conflicts are expected when updating — resolved via Option A (clean replace) for
public users, Option B (provenance preserved) for dev pipeline.

`car_utils.py` patched to v1.0.2 (hashlib fix + re-encode verification).
`cadmies_latest.car` rebuilt after remint. 340 blocks, 3.2MB.

## Architecture Decisions

- Two branches: `main` (dev) + `public` (user)
- Hybrid CAR strategy: Option A for users (clean), Option B for dev (provenance)
- User publishing: delta CARs for sending updates back (future tool)
- `incoming_cars/` replaces `temp_tarz/` as the official CAR import directory
- All four nodes synced, all stray branches deleted (7 patch branches + 1 local)
- Single `main` branch across all nodes

## SanDisk Clone Test (Real-Life Trial)

Fresh clone on SanDisk (`~/CADMIES/`). Venv created. dag_cbor installed. 
CAR imported from `incoming_cars/cadmies_latest.car`. Index conflicts surfaced
because SanDisk's git-tracked index had old CIDs while CAR had newly reminted CIDs.

Conflict resolution strategy designed:
- **Public users:** Delete old blocks/index, import fresh CAR (Option A — clean replace)
- **Dev pipeline:** Merge with provenance chains (Option B — keep history)
- **Hybrid:** CAR releases use Option A. Dev machines use Option B.

First CAR ever placed in `incoming_cars/` directory. History. Texas storm providing
the soundtrack.

## Buttercup Update — A6000 Training Push

Resumed training on Snagnar project with A6000 (48GB VRAM), batch_size=16 
(matching paper config). Performance jump: 2.42 FPS (A4000) → 7.18 FPS (A6000).
Nearly 3x speedup. New log directory: `atari_breakout-20260523-235408`.

**Progress at 107,912 steps:**
- First confirmed intentional brick hit with celebratory paddle shake
  (video: `buttercup_20260524T020541.mp4`)
- Multiple intentional hits across consecutive games
- Trajectory tracking: solid. Sees the angle, knows where to go.
- Motor control: developing. Gets to right spot but sometimes too slow.
- Chaos management: still thrown by unpredictable bounces and deflections.
- 18 new .npz files from tonight's session converted to MP4, stored locally.
- 17 total videos in local training folder, 5 in Obsidian vault.

**Age assessment:** 3-4 years old. Out of pacifier era. Intentional but 
inconsistent. Knows what the paddle does. Tries to hit the ball. Sometimes 
succeeds. Celebratory paddle shake is canon.

## The Humanism Recurring Theme

Got flagged as "seems generated" by Snagnar. Got flagged as "bounty scout candidate"
by GitHub autopilot. Got flagged on Reddit as a sales bot. Three times now the
internet has mistaken genuine human warmth for AI-generated content. The mycelium
is so human it wraps back around to looking artificial. The Turing test in reverse.

Reply to Snagnar sent with proof: Buttercup videos, training logs, repo link.
"I promise I'm a real human, I just use DeepSeek for work and for more effective
communication." If they still don't believe, Dr. Rebentisch's twin mycelium is
the ultimate receipt — two humans on two continents arriving at the same architecture
independently. You can't bot convergent evolution.

## Files Touched

- `tools/remint_existing_concepts.py` — v2.0.0 (adapted for stale CID reminting)
- `tools/car_utils.py` — v1.0.2 (hashlib fix, re-encode verification)
- `store/index/human_id_to_cid.json` — 153 entries updated
- 153 block files renamed with new CIDs, old files deleted
- `incoming_cars/` — first CAR file placed
- `cadmies_latest.car` — rebuilt after remint
- 18 new Buttercup MP4s rendered and downloaded
- All stray branches deleted (7 remote + 1 local)

## Final State

| Metric | Value |
|--------|-------|
| Nodes | 340 |
| Edges | 259 |
| Orphans | 0 |
| Ghost concepts | 2 (harmless) |
| CAR file size | 3.2 MB |
| Buttercup steps | 107,912 |
| Buttercup FPS | 7.18 (A6000) |
| Buttercup age | 3-4 |
| Buttercup intentional hits | Confirmed |
| Nodes synced | 4 |
| Branches | 1 (main) |
| Times flagged as bot | 3 |

## Nuggets

- "The CID bouncer checked the ID and said 'nice try kid, that's your mom's license.'"
- "153 HOG-era blocks reminted. The ghosts are documented. The pipeline works."
- "The mycelium is so human it wraps back around to looking artificial."
- "You can't bot convergent evolution. Dr. Rebentisch is the receipt."
- "Buttercup did a celebratory paddle shake. That's not random. That's joy."
- "The Texas storm provided the soundtrack for the first CAR import."
- "I promise I'm a real human, I just use DeepSeek for work."
- "Full visibility, scientific rigor, unadulterated typos available upon request."
- "Paint the CARs black. The flowers grow through the asphalt."