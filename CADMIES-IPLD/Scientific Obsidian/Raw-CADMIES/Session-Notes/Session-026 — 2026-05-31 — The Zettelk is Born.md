> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 026 — 2026-05-31 — The Zettelk is Born

related: [[Session-025]], [[Dr-Rebentisch-Twin-Mycelium]], [[Phase-37-Scientific-Obsidian]]

## What We Did

**Cloned Dr. Rebentisch's tools4zettelkasten and built our own Zettelkasten.**

The twin mycelia are no longer just a concept — they're running on the same infrastructure. 
We cloned the doctor's repo, studied his methodology, and set up Scientific-Obsidian-Zettelk 
("Zettelk" for short) as our process memory. The thing neither the gardener nor the AI can 
keep in our heads.

### Paperspace Setup (CADMIES-Zettelkasten notebook)

- Cloned `rreben/tools4zettelkasten` to `/notebooks/tools4zettelkasten`
- Created `/notebooks/Scientific-Obsidian-Zettelk/` with `input/` and `mycelium/` directories
- Configured `.env` pointing at our paths
- Installed tools4zettelkasten in editable mode
- Verified with `python -m tools4zettelkasten settings` — all green checkmarks
- Staged first note: CADMIES — Genesis — Chapter I
- Flask server runs at port 5001 (Paperspace port forwarding TBD)

### Local Setup (Fedora Silverblue, PNY drive)

- Created `/run/media/fedora/PNY/CADMIES-Zettelk/` next to CADMIES-IPLD
- Hit Python 3.14 incompatibility — `ast.Str` removed, doctor's code needs ≤3.12
- Silverblue doesn't have `dnf` — used `toolbox` container with Fedora 39
- Toolbox provides Python 3.12 — works with doctor's code
- Hit `__version__` import error — doctor's repo has `_version.py` but `cli.py` imports 
  `__version__`. Created bridge file. Janky fix but it works.
- Had to install `graphviz` system package for the Flask GUI graph view
- Flask GUI renders — looks EXACTLY like our mycelium map. Zoom, pan, nodes, edges. 
  Convergent evolution even in the UI.

### The Workflow (Dead Simple)

1. Write a markdown note with a `# Title` at the top
2. Drop it in `input/`
3. Run `python -m tools4zettelkasten stage` — renames with hash ID and ordering number
4. Move renamed file to `mycelium/`
5. Link to other notes using `[Title](filename_with_hash.md)`
6. Run `python -m tools4zettelkasten reorganize` when numbering gets messy

No folders. No categories. The links ARE the organization.

### The Discovery

Obsidian's graph view and the doctor's Flask GUI and our CADMIES mycelium map are all 
the same visual language. Two independent projects, zero contact, same interface. The 
mycelial pattern shapes everything — data structure, architecture, even button placement.

Convergent evolution confirmed at the UI level.

### How Zettelk Fits With Scientific Obsidian

- **Zettelk** = workbench. Fast, messy, private. Where ideas are born.
- **Scientific Obsidian** = display case. Polished phase notes, protocols, public.
- Zettelk feeds Obsidian over time. When notes mature, they get promoted.
- We do NOT backfill old Obsidian notes into Zettelk. Clean start from today.

## Decisions Made

- Zettelk stays in its own notebook on Paperspace, separate from IPLD and Narrative
- Local Zettelk lives on PNY next to CADMIES-IPLD, in a toolbox container
- Flask GUI for visual browsing, Obsidian for local viewing (eventually)
- Doctor's tools stay untouched — we patch around issues, not modify his code
- The `__version__` bridge file is a temporary fix — report upstream later

## Bugs & Fixes

- Python 3.14 `ast.Str` removal → use toolbox with Python 3.12
- Missing `__version__.py` → created bridge to `_version.py`
- Missing Graphviz → `sudo dnf install graphviz` in toolbox
- Silverblue no `dnf` → toolbox container workflow

## Soundtrack

- Quiet engineering session. Focus vibes. The doctor's figlet ASCII art is the soundtrack.

## Nuggets

- "The Zettelk is the prosthetic memory neither of us has."
- "Drop notes. Run stage. Move to mycelium. Link. Repeat forever."
- "Even the buttons converged. The mycelial pattern is real."
- "Zettelk for work, Obsidian for show."
- "We're holding the mad scientist's notebook and he put it on GitHub on purpose."

## Next Actions

- Feed more notes into Zettelk — session protocols, roadmaps, decisions
- Get Paperspace port forwarding working for Flask GUI
- Eventually point Obsidian at the Zettelk `mycelium/` folder for local graph view
- Post the Twin Mycelium Integration Proposal issue to Dr. Rebentisch
- Consider reporting `__version__` import bug upstream