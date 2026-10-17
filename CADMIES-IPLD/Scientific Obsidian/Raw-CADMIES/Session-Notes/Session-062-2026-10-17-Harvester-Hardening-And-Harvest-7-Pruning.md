> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 062 — 2026-10-17 — Harvester Hardening and Harvest 7 Pruning

## Soundtrack
Whatever was in the air. Low-key debugging groove.

## What We Did

Started the day chasing a failed harvest run in the LLMDataHub repo. The GitHub Action died with `Error: File 'logs/pr_body.md' does not exist.` Looked scary, turned out to be two bugs stacked on top of each other:

1. The harvester (since v1.1.1) writes all logs to `repo-maintenance-automation/logs/`, but the workflow still pointed at `logs/` (repo root) for both the PR body and the artifact upload. Paths drifted apart when the log consolidation happened and nobody updated the workflows.
2. In PR mode, `harvest.py` only wrote `pr_body.md` AFTER `apply_insertions` — so any crash earlier in the pipeline meant the file never existed for create-pull-request.

Fun detour: we dispatched a test run that failed with the exact same error, but the logs showed `old_itch.py` broom emojis — proof none of our fixes had actually landed on the branch the runner used. Classic "fixed the code, forgot to push" moment.

Before fixing, we did an enterprise-grade hardening pass (Option B, chosen over minimal patch and full Option C):

- **Deleted `old_itch.py`** — the "archived, ignore this" file that was actually imported and executed on every banner call. Begone.
- **New `logger.py`** — structured JSONL logging with run-ID correlation. Every line tagged `[INFO][<run_id>]`, run_id inherited from `GITHUB_RUN_ID` in CI. Each run drops a `run_<id>.jsonl` in the logs dir, and it lands in the artifact.
- **New `retry.py`** — exponential backoff with jitter for 429/5xx/transient network errors. Permanent errors raise immediately.
- **`github_scraper.py` v1.1.0`** — wired in the retry decorator, structured logger, killed the bare `except:` in `is_recently_updated`, added a 30s timeout on requests.
- **`harvest.py` v1.2.0** — PR body now written BEFORE `apply_insertions` so it always exists. Removed the old_itch import and the standard_maintenance spam.
- **Both workflows updated** — `body-path` and artifact `path` corrected to `repo-maintenance-automation/logs/`, artifact name now includes `github.run_id`, `if-no-files-found: warn`, bumped checkout@v4 / setup-python@v5 to kill Node deprecation noise.

Re-dispatched. GREEN. Structured logging live in the log, PR body generated before apply, PR #7 created on `auto/harvest-13`, artifact uploaded with the JSONL run log inside. 8 files, 23KB. Beautiful.

Then we gardened PR #7. Found 11 candidates (1 model, 2 papers, 8 tools). Kept three:

- `abhiramm7/openfloodhub` — flood forecasting model (MODELS)
- `locuslab/open-unlearning` — NeurIPS D&B '25, LLM unlearning (PAPERS)
- `benjaminzwhite/reasoning-models` — reasoning experiments (PAPERS)

Everything else was junk. The TOOL bucket is a junk drawer — anything with "AI" + "agent" + "platform" scores 1.2+ regardless of whether it belongs in an LLM archive. Classifier tuning session needed.

Did the pruning surgery manually, which became the SOP:

1. `git fetch origin auto/harvest-13` then checkout (had to discard a dirty `classification_report.txt` first — logs are git-tracked, which causes branch-switch collisions)
2. `sed` inserts into the skip-list (took two tries to find the right path — it lives at `repo-maintenance-automation/logs/rejected_candidates.txt`, buried under logs/)
3. `sed` row deletion in TOOLS.md matched on repo URL slugs
4. Commit, force-with-lease push, merged PR #7
5. Caught a gap after merge: only 5 of 8 rejects made the skip-list — `linny006/awesome-agent-skills`, `Osmantic/ODS`, `clay-good/OpenLore` slipped through. Patched them onto main directly (commit d24c350)

Finished by writing the automation README (`repo-maintenance-automation/README.md`) with the full pruning SOP baked in, plus a parking lot section: Deep Harvest second-pipeline idea, deferred Option C items, and the tracked-logs question.

## The Breakdown

- First re-test failed identically to the original bug — because the fixes weren't pushed to main. Lesson: verify what the runner is actually pulling before declaring a fix dead.
- Wrong path guesses on `rejected_candidates.txt` (twice). The file's home under `logs/` is counterintuitive. The skip-list is persistent curation data, not a log — arguably it should move someday.
- Sed multiline inserts are finicky with `\` line continuations but they work.
- Branch checkout collisions from git-tracked logs. Will keep biting until we decide: audit trail or gitignore?

## Decisions & Why

- **Option B hardening** (logging + retry, skip the full test suite for now) — ROI reasoning: for a weekly autonomous harvest with a sole operator, knowing exactly what happened when something breaks beats full test coverage. Option C remains parked.
- **Prune-then-merge over merge-as-is** — merging 5 off-theme tools into TOOLS.md pollutes the archive and trains the gardener to ignore harvest PRs.
- **Skip-list everything rejected** — non-negotiable. Without it, next week's harvest re-finds the same junk. Every deleted row must get a skip-list entry.
- **Harvester stays GitHub-only for now** — noted in the README parking lot: a future second "Deep Harvest" pipeline for targeted non-GitHub sources (ModelScope, arXiv, data portals) with strict anti-noise filters. No social media garbage.
- **Logs tracked in git — undecided** — flagged, not resolved.

## Nuggets & Vibes

- "The mycelium is stronger than it was yesterday" — and today it learned to keep receipts.
- Watching the green run's log come back tagged with run-IDs felt like the moment the plant learned to write its own diary.
- We pruned a harvest PR on the same day we pruned `old_itch.py`. Gardener's day of snips.
- Lesson of the day: an "ignore this file" note that runs on every invocation is the most dishonest file in the repo.
