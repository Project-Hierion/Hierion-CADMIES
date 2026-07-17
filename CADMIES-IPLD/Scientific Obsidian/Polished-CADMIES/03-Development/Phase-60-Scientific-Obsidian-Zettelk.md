---
phase: 60
date: 2026-05-31
status: Complete — Zettelk operational on Paperspace and local
related: [[Phase-37-Scientific-Obsidian]], [[Dr. Rebentisch — Twin Mycelium]], [[Session-026 — 2026-05-31 — The Zettelk is Born]]
---

# Phase 60: Scientific-Obsidian-Zettelk — Process Memory Infrastructure

## What Changed

Dr. Rupert Rebentisch's `tools4zettelkasten` system was cloned, studied, and deployed as the CADMIES process memory — a dedicated Zettelkasten for tracking sessions, decisions, protocols, roadmaps, and the operational knowledge that neither the gardener's memory nor the AI's context window can reliably retain across sessions. The system was deployed identically on Paperspace (CADMIES-Zettelkasten notebook) and locally on the Fedora Silverblue machine (PNY drive, toolbox container). The first note — CADMIES Genesis — was staged and served through the Flask GUI. The twin mycelium infrastructure is now operational at both the concept level (CADMIES mycelium map) and the process level (Scientific-Obsidian-Zettelk).

## Why

The CADMIES project has accumulated 60+ phases, 26+ sessions, dozens of protocols, and hundreds of decisions across six months of work. The gardener has limited memory capacity. The AI co-pilot (Number 5) has a limited context window that resets every session. Both need an external brain — a persistent, linkable, visually navigable system that tracks what was decided, when, and why.

Scientific Obsidian (Phase 37) addresses the public-facing documentation need — polished phase notes, architecture docs, protocols visible on GitHub. But it is a publication layer, not a working memory. The Zettelk fills the gap: a fast, messy, private workspace where ideas form and link together before they're ready for public promotion.

Dr. Rebentisch's system was chosen because:
1. It is architecturally convergent with CADMIES — same mycelial pattern, same node-edge-link philosophy
2. It provides a proven staging workflow (`input/` → `stage` → `mycelium/`)
3. It includes a visual Flask GUI with graph view — convergent even at the UI level with our mycelium map
4. The doctor is already a CADMIES collaborator — using his tools deepens the twin mycelium connection

## Deployment

### Paperspace (CADMIES-Zettelkasten Notebook)

**Project:** CADMIES-Gradient
**Notebook:** CADMIES-Zettelkasten (alongside CADMIES-IPLD and CADMIES-Narrative)
**Repository:** `github.com/rreben/tools4zettelkasten` cloned to `/notebooks/tools4zettelkasten`
**Zettelk path:** `/notebooks/Scientific-Obsidian-Zettelk/`

**Directory structure:**

/notebooks/Scientific-Obsidian-Zettelk/  ---

## Session 027 Update — Paperspace Deployment & The Grounding Problem (2026-06-03)

### Paperspace Deployment Complete

The Zettelk was deployed in a new dedicated Paperspace project (Paperspace-Zettelk) with a start-from-scratch notebook. A startup script (`/notebooks/Scientific-Obsidian-Zettelk/startup.sh`) handles full recovery from container resets: zstd, tools4zettelkasten, __version__ fix, RAG dependencies, rag.py Ollama patch, Ollama install, and Mistral 7B pull. All 82 notes were imported from the local Zettelk via tarball and vectorized. The RAG chat is operational with Mistral 7B and Codestral 22B on GPU, achieving 71+ tokens/second.

### The Grounding Problem — Scientific Discovery

Testing across three models (TinyLlama 1.1B, Mistral 7B, Codestral 22B) on two independent machines (local CPU, Paperspace GPU) revealed a consistent hallucination: all models retrieve the correct source notes about Dr. Rupert Rebentisch but conclude he is a fictional character. A grounding note explicitly stating the reality of the project and collaborators was added to the Zettelk — models interpreted it as part of the fiction.

**Root cause:** The poetic, metaphor-rich documentation style of CADMIES triggers a "creative writing = fiction" heuristic in current open-weight LLMs. The models override explicit factual statements in retrieved context with their own interpretation of the documentation style. The retrieval pipeline (ChromaDB + sentence-transformers) works perfectly. The error is in the generation/reasoning step.

**Implications:** Any project using creative or metaphorical language in technical documentation may encounter similar issues with open-weight LLM RAG systems. This is documented as a known limitation.

**Potential solutions (untested):**
- Drier documentation style (rejected — the style is intentional)
- Stronger system prompt engineering
- Metadata flags for factual status
- Larger paid models (GPT-4o, Claude) with better reasoning
- Acceptance of the limitation for local models

### Next Steps Updated

