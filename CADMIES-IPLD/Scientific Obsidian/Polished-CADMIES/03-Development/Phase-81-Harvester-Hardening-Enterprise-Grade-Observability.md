---
phase: 81
date: 2026-10-17
status: Complete
related: [[Phase-69-Repo-Maintenance-Automation]], [[Phase-72-LLMDataHub-Fork-Reorganization]], [[Session-062-2026-10-17-Harvester-Hardening-And-Harvest-7-Pruning]]
---

# Phase 81: Harvester Hardening — Enterprise-Grade Observability

## What Changed

The LLMDataHub harvester pipeline was hardened from a fragile, opaque weekly automation into an observable, resilient system. The weekly harvest GitHub Action had begun failing intermittently, and when it failed, the logs needed to diagnose it were unavailable. This phase fixed the root causes and added structured observability, retry resilience, and a documented manual recovery procedure.

Specifically:

- Corrected a path-drift defect that caused the harvest workflow to fail on every run.
- Introduced structured JSONL logging with run-ID correlation.
- Introduced exponential-backoff retry for transient network and API failures.
- Guaranteed PR-body generation ordering so downstream steps always find the artifact.
- Made artifact uploads tolerant of missing files and uniquely named per run.
- Removed a vestigial module that executed on every invocation despite being marked "archived."
- Documented the manual harvest-PR pruning procedure for operator independence.

## Why

The harvester runs autonomously on a weekly cron with no human in the loop until a pull request appears. That autonomy is only as valuable as its diagnosability: if a run fails silently or leaves no usable trace, the operator must reconstruct the failure from scratch, defeating the purpose of automation.

Three defects motivated this phase:

1. **Path drift.** In harvester v1.1.1, all log, report, and script output paths were consolidated into `repo-maintenance-automation/logs/`. The GitHub workflow files were not updated to match and continued referencing `logs/` at the repository root. Because the harvester wrote to the new location while the workflow read from the old one, the `create-pull-request` step failed with `Error: File 'logs/pr_body.md' does not exist`, and the artifact upload silently found no files.

2. **Fragile PR-body ordering.** In PR mode, the harvester generated `pr_body.md` only after applying insertions. Any failure earlier in the pipeline (scraping, classification, formatting) meant the file never existed when the workflow needed it, cascading a recoverable error into a hard failure.

3. **No structured observability.** Diagnostic output consisted of unstructured `print()` statements scattered across modules. There was no way to correlate console output with a specific CI run, no machine-parseable log artifact, and several bare `except:` clauses swallowed errors silently.

The governing principle: an autonomous pipeline must leave a complete, correlatable record of what it did, and must survive transient failures without human intervention. Silent failure is the enemy of autonomy.

## Changes Made

### New Modules

| File | Purpose |
|------|---------|
| `repo-maintenance-automation/logger.py` | Structured logging with run-ID correlation. Emits human-readable console output plus one JSON-lines file per run (`run_<run_id>.jsonl`). Run ID derives from `GITHUB_RUN_ID` in CI, or a generated `local-<hex>` ID otherwise, and is propagated to child processes via the `HARVEST_RUN_ID` environment variable. |
| `repo-maintenance-automation/retry.py` | `with_retry` decorator providing exponential backoff with jitter. Retries HTTP 429/500/502/503/504 and connection/timeout errors. Raises immediately on permanent errors (e.g. 422, 404) to avoid wasted attempts. |

### Modified Modules

| File | Change |
|------|--------|
| `github_scraper.py` (v1.0.4 → v1.1.0) | Wired in the structured logger and retry decorator. Added a 30-second request timeout. Replaced the bare `except:` in `is_recently_updated` with a typed `except (ValueError, TypeError)` that logs at debug level. |
| `harvest.py` (v1.1.1 → v1.2.0) | PR body is now generated and written **before** `apply_insertions`, guaranteeing its existence for downstream steps. Removed the `old_itch` import and its `standard_maintenance()` calls. Converted diagnostic output to the structured logger. |
| `.github/workflows/harvest.yml` | Corrected `body-path` and artifact `path` to `repo-maintenance-automation/logs/`. Artifact name now includes `github.run_id`. Added `if-no-files-found: warn`. Bumped `actions/checkout` to v4 and `actions/setup-python` to v5. |
| `.github/workflows/vault-check.yml` | Corrected artifact `path` to `repo-maintenance-automation/logs/`. Artifact name includes `github.run_id`. Added `if-no-files-found: warn`. Bumped action versions. |

