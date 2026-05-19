---
phase: 37
date: 2026-05-15
status: Active — Vault operational, backfilling in progress
related: [[Note-Taking Protocol]], [[Architecture Overview]], [[Session-006]], [[Session-007]], [[Dr-Rebentisch-Twin-Mycelium]]
---

# Phase 37: Scientific Obsidian — The CADMIES Knowledge Vault

## What It Is

Scientific Obsidian is the CADMIES scientific documentation system — an Obsidian.md vault serving as the formal lab notebook, decision log, and architectural record for the entire project. It lives alongside the code repository and will eventually be integrated into the public GitHub repo under `/docs/vault/`.

## The Metaphor (CADMIES Canon)

- **Cosmium Angelo** — the conceptual fortress (CADMIES's Fort Saint Angelo). Stone walls, timeless, immovable. The container.
- **Scientific Obsidian** — the library within the fortress. Volcanic glass shelves formed from conversations that cooled before they could crystallize into dogma. Frozen lava, perfect for recording.
- **CADMIES Mycelium** — the living knowledge network growing THROUGH the obsidian shelves. Concepts, edges, Willie, the harvester, the gardener, Number 5. It's the life that weaves through it.

Three layers, one system: the fortress holds the library, the library holds the records, the mycelium holds the living knowledge.

## Vault Structure

CADMIES-Vault/  
├── 00-Meta/ # How the vault works  
│ └── Note-Taking Protocol.md  
├── Raw CADMIES/ # Primary workspace — live notebook  
│ ├── Scratchpad/  
│ ├── Ideas/  
│ └── Session-Notes/  
├── Polished CADMIES/ # Secondary — structured, PhD-ready  
│ ├── 01-System/  
│ ├── 02-Pipeline/  
│ ├── 03-Development/  
│ ├── 04-Concepts/  
│ └── 05-Collaboration/  

## Methodology

- Influenced by Dr. Rupert Rebentisch's zettelkasten methodology (tools4zettelkasten) and the Luhmann/Ahrens/Forte tradition of atomic, densely-linked knowledge management
- Casual Friday approach — lenient, chill, learn-as-we-go. Rigor increases organically.
- Atomic notes with double bracket linking — each note is a node in the graph
- Two layers: Raw CADMIES (primary workspace, mistakes welcome) and Polished CADMIES (structured, PhD-ready)
- Promotion criteria: clear title, structured content, linked evidence, appropriate subfolder
- Credit where credit is due — all influences and collaborators documented

## Current Status

### Notes Created (as of Session 007)

| Note | Location | Status |
|------|----------|--------|
| Note-Taking Protocol | 00-Meta/ | Complete |
| Architecture Overview | 01-System
## Methodology

- Influenced by Dr. Rupert Rebentisch's zettelkasten methodology (tools4zettelkasten) and the Luhmann/Ahrens/Forte tradition of atomic, densely-linked knowledge management
- Casual Friday approach — lenient, chill, learn-as-we-go. Rigor increases organically.
- Atomic notes with double bracket linking — each note is a node in the graph
- Two layers: Raw CADMIES (primary workspace, mistakes welcome) and Polished CADMIES (structured, PhD-ready)
- Promotion criteria: clear title, structured content, linked evidence, appropriate subfolder
- Credit where credit is due — all influences and collaborators documented

## Current Status

### Notes Created (as of Session 007)

| Note | Location | Status |
|------|----------|--------|
| Note-Taking Protocol | 00-Meta/ | Complete |
| Architecture Overview | 01-System/ | Complete |
| Harvester Pipeline | 02-Pipeline/ | Complete |
| Phase 35 — Difficulty Levels | 03-Development/ | Complete |
| Phase 35 — Results | 03-Development/ | Complete |
| Phase 37 — Scientific Obsidian | 03-Development/ | This note |
| Session 006 | Raw CADMIES/Session-Notes/ | Complete |
| Session 007 | Raw CADMIES/Session-Notes/ | Complete |

### Pending Notes

| Note | Location | Priority |
|------|----------|----------|
| Decisions Log | 03-Development/ | High |
| Paperspace Session Protocol | 01-System/ | High |
| Two-System Setup | 01-System/ | Medium |
| Three-Model Arsenal | 01-System/ | Medium |
| Relationship Generator | 02-Pipeline/ | Medium |
| Mycelium Map | 02-Pipeline/ | Medium |
| Public Gateway | 02-Pipeline/ | Medium |
| Dr. Rebentisch — Twin Mycelium | 05-Collaboration/ | Medium |
| CADMIES Canon | 01-System/ | Low |
| Session 001-005 backfill | Raw CADMIES/Session-Notes/ | Low |

## Key Design Decisions

1. **Public by default.** The vault is open notebook science. Mistakes and all.
2. **Raw first, polished second.** The gardener works in Raw CADMIES. PhDs browse Polished CADMIES.
3. **YAML frontmatter for polished notes.** Raw notes use a banner instead.
4. **No `---` dividers in body text.** Uses `***` to avoid YAML parser conflicts.
5. **Vault will join the repo** under `/docs/vault/` with `.obsidian/` workspace folder gitignored.

## Soundtrack

The vault captures not just decisions and results, but the human context. Session soundtracks are documented in raw session notes. Notable additions so far:

- Tears for Fears, The Ink Spots, The White Stripes, The Wallflowers, Weezer, Jet, The Blur, Franz Ferdinand, The Rolling Stones, Dire Straits, The Hollies, The Beatles, Violent Femmes

## Nuggets Logged

- "The fortress holds the library. The library holds the records. The mycelium holds the knowledge."
- "Scientific Obsidian is the glass that remembers."
- "It's the life that weaves through it."
- "We are the Sultans of Knowledge" (homage to Dire Straits)

## Next Actions

- Add vault to GitHub repo under `/docs/vault/`
- Create Decisions Log and backfill from sessions
- Document Paperspace Session Protocol
- Backfill earlier sessions as time allows
- Establish CADMIES Canon note for lore and metaphors