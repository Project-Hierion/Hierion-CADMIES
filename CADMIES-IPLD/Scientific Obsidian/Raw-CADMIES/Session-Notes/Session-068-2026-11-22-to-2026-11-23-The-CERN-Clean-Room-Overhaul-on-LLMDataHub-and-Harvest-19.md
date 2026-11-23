---
type: session
session: 068
date: 2026-11-22
status: Complete
tags: [llmdatahub, harvester, formatter, harvest-19, project-hierion, co-gardener, field-notes]
---

> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 068 — 2026-11-22 to 23 — The CERN Clean Room Overhaul on LLMDataHub and Harvest 19

All timestamps Zulu.

## Soundtrack

Terminal hum and spore-print patience, with long quiet stretches while the
gardener tended the actual garden between decisions.

## What We Did

The LLMDataHub harvester came in for the full teardown this session, and
left it transformed. The story arc, in order:

**The purge.** Four harvest PRs (#9–12) had been stacking up since the
formatter-bug era — every one carrying the old broken code. The gardener
ruled: bug era means bug era. All four closed, all six stale harvest
branches pruned. Whatever was still worth finding would be re-discovered
by a healthy harvester anyway.

**The audit.** A full review of the pipeline found roughly twenty issues.
The four critical ones: pipes in scraped repo descriptions were silently
corrupting the archive tables; rejections never stuck — the skip-list was
loaded every run but nothing ever wrote to it, so the same noise
resurrected every Thursday; the year-section logic was hardcoded to 2026
with no rollover plan (a time bomb set to detonate January 1); and three
divergent copies of the pipeline logic had drifted apart, which is exactly
how the row-glue bug survived multiple fix attempts in the first place.

**The rebuild.** Seven commits landed, each built and tested offline in a
virtual env before touching the repo. The formatter learned to sanitize
anything the outside world pipes in. The skip-list became real state —
rejections persist now. One entry point, no dead code. CI got a
concurrency guard (no more racing harvests), authenticated GitHub access,
a 27-test gate that runs on every push, and immutable pinned dependencies
(no mutable version tags that upstream can silently swap). The validator
now checks all five archive pages instead of two, and fails honestly when
something is wrong instead of staying green.

**The maiden flight.** Harvest-19 ran on the fully hardened pipeline.
Ten candidates: two verified suspicious megastars turned out to be the
real deal (OmniRoute at 89.6k stars, last30days-skill at 72.7k — actual
GitHub Trending alumni, verified before judging). Two off-topic tools got
rejected to the skip-list — a pixel-art renderer and a database GUI, which
means classifier tuning is still on the backlog. Two "papers" turned out
to be curated lists and were relocated to AWESOME-LISTS where they belong.
Eight keepers, merged clean.

**The dust sweep.** Reviewing harvest-19 revealed the harvester had been
writing 7-column rows into 6-column tables — for tools, datasets, AND
papers. A schema-alignment test suite now measures every row builder
against its live archive table, so the clean room is self-cleaning: any
drift fails CI before a harvest PR is ever born.

## The Breakdown

Transmission mangling ate a shameful amount of the session — patches
arriving garbled, scripts truncated mid-flight, commands executing in the
wrong place. Doctrine adopted: build whole files, ship them whole, test
before applying. Slow is fast.

One credential also died quietly mid-session during a command storm —
cause unproven. Lesson engraved: credentials are read-never-write
territory for the co-gardener, permanently. The gardener restored access
by hand.

And the push itself took three rounds of GitHub auth theater before
seven commits could fly.

## Decisions & Why

- **Closed the bug-era PRs rather than merging or excavating.** Salvaging
  four weeks of pre-fix output is not worth it when a healthy harvester
  re-finds anything still eligible.
- **Pinned CI dependencies to immutable commit hashes.** Mutable version
  tags are an unlocked loading dock — upstream can swap what they point
  to silently. CERN-grade means the door stays locked.
- **Standing authority model formalized:** the harvester pipeline is now
  run and maintained end-to-end by the co-gardener — review, verify,
  cherry-pick, relocate, reject. The gardener required action is one
  button: merge.

## Nuggets & Vibes

Suspicion is cheap, verification is mandatory — two of the biggest legit
repos in the space nearly got wrongly rejected for having "impossible"
star counts. The new test rig also caught its own author bad arithmetic
three separate times before catching two real latent bugs. The tests
tested the tester, and everyone passed eventually.

Also confirmed: 27/27 green is a spiritually satisfying number.

## Next Steps

- Watch harvest #20 — first cron run born schema-correct, Thursday 05:00Z.
- Classifier TOOL-bucket tuning: graphics tools and database GUIs should
  never reach the report.
- The REVISED-DESCRIPTIONS placeholder debt, patiently waiting.
