---
date: 2026-05-15
status: Living document — updated with each decision
related: [[Architecture Overview]], [[Note-Taking Protocol]]
---

# Decisions Log

A chronological record of architectural, design, and process decisions made across all CADMIES sessions. Each entry captures what was decided, why, and where the discussion happened.

***

## 2026-05-15 — Session 007

### Paperspace Uses Git Clone as Source of Truth

**Decision:** The Paperspace GPU workspace now uses a git clone (`/notebooks/CADMIES/CADMIES-IPLD/`) instead of bare files uploaded via tar.

**Rationale:** Code travels by git, data travels by tar. Two pipes, no confusion. The old approach of uploading individual files or tarballs of the whole project created version mismatches and duplicate directories. A git clone ensures Paperspace always has the latest code with a single `git pull`.

**Cleanup:** All legacy files in `/notebooks/` were deleted except the CADMIES clone and `.Trash-0`.

### Scientific Validator Version Suffix Purged

**Decision:** Removed `_v1_0_0` suffix from `ScientificValidator` class in `scientific_validator.py`. Changed to `ScientificValidator` (no suffix).

**Rationale:** Version suffixes were purged from class names in Session 4, but this file was missed. The mismatch caused an ImportError during the v4.1.0 harvest test. Consistency across the codebase — no versioned class names.

### Scientific Obsidian Vault — Public by Default

**Decision:** The CADMIES vault (Scientific Obsidian) is 100% public, open notebook science. Mistakes included.

**Rationale:** Aligns with the project's CC BY-SA 4.0 license and open science ethos. Dr. Rebentisch's twin mycelium and any future collaborators can see the full process, not just polished outputs. The mycelium doesn't hide its dead ends.

### Scientific Obsidian Vault — Will Join GitHub Repo

**Decision:** The vault will be added to the CADMIES GitHub repo under `/docs/vault/`.

**Rationale:** Single source of truth for all CADMIES materials — code, concepts, documentation, lab notebook. GitHub renders markdown natively, making the vault browsable without Obsidian. The `.obsidian/` workspace folder will be gitignored to keep the repo clean.

### Two-Layer Vault Structure: Raw CADMIES + Polished CADMIES

**Decision:** The vault has two workspaces: Raw CADMIES (primary, live notebook, mistakes welcome) and Polished CADMIES (secondary, structured, PhD-ready).

**Rationale:** The gardener works in Raw by default. PhDs browse Polished. Clear promotion criteria govern what moves from Raw to Polished. This keeps the workflow natural for the primary user while maintaining a clean interface for external readers.

### Markdown Protocol: No `---` Dividers in Body Text

**Decision:** All section dividers in vault notes use `***` instead of `---`. The only `---` in any note is the YAML frontmatter block at the very top.

**Rationale:** Obsidian's YAML parser treats every `---` as a potential frontmatter closer. Multiple `---` in a document breaks the metadata header. `***` renders identically as a horizontal rule but doesn't confuse the parser.

### GPU Requirement Documented in Harvester Header

**Decision:** Added explicit GPU requirement note to `harvest_full_pipeline.py` file header.

**Rationale:** The harvester makes multiple LLM calls per concept. CPU-only users need to know this upfront. The note specifies minimum VRAM (6GB for Mistral 7B, 12GB+ for Codestral) and points to the manual import path for CPU users. Transparency about hardware requirements.

***

## 2026-05-14 — Session 006

### Two-Pass Architecture for Concept Extraction

**Decision:** The harvester will evolve to a two-pass architecture. Phase 1 extracts core concepts (name, definition, three-tier explanations, domain, poetics, mantra). Phase 2 enriches with scholarly fields (type, subdomain, limitations, applications, historical_context, discoverer, discovery_year, key_references).

**Rationale:** Separating extraction and enrichment keeps the extraction prompt focused and fast. Enrichment can use a different model (Codestral for depth) and be optional (flag-controlled). Matches the early template concepts like bayes_theorem that had these fields.

### Three-Tier Difficulty Levels Restored

**Decision:** Updated the harvester extraction prompt to request three distinct explanations per concept: beginner, intermediate, expert. Updated `transform_to_concept()` to map them with a fallback chain.

**Rationale:** Early CADMIES concepts (bayes_theorem) had distinct tiers. The harvester lost this when built — both beginner and intermediate used the same definition string. Restoring it matches the original schema design and makes the public gateway's difficulty tabs functional.

### Methodology: Influenced by Dr. Rebentisch, Not Cloned

**Decision:** Scientific Obsidian follows the zettelkasten methodology (atomic notes, dense linking) influenced by Dr. Rupert Rebentisch and the Luhmann/Ahrens/Forte tradition, but does not clone his system or tools.

**Rationale:** We're students of the method, not clones of the implementation. Credit where it's due, but CADMIES needs its own conventions. Casual Friday approach to start, rigor increases organically.

### Roadmap on GitHub, Vault on Obsidian

**Decision:** The roadmap (`growth_roadmap.md`) stays on GitHub. The vault documents how and why we execute it.

**Rationale:** Roadmap = what and when (public-facing project plan). Vault = how and why (scientific record). Different documents, different homes.

***

## Template for New Decisions
### Decision Title

**Decision:** What was decided.

**Rationale:** Why this choice was made.

**Alternatives Considered:** What else was on the table.

**Related:** [[linked-note]], Session-XXX