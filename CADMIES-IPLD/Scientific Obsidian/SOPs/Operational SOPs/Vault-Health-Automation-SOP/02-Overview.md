---
type: sop
system: Vault Health Automation
version: 1.0.0
date: 2026-11-24
status: Active
related: "[[SOP Landing]], [[03-Procedures]]"
---

# 02-Overview

Back to: [[SOP Landing]]

## Scope

The vault health system watches the **Scientific Obsidian** vault in the CADMIES repo: frontmatter uniformity per doc-type, required sections, raw-note banners, wikilink integrity, filename extensions, duplicate content, roadmap drift, and (informationally) orphan notes. It deliberately does **not** validate the SOPs folder — SOPs follow the SOP-Creation-SOP conventions and are outside this system's perimeter by design (config `skip_folders`). It is not, and never was, either harvester: not the CADMIES concept harvester, not the LLMDataHub repo harvester. Vault health = documentation structure only.

## Terminology

- **Validator** — `repo-maintenance-automation/validate_vault.py`, the single engine. Read-only by default; `--fix` proposes interactive repairs with timestamped backups; `--fix --yes` applies automatically.
- **Doc-type** — a category in `config.yaml` (polished_phase, raw_session, meta, roadmap...) binding a folder + filename pattern to required frontmatter/sections/banners.
- **Issue** — a violation that fails the run (dead link, missing field, duplicate).
- **Orphan** — a note with zero inbound wikilinks. Informational only; never fails a run.
- **Trend snapshot** — one CSV line per run (timestamp Zulu, files checked, issues found) appended to `logs/vault_health_trends.csv`.

## What Gets Checked (and why)

| Check | Purpose | Failure impact |
|---|---|---|
| Frontmatter per doc-type | Uniform metadata; machine-readability | Issue |
| Required sections (What Changed / Why) | NASA-level narrative discipline on polished phases | Issue |
| RAW NOTE banner on session notes | Separates raw from polished clearly | Issue |
| Wikilink integrity | Every `[[link]]` must resolve to an existing note | Issue |
| .md extension presence | Filenames stay uniform | Issue |
| Duplicate detection (MD5) | Same content must not exist twice | Issue |
| Roadmap drift | Phase-note statuses must match roadmap symbols | Issue |
| Orphan detection | Connectivity diagnosis — which notes are islands | Info only |

## Doctrine

- **Link only to notes that exist** (per the refined Note-Taking Protocol, 2026-11-24): red links are fine in a live Obsidian session, but a note committed to the vault references existing targets or plain text. The validator enforces this.
- **Scheduled, not reactive.** The check runs twice daily (05:00Z / 17:00Z), not on push — push-triggered runs caught notes mid-write and cried wolf. Manual runs are always available via `workflow_dispatch`.
- **Diagnosis ≠ failure.** Orphans inform; they don't alarm.
- **Backups before any fix.** `--fix` writes timestamped backups to `logs/backups/` before touching a file. Content is never rewritten, only structure.
