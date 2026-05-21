# CADMIES Note-Taking Protocol
**Version:** 1.0.0
**Date:** 2026-05-14
**Status:** Living document — updated as conventions evolve
---
## Purpose
This protocol governs how notes are created, formatted, linked, and promoted within the Scientific Obsidian vault. It ensures consistency across Raw CADMIES and Polished CADMIES, making the vault navigable for gardeners, collaborators, and PhDs alike.
---
## Vault Structure
The vault has two primary workspaces plus a meta layer:
- **Raw CADMIES/** — The primary workspace. The live lab notebook. This is where ideas land, sessions are drafted, and half-formed thoughts find their first expression. Gardeners work here by default. Mistakes are welcome. Typos are canon.
- **Polished CADMIES/** — The secondary workspace. Structured, reviewed, PhD-ready documentation. Notes are promoted here from Raw when they meet the promotion criteria below.
- **00-Meta/** — Governs both layers. Templates, conventions, this protocol.
---
## File Naming Conventions
- Use **Sentence case** for all note titles: `Harvester pipeline overview.md` not `harvester_pipeline_overview.md`
- Phase documents: `Phase-XX-Brief-Description.md` (e.g., `Phase-35-Difficulty-Levels.md`)
- Session summaries: `Session-XXX.md` (e.g., `Session-005.md`)
- No special characters except hyphens. No emojis in filenames.
- Spaces are fine — Obsidian handles them natively.
---
## Raw CADMIES Conventions
Every note in Raw CADMIES begins with a banner:

> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,  
> unfiltered thoughts, and coded messages for fellow gardeners.  
> For polished documentation, check Polished CADMIES or promote this note.

text

**Rules for Raw:**
- Write freely. Grammar optional. Structure optional. Vibes mandatory.
- Date your entries. Even a quick `2026-05-14` at the top helps trace idea lineage.
- Use `[[double brackets]]` to link to related concepts, phases, sessions, or people — even if the target note doesn't exist yet. Red links are future spores.
- Tag generously but loosely. `#idea`, `#question`, `#breakthrough`, `#bug`, `#wtf`
- No pressure to organize. The mycelium finds connections organically.
---
## Polished CADMIES Conventions
Every note in Polished CADMIES includes a metadata header:

---

phase: XX  
date: YYYY-MM-DD  
status: Active | Complete | Superseded  
related: [[note-one]], [[note-two]]

---

text

**Rules for Polished:**
- Structured, clear, PhD-readable.
- Every claim links to evidence — a session summary, a commit, a test result.
- No banners needed. The folder itself signals "this is the clean copy."
- Follow the folder structure: System, Pipeline, Development, Concepts, Collaboration.
- Version your notes if they undergo major revisions (append version to metadata, not filename).
---
## YAML Frontmatter Rule
Polished notes use YAML frontmatter (the `---` block at the top). **The only `---` in any note is the YAML block.** For section dividers in the body, use `***` (three asterisks). This prevents Obsidian's YAML parser from breaking when it encounters `---` mid-document.
---
## Promotion Criteria: Raw → Polished
A note is ready for promotion when:
1. It has a clear title that describes its content.
2. It is structured enough that a stranger (or a PhD) could understand it without context.
3. Key claims link to evidence (session notes, commits, test results).
4. The Raw banner is removed and replaced with a Polished metadata header.
5. It is placed in the appropriate Polished CADMIES subfolder.
**Promotion is optional.** Not every raw note needs to become polished. Some spores stay in the scrawl forever, and that's fine.
---
## Linking Philosophy
The vault is a graph, not a hierarchy. Link aggressively:
- `[[Phase-35-Difficulty-Levels]]` — links to phase documentation
- `[[Session-005]]` — links to a session summary
- `[[Harvester Pipeline]]` — links to the pipeline tool note
- `[[Dr-Rebentisch]]` — links to a person/collaborator note
- `[[bayes_theorem]]` — links to a concept (mirrors the mycelium)
Red links (notes that don't exist yet) are **planted spores**. They mark where future notes should grow. Don't delete them — let them fruit.
---
## Tags
Use flat, lowercase tags. No hierarchy needed to start:
| Tag | Usage |
|-----|-------|
| `#idea` | A new concept, approach, or possibility |
| `#question` | Something that needs answering |
| `#breakthrough` | A significant insight or discovery |
| `#bug` | Something broken that needs fixing |
| `#decision` | An architectural or design choice |
| `#phase-XX` | Relates to a specific roadmap phase |
| `#harvester`, `#map`, `#gateway` | Tool-specific notes |
| `#collaboration` | Cross-mycelium or external partnership |
Tags will evolve. That's fine. Add new ones as needed.
---
## Session Summary Template
Create one note per development session in `Raw CADMIES/Session-Notes/`. Use this template:

# Session XXX — YYYY-MM-DD

## What We Did

## What Worked

## What Broke

## Decisions Made

## Nuggets Collected

## Next Session

text

Promote completed session summaries to `Polished CADMIES/03-Development/` when they are coherent enough for external readers.
---
## Collaboration Notes
All external collaboration documentation lives in `Polished CADMIES/05-Collaboration/`. Each collaborator gets a note:
- Who they are
- What they built / are building
- How their work intersects with CADMIES
- Links to their repositories, papers, or correspondence
- Status of the collaboration (active, dormant, completed)
---
## Credit & Attribution
- All influences are documented. If a methodology, tool, or idea came from somewhere else, link to it.
- Dr. Rupert Rebentisch (tools4zettelkasten) and the Luhmann/Ahrens/Forte zettelkasten tradition are the primary methodological influences on this vault.
- **The Naming Protocol** uses hyphens to denote partnership: CADMIES-Mistral, CADMIES-IPLD, CADMIES-Codestral. The hyphen is an acknowledgment of collaboration, not a claim of ownership. Attribution is architecture.
- CADMIES is CC BY-SA 4.0. All vault content inherits this license.
- **The Naming Protocol** uses hyphens to denote partnership: CADMIES-Mistral, CADMIES-IPLD, CADMIES-Codestral. The hyphen is an acknowledgment of collaboration, not a claim of ownership. Attribution is architecture.
---
## Evolution
This protocol is version 1.0.0. It will change as we learn what works. The Casual Friday approach applies: start lenient, increase rigor organically. The mycelium teaches us how to document it.
---
> *"The fortress holds the library. The library holds the records. The mycelium holds the knowledge. Scientific Obsidian is the glass that remembers."*