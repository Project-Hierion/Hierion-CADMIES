> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 037 — 2026-07-16 — The Mycelium Cleans Itself

## Soundtrack
The Black Pumas — "Howlin' For You"
Marvin Gaye — "What's Going On"
Donna Summers — "Try Me" (full album cut)
Too $hort — "Gettin' It"
Saint Motel — "My Type"
Lil Dicky — "Save Dat Money"
Rick James — Mary Jane — the song, and the flower, and the girl, whole session

## What We Did

**Built repo-maintenance-automation from scratch.** A vault validator that scans every markdown file in Scientific Obsidian and reports on frontmatter consistency, dead wikilinks, missing sections, duplicate files, and roadmap drift.

Started at 135 issues across 83 files. Ended at 0 issues across 90 files.

### The Validator
- v1.0.0: Read-only reporter. Checks frontmatter, sections, banners, cross-refs, duplicates, roadmap.
- v1.0.1: Fixed YAML parser to handle [[wikilinks]] with commas. Fixed duplicate self-comparison bug.
- v1.0.2: Skip .ipynb_checkpoints and hidden directories (caught by Paperspace run).
- v1.1.0: --fix mode with before/after previews, interactive confirmations, automatic backups.
- v1.2.0: Dead wikilink auto-fix via fuzzy filename matching. 51 links fixed in one pass.
- v1.2.1: Added .md extension check. Caught 7 files missing extensions.

### What Got Fixed
- 72 dead wikilinks resolved (auto-fix + manual)
- 16 genuinely dead links removed (targets never existed)
- 13 phase notes got missing section placeholders
- 7 files missing .md extension discovered and fixed
- Session-025 split into 025A (Index Recovery) and 025B (Buttercup)
- Phase 45G filename sanitized (colon removed)
- All emojis stripped from polished notes for PhD/scientific standards
- Roadmap synced with all phase notes
- Phase 57 frontmatter repaired (missing YAML delimiters)
- Phase 66 status corrected to "Designed, Postponed"

### Infrastructure
- GitHub Action: vault-check.yml runs validator on every push to main
- Status badge added to README
- automation-README.md created
- Branch: repo-automation-testing → merged to main → deleted
- Tested across Codespaces and Paperspace
- Base Codestral gave clean code review

## What Worked
- Fuzzy matching for dead links is surprisingly accurate
- --fix mode with before/after previews is the right UX
- Automatic backups before every modification = trust
- The .ipynb_checkpoints skip saved us from Paperspace artifact noise
- Session-025A/025B split makes the vault more navigable

## What Broke
- Initial YAML parser failed on [[wikilinks]] with commas
- Duplicate detector compared files against themselves
- & in filenames got encoded as &amp; by sed
- Emoji strip accidentally ate "status:" prefix on some files
- Multiple push conflicts from gardener editing on two machines simultaneously

## Decisions Made
- Wikilinks use full filenames, not shorthand
- Polished notes: no emojis. Scientific audience.
- Placeholder sections acceptable for older notes (better than missing structure)
- Test branch workflow: build on test branch, merge to main when clean
- Descriptive naming convention: repo-maintenance-automation, not just automation/

## Nuggets Collected
- "The mycelium cleans itself." — the validator is the immune system
- 135→0 in one session. 79% reduction in first pass, 100% by end.
- "Save dat money" — all free tools: Python, GitHub Actions, YAML
- The robot secretary actually works
- Mary Jane was the third gardener today
