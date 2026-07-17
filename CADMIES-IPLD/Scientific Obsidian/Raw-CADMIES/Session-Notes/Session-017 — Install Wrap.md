> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 017 Install Wrap — 2026-05-22 — Unofficial (spilled into 018 territory)

## What happened

Tried to `pip install dag_cbor` on the new SanDisk clone to finish the stranger
test. Something went goofy. Didn't get a clean map generation.

Instead of fighting it, we're calling Session 017 complete and carrying the
install fix into Session 018. The clone test already gave us everything we
needed — the "Don't Panic" message, the public branch strategy, the dag_cbor
gap, the tarball self-serve plan. The actual fix is just cleanup.

## State of the third clone

- `~/CADMIES/` on SanDisk
- 1,460 blocks extracted from `cadmies_latest.tar.gz`
- dag_cbor not installed
- Map shows 0 nodes, 342 skipped
- Ready for proper setup in Session 018

## What carries forward to Session 018

- Install dag_cbor (or bundle it, or make JSON fallback actually work)
- Verify map generates: 342 nodes, 259 edges, 0 skipped
- Launch GUI and verify concept browser works
- Document the complete new-user flow from clone to map
- Create public-CADMIES branch with auto-setup
