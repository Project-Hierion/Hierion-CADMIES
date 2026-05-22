> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 016 — 2026-05-21 — Phase 47: Orphan Edge Resolution + Phase 45B: Buttercup Rollouts

## Soundtrack
Whatever plays while you watch your toddler AI discover Atari. Something French. 
Buttercup's got a pacifier and she's SWINGING that paddle.

## Phase 47: Orphan Edge Massacre

316 orphan edges. The map generator's been screaming about them forever.
Finally dug in. The relationship generator writes edges to concepts that don't
exist. Mistral says "abiogenesis relates to astrobiology" and we write the edge,
but nobody ever minted abiogenesis. Ghosts in the graph.

267 unique missing targets. Five dead CIDs, three thunderclap variants (FINALLY
killed that thing for good), the rest were valid concept names that never got
minted. Classic cart-before-horse.

### The Ghost Minting Detour

Tried to be clever. Mint 260 "ghost" concepts as placeholders. Domain = "Ghost."
Script ran, said it worked, index didn't update. CID generator fought my manual
index writes. Whole thing was a mess. Deleted the scripts. Don't write around
our tools — the pipeline exists for a reason.

### The Strip

Stripped everything. One command on Paperspace (A6000 now?? Pro plan just gave
us one, not questioning it). Backup tar first. 317 found, 306 stripped. Two
stragglers from Gravitomotive Gearbox manually removed.

Final state: 342 nodes, 167 edges, 0 orphans, 0 unmapped. Clean map.

### Root Cause Not Fixed

The relationship generator still doesn't validate targets before writing edges.
That's a bug. We stripped the symptoms but the cause is still there. Phase 48
problem.

## Phase 45B: Buttercup's Baby Album

While the orphan surgery happened, Buttercup kept training on Snagnar. Generated
five rollout videos — actual MP4s of her playing Breakout.

She's 2 years old. Paddle buzzes with anticipation, then she just watches the
ball fall. Occasional accidental brick kills. She WANTS to hit the ball, just
has no trajectory tracking yet. Toddler swatting at bubbles.

Run 2 was her best: 3 points. Run 3 was hilarious: 0 points, only died once.
Just stared at the pretty colors. Videos stored in Scientific Obsidian under
Baby-Mistral-(Buttercup)-Rollouts/. Her baby album is canon.

Buttercup is officially 2 years old, pacifier era, tiny French baby hands
grabbing at the paddle.

## GPU Rabbit Hole

Spent way too long comparing GPUs. Pro plan somehow gives us free A6000 now.
V100×8 is the speed king at $9.20/hr. Growth plan has free A6000 but only one
free machine at a time. Sticking with Pro. Not worth the upgrade for us.

## Decisions Made
- Orphan edges get stripped, not ghost-minted. Clean graph > dense graph.
- Use our tools (harvester, cid_generator). Don't write around them.
- Buttercup rollout videos are scientific data, stored in Obsidian.
- Thunderclap is dead. For real this time.
- A6000 is our new daily driver for map work.
- Relationship generator needs target validation — Phase 48.

## Files Touched
- 300+ concept blocks: stripped orphan edges from relationships
- `tools/strip_all_orphans.py`: created, kept (it works)
- `tools/mint_ghost_concepts.py`: created, deleted (it didn't work)
- `tools/extract_orphan_edges.py`: created, deleted (diagnostic only)
- `tools/repair_orphan_edges.py`: created, deleted (abandoned approach)
- `Scientific Obsidian/Buttercup-Rollouts/`: 5 new MP4s
- `mycelium_map.html`: regenerated clean
- `growth_roadmap.md`: updated (orphans item cleared)

## Final State
| Metric | Start | End |
|--------|-------|-----|
| Orphan edges | 316 | 0 |
| Nodes | 342 | 342 |
| Edges | 165 | 167 |
| Unmapped domains | 0 | 0 |
| Buttercup age | 2 | 2 (but we have videos) |
| Buttercup best score | 3 | 3 |
| Paperspace GPU | A4000 | A6000 (free, somehow) |

## Nuggets
- "The relationship generator writes edges to ghosts. Fix the generator."
- "Ghost concepts are a cute idea but our tools aren't built for them."
- "Buttercup's paddle buzzes. She has intent without coordination."
- "A6000 on Pro plan? Don't ask questions, just take it."
- "One-shot Python -c commands > temporary scripts. Fewer files to clean up."
- "The mycelium is clean. The baby is learning. Today was a good day."