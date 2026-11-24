---
type: sop
system: Vault Health Automation
version: 1.0.0
date: 2026-11-24
status: Active
related: "[[SOP-Creation-SOP]], [[Note-Taking Protocol]], [[growth_roadmap]]"
---

# Vault Health Automation SOP

> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Vault Health Automation — SOP Landing

**One-sentence description:** An automated health system for the Scientific Obsidian vault that checks every note for structural uniformity, dead wikilinks, duplicates, and roadmap drift — and reports, trends, and heals on a twice-daily schedule.

**What the system is:** A single Python validator (`validate_vault.py`, currently v1.4.0) driven by a declarative config (`config.yaml`), run automatically by GitHub Actions twice a day (05:00Z and 17:00Z). It is the guardian of NASA-level documentation standards for the vault — the same role the roadmap plays for project direction and the SOP-Creation-SOP plays for SOP authorship.

**How to use this vault:** Read the [[02-Overview]] first for what the system checks and why. [[03-Procedures]] covers operating it — running manually, fixing issues, updating rules. [[05-Troubleshooting]] covers what to do when the check fails or the automation misbehaves. The Landing note is the hub: every section links back here.

**Vault map:**
- 02-Overview — scope, terminology, what gets checked
- 03-Procedures — running, fixing, scheduling, changing rules
- 04-References — command reference, config schema
- 05-Troubleshooting — known failure modes and remedies
- 06-Appendices — version history, health trend data policy

**Status:** Active since 2026-07-16 (v1.0.0 as Phase 69). Enterprise hardening and twice-daily schedule: 2026-11-24 (validator v1.4.0). This vault: v1.0.0.

*All timestamps Zulu.*
