---
type: sop
system: Vault Health Automation
version: 1.0.0
date: 2026-11-24
status: Active
related: "[[SOP Landing]], [[04-References]], [[05-Troubleshooting]]"
---

# 03-Procedures

Back to: [[SOP Landing]]

## 03-01 Running a Manual Check

On the droplet (or any checkout with Python 3.11+ and pyyaml):

```
cd CADMIES/repo-maintenance-automation
python validate_vault.py            # report mode, read-only
python validate_vault.py --fix      # interactive fix proposals
python validate_vault.py --fix --yes # auto-apply (use sparingly)
```

Exit code 0 = healthy; 1 = issues found. Reports land in `logs/`: text report, HTML dashboard, and one appended trend line.

## 03-02 Reading Results

- Console/report: per-file ✅/⚠️ per doc-type, then cross-refs, extensions, duplicates, orphans, roadmap sync, and a summary.
- HTML dashboard (`logs/vault_health_dashboard.html`): one-glance section table with a healthy/issues badge.
- Trend CSV (`logs/vault_health_trends.csv`): the vault's vitals history — issue spikes and drift become visible over weeks.

## 03-03 Fixing Issues

1. Run report mode first; identify the issue class.
2. For dead links: fix the link or de-wikilink to plain text. Check the root cause — if a note links to a nonexistent note, either create the target or demote the reference (Note-Taking Protocol rule: link only what exists).
3. For frontmatter/sections/banner: repair the note by hand or use `--fix`.
4. For duplicates: decide which copy is canonical; delete the other deliberately, not casually.
5. For roadmap drift: reconcile phase-note status with the roadmap entry — the roadmap is the plan of record, the phase note is the truth of what happened; when they conflict, the phase note usually wins and the roadmap gets updated.
6. Re-run the validator; confirm 0 issues; commit.

## 03-04 Changing the Rules

Rules live in `config.yaml` — never in code. To add a required field, a new doc-type, or adjust valid statuses: edit `config.yaml`, run the validator, observe effects, commit. See [[04-References]] for the config schema.

## 03-05 Scheduling

GitHub Actions workflow `.github/workflows/vault-check.yml` runs the check at 05:00Z and 17:00Z daily. Manual trigger: Actions tab → Vault Health Check → Run workflow. The workflow pins actions to commit hashes; keep that discipline on any edit.
