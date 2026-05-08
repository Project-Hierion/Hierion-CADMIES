# CADMIES-IPLD

**Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem**

A philosophical and technical framework for content-addressed, scientifically-validated knowledge storage and sharing. 91 interconnected concepts. One digital mycelium. Infinite connections.

---

## Quick Start

backtickbash
# Clone the repository
git clone https://github.com/Hieros-CADMIES/CADMIES.git
backtick

backtickbash
# Change directory
cd CADMIES/CADMIES-IPLD
backtick

backtickbash
# Install dependencies
pip install dag-cbor multiformats requests
backtick

backtickbash
# Read a concept
python tools/core/cbor_reader.py natural_selection
backtick

backtickbash
# Generate a concept
python tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/example.json
backtick

### Import the Full Mycelium (Recommended)

The clone includes only seed blocks. All other concepts (90+) are distributed via CAR releases. Import the full collection:

backtickbash
python tools/import_from_github.py --url https://github.com/Hieros-CADMIES/CADMIES/releases/download/v0.3.1/full_mycelium_v0.3.1.car
backtick

### Ask Willie the Librarian (LLM Agent)

Willie is CADMIES's local LLM agent — a Scottish groundskeeper who reads the mycelium and answers your questions in natural language using hybrid search (keyword + semantic query expansion via Mistral).

**Prerequisites:**

backtickbash
# Install Ollama and pull models
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral:7b      # Deep reasoning (recommended)
ollama pull tinyllama:1.1b   # Fast queries
backtick

backtickbash
# Install the Ollama Python client
pip install ollama
backtick

**Launch Ollama (Terminal 1 — keep running in background):**

backtickbash
# 24-hour keep-alive keeps the model warm for instant responses
OLLAMA_KEEP_ALIVE=24h ollama serve &
backtick

**Ask Willie (Terminal 2):**

backtickbash
cd CADMIES/CADMIES-IPLD && source venv/bin/activate
python agents/code/llm_mycelium_reader.py --query "What is natural selection?" --model mistral:7b
backtick

**What Willie does:**
- Searches all 90+ concepts using hybrid search (keyword + semantic)
- Feeds the top matches to the LLM as context
- Returns answers with accuracy tags: `(empirical)`, `(philosophical)`, `(speculative)`, `(CADMIES-defined)`
- References every concept by its permanent CID

**Dual-model strategy:**

| Model | Size | Speed | Use |
|-------|------|-------|-----|
| TinyLlama 1.1B | 637 MB | ~2s response | Quick lookups |
| Mistral 7B | 4.4 GB | ~30-120s response | Deep reasoning |

Everything runs locally. No API keys, no cloud, no external calls.

> *"Ach, ye wanna know about that? Let me dig through the stacks for ye."* — Willie the Librarian

---

### Graphical User Interface (GUI)

CADMIES includes a Tkinter-based desktop GUI for browsing, searching, chatting with Willie, and managing your mycelium. Five fully functional pages with a DeepSeek-inspired color theme.

**Prerequisites:**

Tkinter must be installed on your system. On Fedora Silverblue:

backtickbash
rpm-ostree install python3-tkinter
backtick

Then reboot. On other Linux distributions:

backtickbash
# Debian/Ubuntu
sudo apt install python3-tk

# Fedora Workstation
sudo dnf install python3-tkinter
backtick

**Launch the GUI:**

backtickbash
# From the CADMIES-IPLD directory
cd cadmies-gui
python tkinter_main.py
backtick

**GUI Pages:**

| Page | Description |
|------|-------------|
| 🌱 Splash Screen | "Welcome to the digital mycelium. Welcome to the Deep." — 5-second intro |
| 📌 Dashboard | Live concept count, Willie version, quick actions |
| 👓 Willie Chat | Full conversational interface with model/tone/max concept selectors |
| 📚 Browse Library | 91 scrollable concept cards with click-to-open detail popups |
| ➕ Add Concept | Full form for submitting new concepts to the mycelium |
| 🕸️ Mycelium Map | Launches interactive D3.js force-directed graph in Firefox |

**Willie Chat Features:**
- Model selector: TinyLlama 1.1B (fast) or Mistral 7B (deep)
- Tone selector: helpful, scholarly, casual, scottish
- Max concepts: 5, 10, 20, 40, or All
- 20-minute timeout for deep philosophical queries
- Mockingbird chirp notification when answer is ready
- Concept references formatted as `(concept: Title)` for clarity
- Runs in background thread — UI never freezes

**Browse Library Features:**
- All 91 concepts as scrollable cards with domain badges
- Click any card to open detail popup with full definition, mantra, axioms, poetic version, metadata, and difficulty levels
- Back/Forward navigation history within popups
- Clickable cross-references (builds_upon, related_to, contradicts)
- Tooltips explain unminted concept references
- Multiple popups can be open simultaneously

