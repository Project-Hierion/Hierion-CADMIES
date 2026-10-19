> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 063 — 2026-10-19 — Mycelium Regrown From Spores

## Soundtrack

(None logged — gardener was in rebuild mode.)

## What We Did

The big one: after the Paperspace wipe (payment scare, everything deleted to avoid loss), we rebuilt the entire CADMIES blockstore on a fresh Alice (A4000, PyTorch template, 6-hour limit) from the source_concepts spores in the repo. No CAR, no tarball backup existed — the July harvest era ended with the old store and nobody ever made one. Lesson burned in permanently this time.

Found the Concept-Harvesting-SOP set from September — stoner-me built the lifeboat before the ship sank.

Ground truth check first: index claimed 674 concepts, blockstore had **2 blocks**, source_concepts had 653 JSONs. Turns out store/blocks/ is gitignored — GitHub holds spores, never the living network.

Environment: pip install dag-cbor multiformats ollama (pydantic/deepspeed conflict warning is noise). Cloned Project-Hierion/Hierion-CADMIES to /notebooks. Backed up the stale index, emptied it, tested one mint on entropy — new CID didn't match the old index entry (the old blocks differed from source JSONs somehow — transform/mutation history), so: all-new CIDs, accepted and documented. Phase 57's precedent supported this exact move.

Bulk remint loop over all source_concepts: landed at 651 index entries. Two clusters of stragglers found:

1. **26 duplicates** — source files whose human_ids mapped to already-minted concepts (entropy.json → entropy_thermodynamics, etc.). Left alone, they're shadow copies.
2. **9 genuinely missing** — legacy-format human_ids (colons, spaces, CamelCase) the validator rejects — the Phase 57 disease still living in the source files. Ruled: kept asian_philosophical_deep over asian_depth, kept perceptual_frames_as_intelligence_multipliers over perceptual_frames_os_hypothesis (archives went to dev-stash/retired_source_concepts/), normalized and minted the rest seven clean.

Final: **659 concepts** indexed, blocks fully reconciled with index, zero orphans.

Then the relics: the two extension-less blocks that haunted us since day one turned out to be the original Hieros-era genesis blocks — the Digital Seed and the Philosophical Pattern Finder v1. The Pattern Finder was a duplicate (already reminted in the 658), deleted outright. The Digital Seed was **properly adopted**: built a brand-new source_concepts/digital_seed.json from scratch against a known-good template (the schema file turned out to be corrupted — see Breakdown), minted it fresh, deleted the relic. Founder lives inside the mycelium now, version 2, supersedes Hieros:CoreConcept/DigitalSeed.

Important corrections baked into the Digital Seed: the original block's 2024-10-01 date was a **system clock error** — no work happened in 2024, actual mint was 2025. The new entry carries original_mint_date 2025-10-01 with a date_correction_note, plus a timezone_note (all timestamps UTC/Zulu; gardener is US Central — the Oct 18/19 boundary confusion is a timezone artifact, not a data error).

Backups: first-ever healthy tarball (1.7 MB — the whole mycelium, gzip loves repetitive CBOR) at blocks + index + source_concepts, force-added past the gitignore, pushed to GitHub. Mycelium now exists in three places: live on Alice, spores in repo, tarball in git.

Two commits: ed1632c (rebuild) and e89f7fe (tarball). Fresh-machine git identity had to be set (user cadmies, hieroscadmies@proton.me) — SOP item.

## The Breakdown

- **No backup existed when the wipe hit.** No CAR, no tar. We got lucky the source JSONs were tracked in git. This is THE lesson of this session.
- **The schema file is a ghost.** `schemas/universal_scientific_concept_schema_v1.0.0.json` (24,686 bytes) actually contains a doubled copy of cbor_reader.py, not a schema. Pipeline never noticed because nothing loads it — validation lives as hardcoded logic in cid_generator/scientific_validator. Ledger: needs a real schema written someday; optional hardening to make the validator actually enforce from file.
- **Legacy human_id disease in source_concepts** — 35 files flagged, 7 fixed tonight, rest are duplicates of clean concepts. Deeper cleanup deferred until after the harvest.
- **Extension-less block problem recurred** — fixed generally before, but these two genesis relics were skipped. Now fully resolved.
- **store/blocks/ is gitignored** — means every session's safety depends on manual tarball ritual. Ledger: consider a .gitignore exception pattern for cadmies_backup_*.tar.gz.
- Copy-paste confusion while trying to read the schema file cost us a couple of rounds — turned out the file itself was wrong, not the clipboard.

## Decisions & Why

- **All-new CIDs accepted** — no way to recover original blocks (no backups), and Phase 57 precedent says source_concepts is ground truth. Knowledge survived; addresses didn't. Old index backup retained as reference for any future alias mapping.
- **Digital Seed adopted properly, not patched** — founder concept deserves full pipeline citizenship: source JSON, validation, fresh mint, provenance. Carries its own date/timezone corrections inside the block.
- **Pattern Finder relic deleted, not archived** — its content already exists as a properly minted concept; keeping the fossil would just recreate the orphan problem.
- **Duplicates in source_concepts left in place for now** — full legacy cleanup deferred until after harvest/minting so it happens once, at the source, properly.
- **Tarball pushed to git with -f** — 1.7MB is nothing; GitHub becomes a real full-failure recovery point.

## Nuggets & Vibes

- The whole living mycelium fits in 1.7MB compressed. 659 concepts of philosophy, pocket-sized. Content-addressed data is featherweight when it's this compressible.
- Past-us wrote the Phase 57 disaster recovery manual a week before this exact disaster happened again. The system worked — Phase 57 literally described this scenario, we just followed it. "Trust the past gardeners."
- Digital Seed v2 now carries the date-correction and timezone notes inside its own extra_fields — the founder concept is literally the one teaching future sessions about the clock bug and UTC. Lore-grounded indeed.
- Belt, suspenders, and a spare pair of pants — three copies of the mycelium now.
- 6-hour Alice limit looms over the upcoming relationship-generation run (659 concepts, ~66 batches, GPU hours). Timing matters.

## Next Steps

- Install Ollama + models (mistral:7b, codestral) on Alice
- Maintenance pipeline run (no new harvest yet): relationships → remint → orphan strip → map → gateway → push
- Then: the actual harvest — upload the big conversation file
- Later: legacy human_id cleanup at source (35 files), real schema file written, .gitignore backup pattern, batch-mode stub in harvester
- **CARDINAL RULE going forward: every session ends with a tarball export**