### Removed

| File | Reason |
|------|--------|
| `repo-maintenance-automation/old_itch.py` | Vestigial scratch module labeled "archived — ignore this file," yet imported and executed on every harvester invocation via `standard_maintenance()`. It wrote to a relative `logs/` path, contributing to path confusion. |

### Documentation

| File | Purpose |
|------|---------|
| `repo-maintenance-automation/README.md` | New. Documents all automation components, log locations, harvest flow, and the complete manual procedure for pruning a harvest PR (fetch, inspect, skip-list, row deletion, verify, commit, merge). Includes a parking-lot section for future work. |

## Testing

The hardened pipeline was validated by dispatching the Weekly Harvest workflow via `workflow_dispatch` (rather than waiting for the weekly cron).

An initial test run failed with the identical original error. Inspection of the run log revealed `old_itch.py` broom-emoji output and the pre-hardening PR-body ordering, proving the fixes had not yet been pushed to the branch the runner executed. After pushing all changes to `main`, the workflow was re-dispatched.

The successful run was verified against the following criteria:

- Structured log lines prefixed with the run ID (e.g. `[INFO][9059266985-1]`) appeared in the Actions console.
- The run completed green.
- A pull request (`auto/harvest-13`) was created with the correct body and labels.
- The artifact `harvest-report-<run_id>` uploaded successfully, containing eight files including the run's JSONL log.

## Results

- **Pipeline restored.** The weekly harvest completes successfully end to end: scrape, filter, classify, format, insert, PR creation, and artifact upload.
- **Observability achieved.** Each run produces a machine-parseable `run_<run_id>.jsonl` artifact correlated to its GitHub Actions run ID. Failures can be diagnosed by downloading a single artifact and reading one file.
- **Resilience added.** Transient API failures are retried with backoff; rate-limit waits are logged as warnings rather than crashing the run.
- **PR-body guarantee verified.** The body file is confirmed present in the artifact and rendered correctly in the created pull request.
- **Operator independence.** The manual pruning procedure is documented in the automation README, enabling post-harvest curation without external assistance.

The successful run produced: 67 candidates scraped, 62 new after filtering, 59 classified as noise, and 11 reportable entries (1 model, 2 papers, 8 tools).

## Analysis

The root-cause investigation demonstrated a recurring failure mode in evolving automation: **when a component relocates its outputs, every consumer of those outputs must relocate with it.** The harvester's v1.1.1 path consolidation was correct in isolation but incomplete as a change, because the workflow files that consume those paths were not part of the same edit. The resulting failure was misleading — it presented as a missing file rather than a path mismatch — which delayed diagnosis.

The PR-body ordering defect illustrates a second principle: **artifacts required by downstream consumers should be produced as early as possible in the pipeline, not as late.** Generating the PR body after the risky insertion step coupled a cosmetic output to the success of the most failure-prone operation.

The observability gap was the most consequential finding. Without run-correlated structured logs, the initial failure could only be diagnosed by reading unstructured console output and inferring the cause. The addition of `logger.py` converts every future failure from an investigation into a lookup. This is the defining characteristic of enterprise-grade autonomy: the system explains itself.

A residual observation, deferred rather than resolved: the harvest logs are tracked in git and therefore travel into the pull request commit. This provides an immutable audit trail but introduces branch-switch collisions when local log files are dirty. Whether logs should remain tracked (audit trail) or be gitignored (artifact-only) is an open decision, recorded in the automation README parking lot.

## Conclusion

Phase 81 converted the LLMDataHub harvester from a brittle script into a diagnosable, self-healing system. The three defects — path drift, fragile ordering, and absent observability — are resolved and verified by a successful end-to-end run. The pipeline now satisfies the standard appropriate to autonomous operation: it survives transient failure without intervention, and when it does fail, it leaves a complete, correlatable record sufficient to reconstruct exactly what happened.

The work also produced lasting operational assets: a documented manual pruning procedure and a parking lot capturing deferred improvements (typed exceptions, post-insertion verification, test suite, concurrency locking, and the tracked-logs decision).

Subsequent phases may build on this foundation. Phase 82 (Deep Harvest) proposes extending discovery beyond GitHub to additional high-signal sources, and would inherit the logging and retry infrastructure established here.
