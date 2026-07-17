# Repo Maintenance Automation

Tools that keep the Scientific Obsidian vault clean, consistent, and cross-referenced.

## validate_vault.py

The vault health checker. Scans all markdown files in the Scientific Obsidian vault and reports on:

- Frontmatter consistency — missing YAML headers, missing required fields, invalid statuses
- Dead wikilinks — [[links]] that point to files that don't exist
- Missing sections — polished phase notes missing "What Changed" or "Why"
- Raw note banners — session notes without the required raw note warning
- Duplicate files — identical content in multiple locations
- Roadmap drift — phase note status doesn't match the roadmap
- Missing extensions — markdown files without .md suffix

### Usage
Report only (safe, no changes)
```
python repo-maintenance-automation/validate_vault.py
```

Interactive fix mode (shows before/after, asks for confirmation)
```
python repo-maintenance-automation/validate_vault.py --fix
```

Auto-fix all safe issues (no prompts)
```
python repo-maintenance-automation/validate_vault.py --fix --yes
```

### What --fix handles

- Dead wikilinks — matches to correct filenames via fuzzy search
- Status fields — normalizes emoji-prefixed or non-standard statuses
- Raw note banners — adds the standard banner to session notes

### Safety

- Every fix creates a timestamped backup in logs/backups/
- --fix mode shows before/after previews and asks for confirmation
- Content is never modified — only structural metadata

## config.yaml

Defines the rules for each document type. Update this when standards evolve.

## GitHub Action

A workflow at `.github/workflows/vault-check.yml` runs the validator automatically on every push to main. No manual commands needed.

## Logs

- logs/vault_health_report.txt — latest validation report
- logs/backups/ — automatic backups created before any fix is applied