| #   | Action                                                         | Priority |
| --- | -------------------------------------------------------------- | -------- |
| 1   | Await Dr. Rebentisch's response to GitHub issue                | 🟡       |
| 2   | Test dryer grounding note with URLs                            | 🟢       |
| 3   | Evaluate GPT-4o or Claude API for chat                         | 🟢       |
| 4   | Continue feeding session protocols into Zettelk                |        |
| 5   | Draft technical issue for Dr. Rebentisch re: grounding problem | 🟡       |
├── .env # Configuration pointing at input/ and mycelium/  
├── input/ # Raw notes awaiting staging  
│ └── images/  
└── mycelium/ # Permanent zettels with hash IDs  
└── images/


**Configuration (.env):**

ZETTELKASTEN=/notebooks/Scientific-Obsidian-Zettelk/mycelium/  
ZETTELKASTEN_INPUT=/notebooks/Scientific-Obsidian-Zettelk/input/  
ZETTELKASTEN_IMAGES=/notebooks/Scientific-Obsidian-Zettelk/mycelium/images


**Installation:** `pip install -e .` from the tools4zettelkasten directory. All dependencies resolved cleanly. Flask server runs at port 5001 (Paperspace port forwarding pending).

### Local (Fedora Silverblue, PNY Drive)

**Machine:** HP/Fedora Silverblue 44
**Drive:** PNY removable storage
**Zettelk path:** `/run/media/fedora/PNY/CADMIES-Zettelk/`
**Container:** Toolbox `zettelk-tools` (Fedora 39, Python 3.12)

**Why Toolbox:**
Fedora Silverblue does not use `dnf` for system packages. The system Python is 3.14, which is incompatible with `tools4zettelkasten` (requires `ast.Str`, removed in Python 3.13). A toolbox container provides an isolated Fedora 39 userspace with Python 3.12 and full `dnf` access — the cleanest Silverblue-native solution.

**Installation issues resolved:**
1. **Python version:** System 3.14 incompatible → toolbox with Python 3.12
2. **Missing `__version__`:** `cli.py` imports `from . import __version__` but the repo only has `_version.py` → created bridge file `__version__.py` that re-exports from `_version`
3. **Missing Graphviz:** Flask GUI graph view requires `dot` binary → `sudo dnf install graphviz` in toolbox

**Directory structure and .env identical to Paperspace deployment.**

### The Staging Workflow

The doctor's workflow, adapted for CADMIES:

1. **Write:** Create a markdown file with a `# Title` heading at the top
2. **Drop:** Place the file in `input/`
3. **Stage:** Run `python -m tools4zettelkasten stage` — renames file with alphanumeric ordering and unique hash ID
4. **Review:** The staged file stays in `input/` after renaming — manual review step
5. **Publish:** Move the renamed file from `input/` to `mycelium/`
6. **Link:** Add `[Link Text](filename_with_hash.md)` references to connect zettels
7. **Reorganize:** Run `python -m tools4zettelkasten reorganize` when numbering needs cleanup

**Key principle:** No folders, no categories. The links ARE the organization. Notes live flat in `mycelium/`. The alphanumeric ordering provides a browseable sequence. The hash IDs ensure links survive renames and reorganizations.

### Visual Browsing

**Flask GUI:** `python -m tools4zettelkasten start` launches a web server at `http://127.0.0.1:5001`. Provides:
- List view of all zettels
- Individual note rendering (Markdown → HTML)
- Clickable links between notes
- SVG graph visualization of the Zettelk network

**Obsidian (future):** The `mycelium/` directory can be opened as an Obsidian vault for native graph view, backlinks panel, and quick search — identical to how Scientific Obsidian works today.

### First Note Staged

The CADMIES Genesis document (CADMIES — Genesis — Chapter I) was the first note processed through the pipeline. It received hash ID `b0c14c361` and ordering prefix `0_0`. It is now a permanent zettel in `mycelium/`, viewable through the Flask GUI.

## Relationship to Scientific Obsidian

The Zettelk and Scientific Obsidian serve different purposes:

| | Scientific-Obsidian-Zettelk | Scientific Obsidian |
|---|---|---|
| **Purpose** | Working memory, process tracking | Public documentation |
| **Audience** | Gardener + AI co-pilot | GitHub visitors, collaborators |
| **Tone** | Messy, fast, half-formed | Polished, structured, PhD-ready |
| **Visibility** | Private (local + Paperspace) | Public (GitHub repo) |
| **Flow** | Ideas are born here | Ideas graduate to here |

**Promotion path:** Zettelk notes that mature into reusable knowledge get written up formally and added to Scientific Obsidian. The Zettelk is the nursery. Scientific Obsidian is the display garden.

## Convergence Confirmed at UI Level

The doctor's Flask GUI graph view and the CADMIES mycelium map (D3.js, v2.4.0) share identical interaction patterns: zoom, pan, node-click-to-focus, force-directed layout. Two independent projects on two continents, zero coordination, same visual language.

This extends the twin mycelium convergence beyond architecture (documented in Phase 37) into user experience design. The mycelial pattern shapes not just data structures but the interfaces humans use to navigate them.

