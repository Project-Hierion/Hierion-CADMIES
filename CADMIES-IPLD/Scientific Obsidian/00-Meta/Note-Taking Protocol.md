---
type: protocol
version: 1.3.0
date: 2026-10-17
status: Living document — updated as conventions evolve
related: [[NASA-level standards reference]], [[CADMIES-Canon]], [[Architecture Overview]]
---

# CADMIES Note-Taking Protocol

## Purpose

This protocol governs how notes are created, formatted, linked, and promoted within the Scientific Obsidian vault. It ensures consistency across Raw CADMIES and Polished CADMIES, making the vault navigable for gardeners, collaborators, and PhDs alike. Standards are informed by NASA-level scientific documentation practices where applicable.

**Core Philosophy:** The vault is a living memory. If it isn't written down, it didn't happen. If it's written down vaguely, it's useless later.

---

## Vault Structure

The vault has two primary workspaces plus a meta layer:

- **Raw-CADMIES/** — The primary workspace. The live lab notebook. This is where ideas land, sessions are drafted, and half-formed thoughts find their first expression. Gardeners work here by default. Mistakes are welcome. Typos are canon.
- **Polished-CADMIES/** — The secondary workspace. Structured, reviewed, PhD-ready documentation. Notes are promoted here from Raw when they meet the promotion criteria below.
- **00-Meta/** — Governs both layers. Templates, conventions, this protocol.

---

## File Naming Conventions

**All filenames use hyphens only. No spaces, no em-dashes, no special characters except hyphens.** This ensures machine-readability, command-line safety, and scientific rigor.

### Polished Phase Notes

Format: `Phase-XX-Description-With-Hyphens.md`

Examples:
- `Phase-35-Difficulty-Levels.md`
- `Phase-69-Repo-Maintenance-Automation.md`
- `Phase-45E-Dr-Amanda-Mistral-Fine-Tuning-the-Librarian.md`

Rules:
- Starts with `Phase-` followed by the phase number (digits, optional letter for sub-phases)
- Description uses hyphens between all words
- No dots, no ampersands, no em-dashes
- Use `and` not `&`
- Use `Dr` not `Dr.`

### Raw Session Notes

Format: `Session-XXX-YYYY-MM-DD-Description-With-Hyphens.md`

Examples:
- `Session-037-2026-07-16-The-Mycelium-Cleans-Itself.md`
- `Session-041-2026-07-28-LLMDataHub-Fork-Reorganization.md`
- `Session-061-2026-10-17-Building-The-Gardeners-Wall-Blog.md`

Rules:
- Starts with `Session-` followed by the session number
- Date in YYYY-MM-DD format, separated by hyphens
- Description uses hyphens between all words
- No dots, no ampersands, no em-dashes
- Use `and` not `&`
- Use `Dr` not `Dr.`

### General Rules

- All markdown files must carry the `.md` extension
- No colons, no emojis in filenames
- No special characters except hyphens
- Sentence case for descriptions (not lowercase, not UPPERCASE)

---

## Raw CADMIES Conventions

Every note in Raw CADMIES begins with a banner:

> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

**The Field Notes Style (Casual Friday)**

Raw notes are **narrative-driven records**, not rigid forms. The goal is to capture the *story* of the day so that six months from now, you remember exactly what happened, why it broke, and how you fixed it.

**Golden Rule:** **Cover Everything.** If we touched it, broke it, fixed it, or argued about it, it goes in the note. If you forget a detail today, you'll regret it next month.

**Structure (Loose, Narrative-First):**

1.  **What We Did (The Story):** Write chronologically. Don't just say "Fixed bug." Tell the story: *"Spent 45 mins debugging why the blog wasn't loading. Turns out the nginx config had a typo: `hirerion` instead of `hierion`. Fixed it, reloaded, live."* Include commands, error messages, and the "aha!" moments.
2.  **The Breakdown (What Failed):** What failed? What was confusing? What took way too long? Be specific. *"The deploy key didn't work because the SSH config had the wrong path. Wasted 20 mins before realizing the typo."*
3.  **Decisions & Why:** What did we decide? Why? *"Decided to use a 30-min cron pull instead of instant webhook. Reason: simple, safe, gives us a grace window to edit mistakes before they go live."*
4.  **Nuggets & Vibes:** The funny moments, the weird insights, the "aha!" moments. *"Realized the mycelium philosophy applies to git branches too: they grow, connect, and sometimes need pruning."*
5.  **Next Steps (Optional):** Only if there's a clear, actionable task left hanging. Otherwise, skip it.

**Tone Guidelines:**
-   **Honest:** Admit when you messed up. *"I forgot to set the password for the cadmies user and got stuck for an hour."*
-   **Specific:** Names, commands, timestamps, error messages.
-   **Human:** It's okay to say "this sucked" or "that was cool."
-   **No Fluff:** Cut the corporate speak. Get straight to the point.

**Example Snippet (Good):**
> "We spent the afternoon building the blog. Started with a private repo, added a deploy key, then realized the droplet didn't have Hugo installed. Installed it, built the site, but Nginx was serving the default page because the server_name was misspelled. Fixed the typo, reloaded, SSL issued. Finally live! The vibe was 'frustrated but triumphant.'"

**Example Snippet (Bad - Too Rigid):**
> "**What We Did:** Built blog. **What Broke:** Nginx. **Fix:** Typo. **Next Steps:** None."

**Rules for Raw:**

-   Write freely. Grammar optional. Structure optional. Vibes mandatory.
-   Date your entries. Even a quick `2026-05-14` at the top helps trace idea lineage.
-   Use `[[double brackets]]` to link to related concepts, phases, sessions, or people — even if the target note doesn't exist yet. Red links are future spores.
-   Tag generously but loosely. `#idea`, `#question`, `#breakthrough`, `#bug`, `#wtf`
-   No pressure to organize. The mycelium finds connections organically.
-   Session notes must include the standard session template sections (but follow the Field Notes style above).

---

## Polished CADMIES Conventions

Every note in Polished CADMIES includes a YAML frontmatter header:

```text
---
phase: XX
date: YYYY-MM-DD
status: Complete | In Progress | Designed | Planned | Abandoned | Active
related: [[note-one]], [[note-two]]
---
```

Rules for Polished:

Structured, clear, PhD-readable.

Every claim links to evidence — a session summary, a commit, a test result.

No banners needed. The folder itself signals "this is the clean copy."

Follow the folder structure: System, Pipeline, Development, Concepts, Collaboration.

No emojis in polished notes. These documents serve a scientific audience. Use words, not icons.

Required sections: ## What Changed and ## Why are mandatory. Additional sections (## Changes Made, ## Testing, ## Results, ## Analysis, ## Conclusion) are recommended where applicable.

Status values are standardized. Use plain text: Complete, In Progress, Designed, Planned, Abandoned, Active. If a phase is postponed, use Designed with clarification in the body.

A blank line must separate the YAML frontmatter closing --- from the content.

YAML Frontmatter Rule Polished notes use YAML frontmatter (the --- block at the top). The only --- in any note is the YAML block. For section dividers in the body, use *** (three asterisks). All frontmatter fields use lowercase keys. Required fields vary by document type — see repo-maintenance-automation/config.yaml for the authoritative list.

Promotion Criteria: Raw → Polished A note is ready for promotion when:

It has a clear title that describes its content.

It is structured enough that a stranger (or a PhD) could understand it without context.

Key claims link to evidence (session notes, commits, test results).

The Raw banner is removed and replaced with a Polished metadata header.

It is placed in the appropriate Polished CADMIES subfolder.

All wikilinks resolve to actual files. Dead links must be fixed or removed before promotion.

Promotion is optional. Not every raw note needs to become polished. Some spores stay in the scrawl forever.

Linking Philosophy The vault is a graph, not a hierarchy. Link aggressively:

[[Phase-35-Difficulty-Levels]] — links to phase documentation

[[Session-041-2026-07-28-LLMDataHub-Fork-Reorganization]] — links to a session summary

[[Harvester Pipeline (Superceded by Workflows)]] — links to a pipeline tool note

Wikilinks must use the full filename of the target note (without the .md extension). Shorthand links will be flagged as dead links by automation.

Red links (notes that don't exist yet) are planted spores. They mark where future notes should grow. Don't delete them — let them fruit.

Script files, concept IDs, and other non-note references should use backtick code formatting, not wikilinks.

Automation & Validation The vault is monitored by an automated validation system at repo-maintenance-automation/.

validate_vault.py — scans all notes for frontmatter consistency, dead wikilinks, missing sections, duplicate files, roadmap drift, and missing file extensions.

Run it: python repo-maintenance-automation/validate_vault.py

Auto-fix: python repo-maintenance-automation/validate_vault.py --fix (shows before/after, asks for confirmation)

Batch mode: python repo-maintenance-automation/validate_vault.py --fix --yes

GitHub Action: Runs on every push to main. Status badge in README.

Pre-commit hook: Blocks commits if vault has issues.

Backups: Every automated fix creates a timestamped backup.

Configuration: config.yaml defines required fields and sections. Update it when standards evolve.

Session Summary Template Create one note per development session in Raw-CADMIES/Session-Notes/.

Session XXX — YYYY-MM-DD — Brief Description
Soundtrack
(If the gardener says they're playing music or a video or movie)

What We Did
(Write a narrative story of the day's work. Cover everything. Be specific.)

The Breakdown
(What failed? What was confusing?)

Decisions & Why
(What did we decide and why?)

Nuggets & Vibes
(Funny moments, weird insights, quotes)

Next Steps (Optional)
(Only if there's a clear, actionable task left hanging)

Tags Tag Usage #idea A new concept, approach, or possibility #question Something that needs answering #breakthrough A significant insight or discovery #bug Something broken that needs fixing #decision An architectural or design choice #phase-XX Relates to a specific roadmap phase #harvester, #map, #gateway Tool-specific notes #collaboration Cross-mycelium or external partnership

Collaboration Notes All external collaboration documentation lives in Polished-CADMIES/05-Collaboration/. Each collaborator gets a note with: who they are, what they built, how their work intersects with CADMIES, links to their work, and collaboration status.

Classification & Privacy Polished notes are safe for public viewing. No personal information beyond first initial.

Raw notes may contain local paths, unfiltered thoughts, and personal references. Not for public distribution.

Sensitive files are excluded from GitHub via .gitignore.

Credit & Attribution All influences are documented. Link to sources.

NASA-level scientific documentation standards inform the structure and rigor of polished phase notes.

The Naming Protocol uses hyphens to denote partnership: CADMIES-Mistral, CADMIES-IPLD, CADMIES-Codestral. The hyphen is a handshake.

CADMIES is CC BY-SA 4.0. All vault content inherits this license.

Evolution This protocol is version 1.3.0. It will change as we learn what works. The Casual Friday approach applies: start lenient, increase rigor organically. The mycelium teaches us how to document it.

What Changed (v1.2.0 → v1.3.0) Changed:

Added Field Notes Style guidelines to Raw CADMIES: Shifted from rigid templates to narrative-driven recording. Emphasized "Cover Everything" and "Storytelling" over form-filling.
Updated Session Summary Template to reflect the narrative approach.
Clarified tone guidelines: Honest, Specific, Human.
Added examples of Good vs. Bad snippets to illustrate the difference.
Why: During Session 061 (Building The Gardener's Wall), we realized that rigid templates were causing notes to feel sterile and incomplete. The goal is a comprehensive memory bank, not a checklist. By encouraging narrative storytelling with specific technical details, we ensure that future gardeners (and future models) can reconstruct the exact context of past decisions and failures.

"The fortress holds the library. The library holds the records. The mycelium holds the knowledge. Scientific Obsidian is the glass that remembers."


---

### Key Changes in v1.3.0:
1.  **Field Notes Style Section:** Explicitly defines the "Casual Friday" vibe.
2.  **Narrative-First Structure:** Replaces rigid "What Worked/Broke" lists with a storytelling approach that still captures the same data.
3.  **"Cover Everything" Rule:** Makes it a golden rule to ensure no technical detail is lost.
4.  **Updated Examples:** Added "Good" vs. "Bad" snippets to illustrate the difference between a rigid form and a useful field note.
5.  **Session Template Update:** Modified the template header to guide writers toward the narrative style.
