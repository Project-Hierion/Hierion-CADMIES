---
type: sop
system: Vault Health Automation
version: 1.0.0
date: 2026-11-24
status: Active
related: "[[SOP Landing]], [[03-Procedures]]"
---

# 04-References

Back to: [[SOP Landing]]

## 04-01 Command Reference

| Command | Effect |
|---|---|
| `python validate_vault.py` | Report-only health check; exit 1 on issues |
| `python validate_vault.py --fix` | Interactive fix mode; backups to `logs/backups/` |
| `python validate_vault.py --fix --yes` | Auto-apply all fixes |
| Workflow dispatch (GitHub) | Run the same check in CI on demand |

## 04-02 Configuration Schema (`config.yaml`)

- `vault_root` — path to Scientific Obsidian, relative to the script.
- `skip_folders` — directories excluded from all checks (currently: SOPs/ — deliberate).
- `doc_types.<name>` — folder, name_pattern (or filename), required_frontmatter, required_sections, valid_statuses, required_banner.
- `cross_refs.scan_folders` — folders whose wikilinks get resolved.
- `roadmap_sync.source` — the roadmap file for drift checks.
- `privacy.local_only_patterns` — files flagged local-only.
- `reporting` — output dir, report filename, save toggle.

## 04-03 Dependencies

- Python ≥ 3.11 (production CI uses 3.12), `pyyaml`.
- GitHub Actions runner for scheduled runs (ubuntu-latest).
- Output artifacts: text report, HTML dashboard, trends CSV — all under `logs/`.