## Issues Encountered

### Python 3.14 Incompatibility (Local)
`ast.Str` was removed in Python 3.13. The doctor's codebase uses it in `flask_views.py`. Resolution: run inside a toolbox container with Python 3.12. This is a Silverblue-specific issue — Paperspace uses Python 3.11 and is unaffected.

### Missing __version__ Module
The repository contains `_version.py` (with the `__version__` variable) but `cli.py` imports `from . import __version__` which expects a module named `__version__`. Created a one-line bridge file. This may be an upstream bug or an artifact of the editable install. Deferred reporting.

### Graphviz System Dependency
The Python `graphviz` package requires the `dot` binary at the system level. Not installed by default in the toolbox. Resolution: `sudo dnf install graphviz`.

## Decisions Made

1. **Dedicated notebook on Paperspace.** Zettelk lives in CADMIES-Zettelkasten, separate from IPLD and Narrative notebooks. Prevents dependency conflicts.
2. **Toolbox container for local.** Silverblue-native solution. Isolates Python 3.12 from system Python 3.14. Clean separation from CADMIES-IPLD venv.
3. **Flat `mycelium/` structure.** No subfolders by topic or phase. The Zettelkasten method relies on links for organization, not directory hierarchy.
4. **No backfill from Scientific Obsidian.** The Zettelk starts fresh from today. Old Obsidian notes stay in Obsidian. New process notes go into the Zettelk.
5. **Doctor's tools untouched.** Patches applied externally (bridge file) rather than modifying his source. Upstream-friendly.

## Conclusion

The Scientific-Obsidian-Zettelk is operational on both Paperspace and local Fedora. It provides the process memory infrastructure that neither the gardener nor the AI co-pilot possess natively. The staging workflow is proven, the Flask GUI is running, and the first note is staged.

The twin mycelium — CADMIES for concept mapping, Zettelk for process memory — is now a functioning reality. Both systems use the same mycelial pattern. Both were built independently and converged naturally. Both are now deployed side by side, maintained by the same gardener, ready to feed each other over time.

## Next Steps

| # | Action | Priority |
|---|--------|----------|
| 1 | Feed session protocols and roadmaps into Zettelk |  |
| 2 | Get Paperspace port forwarding working for Flask GUI | 🟡 |
| 3 | Post Twin Mycelium Integration Proposal to Dr. Rebentisch | 🟡 |
| 4 | Point local Obsidian at Zettelk `mycelium/` for graph view | 🟢 |
| 5 | Report `__version__` import issue upstream | 🟢 |
| 6 | Develop promotion criteria for Zettelk → Scientific Obsidian | 🟢 |

---

## Session 027 Update — Paperspace Deployment & The Grounding Problem (2026-06-03)

### Paperspace Deployment Complete

The Zettelk was deployed in a new dedicated Paperspace project (Paperspace-Zettelk) with a start-from-scratch notebook. A startup script (`/notebooks/Scientific-Obsidian-Zettelk/startup.sh`) handles full recovery from container resets: zstd, tools4zettelkasten, __version__ fix, RAG dependencies, rag.py Ollama patch, Ollama install, and Mistral 7B pull. All 82 notes were imported from the local Zettelk via tarball and vectorized. The RAG chat is operational with Mistral 7B and Codestral 22B on GPU, achieving 71+ tokens/second.

### The Grounding Problem — Scientific Discovery

Testing across three models (TinyLlama 1.1B, Mistral 7B, Codestral 22B) on two independent machines (local CPU, Paperspace GPU) revealed a consistent hallucination: all models retrieve the correct source notes about Dr. Rupert Rebentisch but conclude he is a fictional character. A grounding note explicitly stating the reality of the project and collaborators was added to the Zettelk — models interpreted it as part of the fiction.

**Root cause:** The poetic, metaphor-rich documentation style of CADMIES triggers a "creative writing = fiction" heuristic in current open-weight LLMs. The models override explicit factual statements in retrieved context with their own interpretation of the documentation style. The retrieval pipeline (ChromaDB + sentence-transformers) works perfectly. The error is in the generation/reasoning step.

**Implications:** Any project using creative or metaphorical language in technical documentation may encounter similar issues with open-weight LLM RAG systems. This is documented as a known limitation.

**Potential solutions (untested):**
- Drier documentation style (rejected — the style is intentional)
- Stronger system prompt engineering
- Metadata flags for factual status
- Larger paid models (GPT-4o, Claude) with better reasoning
- Acceptance of the limitation for local models

### Next Steps Updated

| # | Action | Priority |
|---|--------|----------|
| 1 | Await Dr. Rebentisch's response to GitHub issue | 🟡 |
| 2 | Test dryer grounding note with URLs | 🟢 |
| 3 | Evaluate GPT-4o or Claude API for chat | 🟢 |
| 4 | Continue feeding session protocols into Zettelk |  |
| 5 | Draft technical issue for Dr. Rebentisch re: grounding problem | 🟡 |