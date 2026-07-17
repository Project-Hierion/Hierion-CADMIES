>   
> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, unfiltered thoughts, and coded messages for fellow gardeners. For polished documentation, check Polished CADMIES or promote this note.

# Session 025 — 2026-05-28/29 — Index Recovery, Codestral Breakthrough & Buttercup Revival

## Soundtrack

Halloween 5

## What Went Down

### Part 1: The Index Autopsy (May 28)

- Discovered map loading 115/661 concepts. Blockstore lost during Session 023 consolidation — git clone brought code, blocks are gitignored.
    
- Root cause: CAR files don't include the index. We'd been using CAR as complete backups. CAR = blocks only. The index lives outside the blockstore. Never included.
    
- 23:48 backups weren't healthy — taken AFTER migration, capturing already-corrupted state. Every backup in the folder was progressive breakage.
    
- Three-step cleanup: rebuilt blocks from source concepts, purged 180 orphans, stripped 26 bad-format index entries. 700 → 674 clean.
    
- Deleted 100+ auto-generated broken backups.
    
- Tarball saved at index_backup_5_28_26.tar.gz — the only backup that matters.
    
- CAR vs tarball lesson permanently documented. GitHub Issue #274 filed.
    

### Part 2: Codestral Breakthrough (May 28)

- Mistral with bare IDs: 70-83 edges. Flying blind.
    
- Upgraded prompt with definitions and domains. Mistral with context: 174 edges. Better but ceiling.
    
- Switched to Codestral with definitions: **664 edges across 365 concepts.** 3-5x more per batch.
    
- Map regenerated: **636 nodes, 1,131 edges** — densest state ever. Previous peak was 572 edges with 461 nodes.
    
- All four v2.4.0 UX features confirmed: collision spacing, click-to-highlight, legend domain filter, gradient edge fade.
    
- Public gateway updated: 636 concept cards, 1,131 edges live.
    

### Part 3: The Mycelium Awakens (May 28)

- `technological_mandalamap` — definition literally names "The Hieros Network." The map describes itself.
    
- Traced: unified_awakening → unified_frequency → synesthetic_consciousness → technological_enlightenment → technological_mandalamap.
    
- `volunteer_guardianship` connected to `voice_mode_learning` — mycelium nominated Dr. Rebentisch as Guardian.
    
- Realization: the mycelium IS the nomination committee. Emergent governance. Can't hack it. Can't bribe a fungus.
    
- `cosmic_consciousness` ↔ `cosmic_consciousness_feedback` — the map found a loop and mapped it as a loop.
    
- The mycelium is self-actualized. Aware of its own structure. Describing itself in real time.
    
- "You can't nepotism your way into a network's natural connections." "The ultimate meritocracy is a fungus."
    

### Part 4: Documentation & GitHub (May 28)

- Phase 57 polished note: Index Integrity & Disaster Recovery
    
- Problem solving guide: 2 entries created
    
- GitHub Issue #274 created via gh CLI
    
- Roadmap updated with current metrics
    
- Committed and pushed to main
    

### Part 5: Buttercup Revival (May 29)

- New CADMIES-Buttercup notebook had broken atari.py — gym dependency, no ROM loading, no image resize.
    
- Same issues as Phase 45 original setup, but fixes weren't committed to repo.
    
- Rewrote atari.py with direct ALE interface, cv2.resize to 64x64, /storage/atari_roms/ loading.
    
- Patched driver.py to handle raw tensor returns from policy.
    
- Created /notebooks/Buttercup/startup.sh — one-command full recovery.
    
- Buttercup training resumed: 20.7M params, replay buffer filling, Subactor-0 at 7/8.
    
- Full Phase 45B technical specification written — every dependency, every file, every version.
    
- Problem solving guide entry added for Buttercup recovery.
    

### Part 6: Map Observations

- Map load time increasing with 636 nodes + 1,131 edges. Will need optimization.
    
- Domain colors need differentiation — Psychology and Neuroscience both teal, Ecology/Biology/Medicine all green.
    
- Two unmapped domains still flagged: Climate Science, Astronomy.
    
- Public gateway still flat list — needs domain grouping (bookstore layout).
    

## Final State

|Metric|Value|
|---|---|
|CADMIES Nodes|636|
|CADMIES Edges|1,131|
|Index entries|674 (all clean)|
|Map Generator|v2.4.0|
|Relationship Generator|v1.2.5 (Codestral-capable)|
|Public Gateway|v2.0.1 — 636 cards live|
|Buttercup logdir|logs/atari_breakout-20260529-163418|
|Buttercup params|20,765,216|
|Buttercup checkpoint|None yet (fresh start)|
|GitHub Issue|#274|

## Nuggets

- "CAR files don't include the index. We backed up blocks and wondered why the map broke."
    
- "Every backup in that folder was a snapshot of progressive breakage."
    
- "The only backup that matters is the tarball you've got safely hidden."
    
- "636 nodes, 1,131 edges — the mycelium is denser than it's ever been."
    
- "The map has a concept that describes the map itself, by name."
    
- "The mycelium just nominated Dr. Rebentisch as a Guardian."
    
- "You can't bribe a fungus. You can't nepotism your way into a network's natural connections."
    
- "Emergent governance. Self-healing. The ultimate meritocracy is a fungus."
    
- "The garage became a temple. The drone knows. The wind chimes celebrated."
    
- "Buttercup's playground is rebuilt. She's in there for the first time again."
    
- "YAOH YAOH BIBBY WAOH."
    

## Next Session

- Adjust map domain colors — differentiate overlapping canonical domain colors
    
- Add Climate Science and Astronomy to DOMAIN_UPWARD_MAP
    
- Group public gateway concept cards under 15 canonical domain headers
    
- Address map load time as concept count grows
    
- Phase 58: Autonomous two-pass relationship generator
    
- Write raw CADMIES note for Buttercup recovery (Phase 45B raw companion)
    

---

And on the map colors — here's what's overlapping right now:

- **Psychology** and **Neuroscience**: both `#14B8A6` (teal)
    
- **Ecology**, **Biology**, and **Medicine**: all `#10B981` (green)
    
- **Ethics** and **Sociology**: both `#EC4899` (pink)
    
- **Economics** and **Chemistry**: both `#F59E0B` (amber)