> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 063 — 2026-10-29 (≈02:52Z) — Droplet Dev Environment and Double Harvest Pruning

## NEW DOCUMENTATION CONVENTION (effective this note, onward)
All documentation now carries Zulu time (UTC) timestamps. Local time is
dead to us; the mycelium runs on coordinated universal time now.
(Gardener's local at session end: 2026-10-28 21:52, but we speak Zulu now. =) )

## Soundtrack
Back-in-the-room energy after stepping away for a while. Quiet, methodical pruning music.

## What We Did

Two harvest PRs were waiting in the repo — the previous week's (PR #7)
and the newest (PR #8). PR #7 turned out to be a zombie: it was never
actually merged. Its pruning surgery was done two weeks ago, but the
merge button never got pressed. Worse, because a follow-up skip-list
commit had landed directly on main, the zombie branch was left with a
merge conflict in `rejected_candidates.txt`. It sat rotting for two
weeks while the archive quietly missed its three keepers.

Meanwhile, all the hands-on work this session happened on the Digital
Ocean droplet — the LLMDataHub repo now has a fully independent dev
environment there, strictly isolated from every other project on the
box per the sacred separation rule:

- Repo cloned to `~/LLMDataHub` (own tree, own clone, no sharing)
- Dedicated virtualenv at `~/LLMDataHub/.venv` (deps: pyyaml, requests — quarantined, deletable, zero leakage to system Python)
- Repo-scoped git identity configured (kept local to this clone only)
- Credential helper armed; push access verified end-to-end
- Environment proven by doing the entire harvest-8 pruning remotely

The PR #8 triage: 15 reportables (2 models, 13 tools, 64 noise —
classifier doing decent drowning work in the noise pool).

Kept two:
- `Goekdeniz-Guelmez/mlx-lm-lora` (437★) — MLX LLM trainer (MODELS)
- `AcademiaSD/AcademiaSD_LoRAlab-TrainerStudio` (106★) — LoRA training studio (TOOLS)

Skip-listed eleven: nightmare-mobile (image diffusion, not LLM),
datamimic (synthetic CI/CD test data), DuDuClaw (CLI-to-chatbot
wrapper), opencrabs (all-in-one agent platform, dify's cousin), cognee
(agent memory platform), nodus (research workspace), dsh-session-manager
(too meta), deepchat (generic assistant), trending-claude-skills
(repeat surfacing — see below), repo-harness (session harness meta),
cogneva (multi-agent digital employees).

Zombie resolution strategy — fold and close: instead of resolving PR
#7's merge conflict, we absorbed its five stranded skip-list entries
(nightly, tabularis, platform-skills, aidevops, trending-claude-skills)
into the harvest-14 branch, merged #8, and closed #7 with prejudice.
One PR to rule them all.

Key discovery about the trending-claude-skills reappearance: it wasn't
a harvester bug — the skip-list entry lived only on the unmerged PR #7
branch, invisible to the harvester. Lesson: **an unmerged harvest PR is
a blind spot in the skip-list. Merge the PRs or the pruning doesn't
count.**

Execution details worth remembering: both sed skip-list inserts landed
clean (47 total entries now), row surgery verified with
`git diff main -- MODELS.md TOOLS.md | grep '^+'` showing exactly the
two keepers, commit `d551937`, push clean, merge, `main` fast-forwarded
to `f0eff1b` with all keepers, skip-list growth (+16), and the run's
JSONL receipt aboard.

Fresh-clone gotchas encountered on the droplet (all resolved, all
documented for next time): pip ships separately on Ubuntu 24.04 (fixed
via python3-venv + venv, which was the right call anyway for
isolation), git identity unknown on a fresh clone (set repo-scoped,
not global, honoring the separation rule), and first-push
authentication (renewed; now cached).

## The Breakdown

- The zombie PR was the session's real lesson: completed surgery ≠
  closed wound. The pruning was perfect — and completely inert because
  nobody merged it. Autonomy's ledger only updates when the human hits
  the button.
- `.venv/` showing as untracked in `git status` — never commit it.
- Had a step-ordering stumble early on (assistant handed step 3 before
  step 1) — new permanent expectation: steps in strict dependency
  order, prerequisites first, nothing withheld for later.

## Decisions & Why

- **Fold-and-close over conflict resolution** — resolving PR #7's
  conflict would've meant juggling three versions of the skip-list.
  Absorbing its entries into #8 and closing the zombie was cleaner,
  faster, and left zero stranded work.
- **Repo-scoped git config (not --global)** — each project on the
  droplet keeps its own identity and credentials. Contamination-proof.
- **Virtualenv per project** — same isolation logic. The system Python
  belongs to the OS; each project's dependencies belong to the project.
- **Zulu time for all future documentation** — effective immediately,
  noted at the top of this session note. The mycelium speaks UTC now.

## Nuggets & Vibes

- "An unmerged PR is a prayer that was never mailed."
- The droplet is now a full-fledged dev environment — the mycelium has
  a second home.
- Two zombies pruned in two weeks. The gardener's shears stay sharp.
- "Computer logic is reversed in LLMs" — steps go forward, Monsieur. Always forward.

## Next Steps

- Keep an eye on next Thursday's harvest (cron 05:00Z) — with #7 and
  #8 both merged and ~16 new skip-list entries, the garden should come
  back cleaner
- Open decision from last session still parked: tracked-logs question
  (audit trail vs gitignore)
- Classifier tuning still flagged — TOOL bucket remains a junk drawer
- Promote this to a polished phase note when ready; adjacent to
  [[Session-062-2026-10-17-Harvester-Hardening-And-Harvest-7-Pruning]]
