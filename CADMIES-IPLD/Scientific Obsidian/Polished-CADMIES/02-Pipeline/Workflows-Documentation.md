---
pipeline: CADMIES Documentation Workflow
date: 2026-05-26
status: Living document
related: [[Pipeline-Workflows]], [[Phase-37-Scientific-Obsidian]], [[Note-Taking-Protocol]]
---
# CADMIES Documentation Workflow
## What This Covers
Every session produces documentation: raw notes, polished phase notes, roadmap updates, and changelog entries. This workflow ensures nothing is forgotten.
## Workflow: Session Documentation

┌──────────────────────────────────────────────────────────────────┐  
│ DOCUMENTATION WORKFLOW │  
│ │  
│ Session ends │  
│ │ │  
│ ▼ │  
│ ┌─────────────────┐ │  
│ │ Raw session note │ Scientific Obsidian/Raw-CADMIES/ │  
│ │ │ Session-Notes/Session-XXX.md │  
│ └────────┬────────┘ │  
│ │ │  
│ ▼ │  
│ ┌─────────────────┐ │  
│ │ Polished phase │ Scientific Obsidian/Polished-CADMIES/ │  
│ │ notes (if any) │ 03-Development/Phase-XX-Name.md │  
│ └────────┬────────┘ │  
│ │ │  
│ ▼ │  
│ ┌─────────────────┐ │  
│ │ Roadmap update │ growth_roadmap.md │  
│ │ (milestone log) │ Update metrics, add milestone │  
│ └────────┬────────┘ │  
│ │ │  
│ ▼ │  
│ ┌─────────────────┐ │  
│ │ CHANGELOG update │ CHANGELOG.md │  
│ │ (script changes) │ Per-script version histories │  
│ └────────┬────────┘ │  
│ │ │  
│ ▼ │  
│ ┌─────────────────┐ │  
│ │ Commit & push │ git add -A && git commit && git push │  
│ └─────────────────┘ │  
└──────────────────────────────────────────────────────────────────┘

text

## Note Types
### Raw Session Notes
- Location: `Scientific Obsidian/Raw-CADMIES/Session-Notes/Session-XXX.md`
- Format: Casual Friday tone. Soundtrack, vibes, half-formed ideas, coded messages.
- Template: Banner warning, session number, date, soundtrack, sections for what happened, final state, bugs, nuggets.
### Polished Phase Notes
- Location: `Scientific Obsidian/Polished-CADMIES/03-Development/Phase-XX-Name.md`
- Format: Scientific rigor. Frontmatter (phase/date/status/related), then What Changed, Why, Changes Made, Testing, Results, Analysis, Conclusion, Next Steps.
- Created when: A phase is completed or a significant milestone is reached.
### Pipeline Documents
- Location: `Scientific Obsidian/Polished-CADMIES/02-Pipeline/`
- Format: Workflow diagrams, command references, quick reference cards.
- Created when: New workflows are established or existing ones change significantly.
## Quick Reference
| Document Type | Location | When to Create |
|--------------|----------|----------------|
| Raw session note | Raw-CADMIES/Session-Notes/ | Every session |
| Polished phase note | Polished-CADMIES/03-Development/ | Phase completion |
| Roadmap update | growth_roadmap.md | Every session |
| CHANGELOG update | CHANGELOG.md | Script changes |
| Pipeline document | Polished-CADMIES/02-Pipeline/ | New workflows |