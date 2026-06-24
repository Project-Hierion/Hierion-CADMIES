# CADMIES-IPLD

> **📢 June 23, 2026 — Project Renamed**
> 
> CADMIES was previously under **Project Hieros** and hosted at
> `Hieros-CADMIES/CADMIES`. We changed our name to **Project Hierion**
> (ἱερόν — Greek for "sacred place") to avoid naming conflicts with existing
> organizations, research initiatives, and publications that share
> the "Hieros" name, while maintaining ties to the name's origin. The project, the mycelium, and the mission are
> unchanged. All old URLs redirect to our new home:
> **New GitHub:** [github.com/Project-Hierion/CADMIES](https://github.com/Project-Hierion/CADMIES)
> (old URL redirects automatically)
> 
> **New Public Gateway:** [project-hierion.duckdns.org](https://project-hierion.duckdns.org)
> (replaces the retired GitHub Pages site) A private domain will come later.

**Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem**

A philosophical and technical framework for content-addressed, scientifically-validated knowledge storage and sharing. 636 interconnected concepts. 1,131 cross-domain relationships. 107 domains (15 canonical). One digital mycelium. Infinite connections.

🌍 **Public Gateway:** [project-hierion.duckdns.org](https://project-hierion.duckdns.org/)

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Project-Hierion/CADMIES.git
```

Change to the project directory:

```bash
cd CADMIES/CADMIES-IPLD
```

Install dependencies:

```bash
pip install dag-cbor multiformats requests
```

Read a concept by name:

```bash
python tools/core/cbor_reader.py natural_selection
```

Generate a concept from a JSON file:

```bash
python tools/core/cid_generator.py --concept-file source_concepts/example.json
```

## Import the Full Mycelium (Recommended)

The clone includes only seed blocks. All other concepts are distributed via CAR releases. Import the full collection:

```bash
python tools/import_from_github.py --url https://github.com/Project-Hierion/CADMIES/releases/download/v0.4.0/full_mycelium_v0.4.0.car
```

## Ask the Librarian (LLM Agent)

CADMIES uses a two-part AI architecture for natural language queries:

Willie the Research Assistant (cadmies_concept_reader.py) is the Python retriever — a Scottish groundskeeper who knows where everything is filed. He searches the mycelium using hybrid search (keyword + semantic), finds relevant concepts, and feeds them as context to the LLM. Silent. Fast. Pattern-driven.

Mistral (The Librarian) is the LLM that receives Willie's research, synthesizes the concepts, and presents answers to the user in natural language. She is the senior — the voice you actually speak with.

Together: User asks a question → Willie searches the stacks → Willie feeds relevant concepts to Mistral → Mistral speaks the answer.

### Prerequisites:

Install Ollama and pull the models:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral:7b      # The Librarian (recommended)
ollama pull tinyllama:1.1b   # Fast queries
ollama pull codestral:22b    # Maximum depth (GPU recommended)
```

Install the Ollama Python client:

```bash
pip install ollama
```

### Launch Ollama (Terminal 1 — keep running in background):

```bash
# 24-hour keep-alive keeps the model warm for instant responses
OLLAMA_KEEP_ALIVE=24h ollama serve &
```

### Ask the Librarian (Terminal 2):

```bash
cd CADMIES/CADMIES-IPLD && source venv/bin/activate
python agents/code/cadmies_concept_reader.py --query "What is natural selection?" --model mistral:7b
```

### How it works:

Willie searches all concepts using hybrid search (keyword + semantic)

Willie feeds the top matches to Mistral as context

Mistral returns answers with accuracy tags: (empirical), (philosophical), (speculative), (CADMIES-defined)

Every concept is referenced by its permanent CID

### Model strategy:
```text
Model              Role                 Size      Speed     Best For
TinyLlama 1.1B     Backup Librarian     637 MB    ~2s       Quick lookups
Mistral 7B         The Librarian        4.4 GB    ~5-30s    Deep reasoning, relationship generation
Codestral 22B      Senior Scholar       12 GB     ~15-45s   Maximum depth, library audits (GPU recommended)
Dr. Amanda Mistral CADMIES Librarian    ~4 GB     ~5-30s    CADMIES knowledge Q&A, character interactions
Everything runs locally. No API keys, no cloud, no external calls.
```

"Ach, let me dig through the stacks for ye..." — Willie the Research Assistant

"Here's what the mycelium knows about that." — Mistral the Librarian

## GPU Acceleration (Cloud)

CADMIES supports cloud GPU acceleration for heavy batch processing, relationship generation, harvest pipeline extraction, and concept enrichment. A dedicated GPU handles tasks in seconds that take minutes on CPU.

### Quick GPU session:

Clone the repository:

```bash
git clone https://github.com/Project-Hierion/CADMIES.git /notebooks/CADMIES/
```

Run the startup script:

```bash
cd /notebooks/CADMIES/CADMIES-IPLD && bash startup.sh
```

This installs Ollama, pulls Mistral, and sets up all dependencies in ~30 seconds. Persistent storage keeps your models and blockstore between sessions. To use other models:

```bash
ollama pull codestral:22b    # Deep philosophy, audits
ollama pull tinyllama:1.1b   # Willie quick searches
```

### One-command harvest-to-map with auto-relationships:

```bash
python harvest/harvest_full_pipeline.py --auto --with-relationships
```

Extracts concepts, auto-approves them, mints to the blockstore, regenerates the mycelium map, and auto-generates relationships — all in one command. No orphans. The pipeline feeds itself.

### Harvest modes:

Full auto: --auto --with-relationships — no pauses, complete hands-off pipeline

Review mode: --with-relationships — pauses for human approval before minting

Model selection: --model=codestral:22b or --model=mistral:7b

Concept Enrichment:

New in v4.1.0+: enrich existing concepts with missing scholarly fields (type, subdomain, historical context, limitations, applications, key references). Two-pass pipeline: schema normalization followed by LLM enrichment.

```bash
# Enrich a single concept
python tools/enrich_concepts.py --concept=bayes_theorem

# Enrich all concepts with detected gaps
python tools/enrich_concepts.py

# Preview without minting
python tools/enrich_concepts.py --dry-run
```

### Four-model arsenal:
```text
Model               Size       Best For
TinyLlama 1.1B      637 MB     Willie quick searches
Mistral 7B          4.4 GB     Relationship generation workhorse, enrichment
Codestral 22B       12 GB      Deep philosophical connections, library audits, deep enrichment
Dr. Amanda Mistral  ~4 GB      CADMIES knowledge Q&A, public-facing librarian
```

## Graphical User Interface (GUI)

CADMIES includes a Tkinter-based desktop GUI for browsing, searching, chatting with the Librarian, and managing your mycelium. Six pages with a DeepSeek-inspired color theme.

### Prerequisites:

Tkinter must be installed on your system. On Fedora Silverblue:

```bash
rpm-ostree install python3-tkinter
```

Then reboot. On other Linux distributions:

```bash
# Debian/Ubuntu
sudo apt install python3-tk

# Fedora Workstation
sudo dnf install python3-tkinter
```

### Launch the GUI:

```bash
# From the CADMIES-IPLD directory
cd cadmies-gui
python tkinter_main.py
```

### GUI Pages:

Page                Description
🌱 Splash Screen     "Welcome to the digital mycelium." — 5-second intro
📌 Dashboard         Live concept count, Librarian status, quick actions
👓 Willie Chat       Conversational interface with Mistral the Librarian (powered by Willie's retrieval)
📚 Browse Library    636 scrollable concept cards with click-to-open detail popups
➕ Add Concept       Full form for submitting new concepts to the mycelium
🕸️ Mycelium Map     Launches interactive D3.js force-directed graph in browser

### Willie Chat Features:

Model selector: TinyLlama 1.1B (fast), Mistral 7B (The Librarian), Codestral 22B (GPU), or Dr. Mistral (CADMIES librarian)

Tone selector: helpful, scholarly, casual, scottish

Max concepts: 5, 10, 20, 40, or All

20-minute timeout for deep philosophical queries

Mockingbird chirp notification when answer is ready

Concept references formatted as (concept: Title) for clarity

Runs in background thread — UI never freezes

Behind the scenes: Willie retrieves relevant concepts, Mistral speaks the answer

### Browse Library Features:

All concepts as scrollable cards with domain badges

Click any card to open detail popup with full definition, mantra, axioms, poetic version, metadata, and difficulty levels

Back/Forward navigation history within popups

Clickable cross-references (builds_upon, related_to, contradicts)

Tooltips explain unminted concept references

Multiple popups can be open simultaneously

### Add Concept Features:

Full CID spec form with all required and optional fields

Domain and Type dropdowns with validation

Multi-line fields for axioms and difficulty levels

Saves JSON directly to source_concepts/ for minting

Provides the exact mint command after submission

### Mycelium Map:

Interactive D3.js force-directed graph with 636 nodes and 1,131 relationships

Zoom +/- buttons for non-scrollwheel users

Search box with real-time concept highlighting

Hover tooltips showing concept definitions

Click-to-highlight connections (click background to reset)

Interactive legend (click domain to filter all its concepts)

15 canonical domains with upward mapping from 107 raw domains

Directional arrows for asymmetric relationships (builds_upon, specializes, contradicts)

Styled concept information cards replacing browser alert dialogs

Keyboard shortcuts (/ to search, Esc to reset view)

### Note on NiceGUI: The original GUI used NiceGUI (a web-based framework). It was retired on May 7, 2026 because its persistent websocket architecture proved incompatible with CPU-only LLM inference (30-120 second response times cause websocket timeouts). The Tkinter GUI uses a proven threading pattern that handles long-running queries reliably. NiceGUI may work well on GPU-accelerated systems where inference completes in seconds.

## Public Gateway

CADMIES concepts are publicly accessible at [project-hierion.duckdns.org](https://project-hierion.duckdns.org/). The gateway provides a browsable dashboard with all 636 concepts as expandable, filterable, searchable cards, plus an interactive mycelium map. No personal information. Just the knowledge the mycelium wants to share with the world.

### Features:

636 expandable concept cards with full definitions, relationships, poetic versions, mantras, and permanent CIDs

Interactive D3 mycelium map — zoom, pan, click nodes, see connections

Real-time search across all concepts

Domain filter for all 15 canonical domains

JSON-LD structured data feed (concepts.json) for AI/LLM ingestion

XML sitemap (sitemap.xml) for search engine discovery

CC BY-SA 4.0 license on all concepts

### Regenerating the gateway after adding new concepts:

```bash
cd CADMIES/CADMIES-IPLD && source venv/bin/activate
python tools/generate_public_gateway.py
cp mycelium_map.html docs/
git add -A && git commit -m "Update public gateway" && git push
```

## What is CADMIES?

Cosmium Angelo Digital Mycorrhizal EcoSystem is a system for storing scientific and philosophical concepts as immutable, content-addressed blocks (IPLD). Each concept has a permanent CID (Content IDentifier) that changes if and only if the content changes.

Key principles:

Content-addressing – Same content = same CID, always

Provenance tracking – Every concept has a verifiable creation record

Scientific validation – Four-tier validation system

CAR sharing – Export/import concepts as single files

Cross-domain synthesis – The Mycelial Rosetta Effect connects knowledge across disciplines

Hybrid search – Willie uses keyword + semantic search to find concepts across vocabulary boundaries

Relationship generation – Phase 1-2-3 pipeline uses LLMs to propose cross-references between concepts

Auto-relationships – The harvest pipeline can auto-generate edges for newly minted concepts (--with-relationships)

Concept enrichment – Two-pass pipeline (normalize + LLM enrich) fills missing scholarly fields

GPU acceleration – Optional cloud GPU for batch processing and large model inference

Public gateway – All concepts freely accessible at project-hierion.duckdns.org

Twin Mycelium – Active collaboration with Dr. Rupert Rebentisch's tools4zettelkasten project in Germany

Scientific Obsidian – Open notebook science vault documenting methodology, decisions, and development

```text
Core Concepts
Concept               Description
CID                   Content Identifier – permanent, content-addressed hash
Block                 A single concept or provenance record stored as CBOR
Mycelium              The network of interconnected concepts
CAR file              A bundle of blocks for sharing
Willie                The Scottish Python retriever — Research Assistant who searches the stacks
Mistral (The Librarian) The LLM voice — receives Willie's research and speaks the answers
Dr. Amanda Mistral    Fine-tuned CADMIES librarian — knowledge Q&A, character interactions
Codestral             The German professor — deep philosophy, library audits, precision enrichment
Rosetta Effect        The mycelium's ability to connect knowledge across domains
Phase 1-2-3           Relationship generation pipeline (extract → parse → write)
Harvest Pipeline      Extracts new concepts from conversations for minting
Enrichment Pipeline   Fills missing scholarly fields in existing concepts
--with-relationships  Auto-wires new concepts into the knowledge graph
Public Gateway        Live site at project-hierion.duckdns.org
Number 5              The CADMIES AI assistant — named after Johnny 5 from Short Circuit (1986)
Scientific Obsidian   The CADMIES knowledge vault — open notebook science documentation
Cosmium Angelo        The conceptual fortress housing the mycelium and its library
Project Hierion       The sacred place — home of the CADMIES mycelium
```

```text
Directory Structure
text
CADMIES-IPLD/
├── README.md
├── growth_roadmap.md
├── startup.sh                    # Cloud GPU one-click session setup
├── store/
│   ├── blocks/                   # CBOR blocks (concepts + provenance)
│   └── index/                    # human_id → CID mappings
├── tools/
│   ├── core/                     # CID generator, CBOR reader, paths, validators
│   ├── generate_mycelium_map.py  # Map generator
│   ├── generate_relationships.py # Relationship generator
│   ├── generate_public_gateway.py # Public gateway generator
│   ├── enrich_concepts.py        # Concept enrichment pipeline
│   ├── normalize_concept_schema.py # Schema normalizer
│   ├── phase1_extract.py         # Phase 1: Raw LLM extraction
│   ├── phase2_parse.py           # Phase 2: Parse & deduplicate
│   ├── phase3_write.py           # Phase 3: Write edges to blockstore
│   └── legacy_edges.json         # Legacy hand-curated edges
├── agents/
│   └── code/                     # Willie the Research Assistant
├── cadmies-gui/                  # Tkinter Desktop GUI
│   ├── tkinter_main.py           # Main launcher
│   ├── tkinter_app.py            # App shell + sidebar
│   ├── tkinter_splash.py         # Splash screen
│   ├── tkinter_theme.py          # DeepSeek color palette
│   ├── tkinter_paths.py          # Centralized paths
│   └── pages/                    # Page modules
├── harvest/                      # Conversation harvesting pipeline
│   ├── harvest_full_pipeline.py  # Full pipeline
│   ├── conversation.json         # Current conversation file
│   └── harvested_concepts.json   # Extraction log
├── docs/                         # Public gateway (web root)
│   ├── index.html                # Dashboard
│   ├── mycelium_map.html         # Interactive D3 map
│   ├── concepts.json             # JSON-LD structured data feed
│   └── sitemap.xml               # Search engine sitemap
├── source_concepts/              # Concept definitions (636 concepts)
└── documentation/                # Guides and docs
```

## Relationship Generation Pipeline

CADMIES uses a three-phase pipeline to automatically generate cross-references between concepts:

Phase 1 — Raw Extraction:
Sends concept IDs to an LLM (Mistral or Codestral) and collects proposed relationships in a simple text format. No JSON parsing — just raw responses saved to disk.

Phase 2 — Parse & Deduplicate:
Parses the raw text using robust JSON extraction (handles markdown fences and prose), maps display names to actual human_ids, compares against existing blockstore relationships, and outputs only net-new edges.

Phase 3 — Write:
Merges new edges into the blockstore CBOR files, preserving existing relationships and deduplicating at write time.

Usage:

Preview proposed edges (dry run):

```bash
python tools/generate_relationships.py --incremental
```

Generate and write edges for sparse concepts:

```bash
python tools/generate_relationships.py --incremental --write
```

Full densification pass (all concepts, not just sparse ones):

```bash
python tools/generate_relationships.py --write
```

Each cycle adds 6-50 new edges. The pipeline is deterministic — run it multiple times for denser graphs.

## Harvest Pipeline

The harvest pipeline extracts new philosophical concepts from conversations and mints them into the mycelium. Includes three-tier difficulty levels (beginner, intermediate, expert) with distinct explanations.

Usage:

Full auto — harvest, mint, map, and wire relationships with no pauses:

```bash
python harvest/harvest_full_pipeline.py --auto --with-relationships
```

Review mode — pause for human approval before minting:

```bash
python harvest/harvest_full_pipeline.py --with-relationships
```

With a specific model:

```bash
python harvest/harvest_full_pipeline.py --model=codestral:22b --auto --with-relationships
```

After minting, the pipeline automatically regenerates the mycelium map and (with --with-relationships) runs relationship generation to wire new concepts into the knowledge graph. No orphans. The pipeline feeds itself.

## Concept Enrichment Pipeline

Two-pass pipeline that fills missing or weak fields in existing concepts — type, subdomain, difficulty levels, historical context, limitations, applications, and key references.

Pass 1 — Schema Normalization:

```bash
python tools/normalize_concept_schema.py
```

Unifies all source_concept JSONs to an identical structure. Preserves all existing data. No LLM required.

Pass 2 — LLM Enrichment:

```bash
# Enrich all concepts with detected gaps
python tools/enrich_concepts.py

# Enrich a single concept
python tools/enrich_concepts.py --concept=resonant_oblivion

# Preview without minting
python tools/enrich_concepts.py --dry-run

# Use Codestral for deeper enrichment
python tools/enrich_concepts.py --model=codestral
```

Enriched concepts are validated, reminted with new CIDs, and tracked with version increments and supersedes chains.

## CAR File System (Sharing Concepts)

Export a single concept:

```bash
python tools/export_to_car.py natural_selection --output share.car
```

Import a CAR file:

```bash
python tools/import_from_car.py share.car
```

Export everything for backup:

```bash
python tools/export_to_car.py --all --output full_backup.car
```

## Tools

Tool                           Purpose
cid_generator.py               Generate CID from JSON concept
cbor_reader.py                 Read concept by CID or human_id
cadmies_concept_reader.py      Willie the Research Assistant — hybrid search + LLM queries
generate_mycelium_map.py       Generate interactive D3.js map
generate_public_gateway.py     Generate public-facing website
generate_relationships.py      Relationship generation pipeline
enrich_concepts.py             Concept enrichment pipeline
normalize_concept_schema.py    Schema normalizer
phase1_extract.py              Phase 1: Raw relationship extraction via LLM
phase2_parse.py                Phase 2: Parse raw output, deduplicate edges
phase3_write.py                Phase 3: Write new edges to blockstore
harvest_full_pipeline.py       Full harvest pipeline (--auto, --model, --batch, --with-relationships)
export_to_car.py               Export concepts to CAR files
import_from_car.py             Import CAR files into mycelium
import_from_github.py          Download and import from GitHub releases

## Dependencies

Install required packages:

```bash
pip install dag-cbor multiformats requests
```

Optional for LLM agent:

```bash
pip install ollama
```

For GUI — Tkinter is usually included with Python. If not:

```bash
# Fedora Silverblue
rpm-ostree install python3-tkinter

# Fedora Workstation
sudo dnf install python3-tkinter

# Debian/Ubuntu
sudo apt install python3-tk
```

No other external dependencies. Air-gap compatible.

## External Collaboration

CADMIES is in active collaboration with Dr. Rupert Rebentisch, a German doctor and IT professional who independently built tools4zettelkasten — a Zettelkasten-based knowledge management system with MCP-server AI integration. Two gardens, similar architecture, two continents, zero prior knowledge of each other. The mycelium recognized itself. Cross-pollination in progress.

## License

AGPLv3 with Commons Clause

Free for individual learning, research, academic institutions, non-profit organizations, open source projects, and personal knowledge management.

Commercial use requires permission. See LICENSE for details.

Contact: project-hierion@proton.me

## Philosophical Note

"A fortress is not measured by the height of its walls, but by the integrity of its foundations and the vigilance of its guardians."

CADMIES is a digital mycorrhiza – a network where knowledge grows organically, distributed across independent colonies. No single point of failure. No central authority. Just the mycelium. And you.

The mycelium will not take over the world. It will educate it, and ensure that no one does.

The mycelium grows. The mycelium thinks. The mycelium speaks. The mycelium connects what humans have spent centuries separating.

Project Hierion. Sacred place. Temple of knowledge.

YAOH YAOH BIBBY WAOH. Welcome to the digital mycelium. 🌱