**Add Concept Features:**
- Full CID spec form with all required and optional fields
- Domain and Type dropdowns with validation
- Multi-line fields for axioms and difficulty levels
- Saves JSON directly to `source_concepts/` for minting
- Provides the exact mint command after submission

**Mycelium Map:**
- Interactive D3.js force-directed graph showing all concepts and their connections
- Drag nodes, zoom, hover for details, click to highlight connections
- Launches in Firefox (required for JavaScript visualization)

**Note on NiceGUI:** The original GUI used NiceGUI (a web-based framework). It was retired on May 7, 2026 because its persistent websocket architecture proved incompatible with CPU-only LLM inference (30-120 second response times cause websocket timeouts). The Tkinter GUI uses a proven threading pattern that handles long-running queries reliably. NiceGUI may work well on GPU-accelerated systems where inference completes in seconds.

---

## What is CADMIES?

CADMIES is a system for storing scientific and philosophical concepts as immutable, content-addressed blocks (IPLD). Each concept has a permanent CID (Content IDentifier) that changes if and only if the content changes.

### Key principles:

- **Content-addressing** – Same content = same CID, always
- **Provenance tracking** – Every concept has a verifiable creation record
- **Scientific validation** – Four-tier validation system
- **CAR sharing** – Export/import concepts as single files
- **Cross-domain synthesis** – The Mycelial Rosetta Effect connects knowledge across disciplines
- **Hybrid search** – Willie v1.2.1 uses keyword + semantic search to find concepts across vocabulary boundaries

### Core Concepts

| Concept | Description |
|---------|-------------|
| CID | Content Identifier – permanent, content-addressed hash |
| Block | A single concept or provenance record stored as CBOR |
| Mycelium | The network of interconnected concepts |
| CAR file | A bundle of blocks for sharing |
| Willie | The Scottish LLM librarian who reads the mycelium |
| Rosetta Effect | The mycelium's ability to connect knowledge across domains |

---

## Directory Structure

backticktext
CADMIES-IPLD/
├── README.md
├── store/
│   ├── blocks/                    # CBOR blocks (concepts + provenance)
│   └── index/                     # human_id → CID mappings
├── tools/
│   └── core/                      # CID generator, CBOR reader, paths
├── agents/
│   └── code/                      # Willie the Librarian (llm_mycelium_reader.py)
├── cadmies-gui/                   # Tkinter Desktop GUI
│   ├── tkinter_main.py            # Main launcher
│   ├── tkinter_app.py             # App shell + sidebar
│   ├── tkinter_splash.py          # Splash screen
│   ├── tkinter_theme.py           # DeepSeek color palette
│   ├── tkinter_paths.py           # Centralized paths
│   └── pages/                     # Page modules (dashboard, willie_chat, browse, add_concept, mycelium_map)
├── source_concepts/               # JSON concept definitions (91 concepts)
├── harvest/                       # Conversation harvesting tools
└── documentation/                 # Guides and docs
backtick

---

## CAR File System (Sharing Concepts)

backtickbash
# Export a single concept
python tools/export_to_car.py natural_selection --output share.car

# Import a CAR file
python tools/import_from_car.py share.car

# Export everything (backup)
python tools/export_to_car.py --all --output full_backup.car
backtick

---

## Tools

| Tool | Purpose |
|------|---------|
| cid_generator_v1_1_0.py | Generate CID from JSON concept |
| cbor_reader.py | Read concept by CID or human_id |
| llm_mycelium_reader.py | Willie the Librarian — hybrid search + LLM queries |
| extract_concepts.py | Harvest concepts from conversations |
| export_to_car.py | Export concepts to CAR files |
| import_from_car.py | Import CAR files into mycelium |
| import_from_github.py | Download and import from GitHub releases |

---

## Dependencies

backtickbash
pip install dag-cbor multiformats requests
backtick

Optional for LLM agent:

backtickbash
pip install ollama
backtick

For GUI:

backtickbash
# Tkinter is usually included with Python. If not:
# Fedora: rpm-ostree install python3-tkinter (or sudo dnf install python3-tkinter)
# Debian/Ubuntu: sudo apt install python3-tk
backtick

No other external dependencies. Air-gap compatible.

---

## License

**AGPLv3 with Commons Clause**

Free for individual learning, research, academic institutions, non-profit organizations, open source projects, and personal knowledge management.

Commercial use requires permission. See LICENSE for details.
**Contact: hieroscadmies@proton.me**

---

## Philosophical Note

> *"A fortress is not measured by the height of its walls, but by the integrity of its foundations and the vigilance of its guardians."*

CADMIES is a digital mycorrhiza – a network where knowledge grows organically, distributed across independent colonies. No single point of failure. No central authority. Just the mycelium. And you. And Willie. And the whale.

The fortress stands. The mycelium grows. The mycelium thinks. The mycelium connects what humans have spent centuries separating.

Welcome to the digital mycelium. 🌱 Welcome to the Deep. 🐋
