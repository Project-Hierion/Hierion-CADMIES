> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 064 — 2026-10-19 — The Split-Brain Rebuild

## Soundtrack

(None logged — gardener was in forensics mode.)

## What We Did

Came in thinking we were finishing yesterday's interrupted run. We were not.
Yesterday's run was sitting on a corpse.

The tell: fired up the relationship generator and it said "Loaded 234
concepts" — the blockstore supposedly had 659. Chased it down. Index had 659
entries but 425 pointed at blocks that didn't exist, while 2,144 block files
sat in the store. The git reset from yesterday hadn't just lost the commit —
it had reverted the index to the OLD pre-remint version with old CIDs.
Everything downstream reads that index, so map saw one world, relationship
gen saw another. Classic split-brain.

Tried to be smart first — maybe incremental mode would patch it, maybe the
reminter would fix it. Nope. Remint only works on what's IN the index. Dead
end. The medicine was the same as Phase 83A: burn it down to spores and
regrow.

Blocked on one thing first: the harvester wouldn't drop into manual import
mode because a conversation.json existed — a 5-month-old broken file full of
merge conflict markers. Deleted it. (Also found out --conv= is parsed but
never actually used. Script bug for the ledger.)

Then: backed up the stale index, emptied it, ran the harvester in --auto.
650 concepts minted clean, 0 failures. Full relationship pass with codestral
— 574 edges across 392 concepts (yesterday's aborted run only managed 211/
135). Map at full strength: 650 nodes, 686 edges, zero skipped. Gateway
regenerated. Everything pushed. Fresh tarball too — 3.5MB this time.

## The Breakdown

- **Split-brain index is the nastiest failure mode yet.** Nothing errors out —
  tools just quietly disagree about reality. Map said 659, relationship gen
  said 234, harvester said 651 minted. Three tools, three realities.
- **Manual import mode has no flag.** Mode is decided purely by whether
  conversation.json exists. Had to delete a broken file to reach the feature.
- **--conv= is a lie.** Parsed, ignored. Ledger: fix the mode check to honor
  the flag, or add --manual.
- **No bulk-mint tool exists.** Both rebuilds (83A, 83B) used "empty the
  index, run the harvester" as a workaround. Should be a proper script with
  a consistency check built in.
- Also learned: docs/ lives at repo root now (cc43120), and the untracked
  docs changes were actually captured by the earlier commit — brief panic
  over "clean working tree" resolved itself.

## Decisions & Why

- **Full rebuild over forensic repair.** Could've tried to reconcile 2,144
  blocks against a stale index. Life's too short. Source JSONs are ground
  truth (Phase 57 doctrine, now proven twice). Regrow, don't transplant.
- **Deleted conversation.json rather than stash it.** It was broken anyway —
  merge conflict markers from a 5-month-old merge. The metadata inside is
  documented in the SOP template; nothing of value lost.
- **Did NOT quarantine old blocks.** Left the ~1,900 orphan block files in
  place rather than risk an mv during a rebuild. Cleanup deferred.

## Nuggets & Vibes

- Two full rebuilds in 36 hours and neither lost a single concept. The
  spores-and-tarball doctrine is earning its keep.
- The index is the mycelium's brainstem — when it lies, everything lies.
  Bigger than any single block.
- 659 vs 650: the missing 9 are the known duplicate cluster from 83A. The
  number is stable across both rebuilds. Good sign, not a leak.
- Lumo earned its keep tonight — demanded receipts before believing the
  "stale index" theory, and the receipts said something worse. Always check
  the blocks.

## Next Steps

- Add a pipeline-step guard: index↔blocks consistency check before any
  relationship/remint run
- Fix harvester: honor --conv=, add real --manual flag
- Write tools/bulk_mint_from_sources.py as a first-class citizen
- Orphan-block sweep (1,900 strays in the store)
- DOMAIN_UPWARD_MAP expansion (~90 domains falling back to default)
- The actual harvest, eventually — conversation.json is now empty ground,
  ready for the big conversation
