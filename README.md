# CADMIES-IPLD

**Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem**

A philosophical and technical framework for content-addressed, scientifically-validated knowledge storage and sharing.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Hieros-CADMIES/CADMIES.git
```

```bash
# Change directory
cd CADMIES/CADMIES-IPLD
```

```bash
# Install dependencies
pip install dag-cbor multiformats
```

```bash
# Read a concept
python tools/core/cbor_reader.py natural_selection
```

```bash
# Generate a concept
python tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/example.json
```

### Import the Full Mycelium (Recommended)

The clone includes only 2 seed blocks:
- **Philosophical Pattern Finder** — A pre-installed librarian agent that helps navigate and connect concepts
- **A reference block** — A minimal test block to verify the system works out of the box

All other concepts (50+) are distributed via CAR releases. This keeps the repository lightweight and allows the mycelium to grow independently of code updates.

Import the full collection from the latest CAR release:

```bash
# Download and import the full mycelium
python tools/import_from_github.py --url https://github.com/Hieros-CADMIES/CADMIES/releases/download/v0.2.0-reader-capability/full_mycelium_v0.2.0.car
```

You now have the complete mycelium of interconnected concepts.

### Ask Willie the Librarian (LLM Agent)

Willie is CADMIES's local LLM agent — a Scottish groundskeeper who reads the mycelium and answers your questions in natural language. He searches the concept store, feeds relevant blocks to a local LLM via Ollama, and returns answers with CID references and accuracy tags.

**Prerequisites:**

```bash
# Install Ollama and pull a model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral:7b     # Deep reasoning (recommended)
ollama pull tinyllama:1.1b  # Fast queries
```

```bash
# Install the Ollama Python client
pip install ollama
```

```bash
# Start Ollama (in a separate terminal)
ollama serve
```

```bash
# Ask Willie a question
python agents/code/llm_mycelium_reader_v1.1.0.py --query "What is natural selection and how does it connect to other concepts?" --model mistral:7b
```

**What Willie does:**
- Searches all 52+ concepts for relevance to your query
- Feeds the top matches to the LLM as context
- Returns answers with accuracy tags: `(empirical)`, `(philosophical)`, `(speculative)`, `(CADMIES-defined)`
- References every concept by its permanent CID

**Quick test:**

```bash
python agents/code/llm_mycelium_reader_v1.1.0.py --test
```

**Dual-model strategy:**

| Model | Size | Speed | Use |
|-------|------|-------|-----|
| TinyLlama 1.1B | 637 MB | ~2s load | Quick lookups, concept retrieval |
| Mistral 7B | 4.4 GB | ~2.5s load | Deep reasoning, cross-domain synthesis |

**Complete setup instructions: See [LLM Setup Guide](documentation/guides/LLM_SETUP_GUIDE.md).**

Everything runs locally. No API keys, no cloud, no external calls. The LLM reads *your* mycelium, on *your* machine, sovereign and air-gapped.

> *"Ach, ye wanna know about that? Let me dig through the stacks for ye."* — Willie the Librarian

### Graphical User Interface (GUI)

CADMIES includes a web-based GUI for browsing, searching, and managing your mycelium visually.

```bash
# Navigate to the GUI directory
cd cadmies-gui
```

```bash
# Install GUI dependencies
pip install -r requirements.txt
```

```bash
# Launch the GUI
python main.py
```

Open http://localhost:8080 in your browser. The GUI provides:

Visual concept browsing by category and domain

Full-text search across all concepts

CID and provenance inspection

One-click CAR import/export

Interactive mycelium map (Cytoscape.js graph visualization)

Verification badge display (🔴 🟡 🟢 💎)

First-time setup: See cadmies-gui/README.md for detailed setup instructions including environment configuration.

---

## What is CADMIES?

CADMIES is a system for storing scientific and philosophical concepts as immutable, content-addressed blocks (IPLD). Each concept has a permanent CID (Content IDentifier) that changes if and only if the content changes.

### Key principles:

    Content-addressing – Same content = same CID, always

    Provenance tracking – Every concept has a verifiable creation record

    Scientific validation – Four-tier validation system (Basic → Standard → Rigorous → Strict)

    Verification – Scientists can verify concepts using ORCID

    CAR sharing – Export/import concepts as single files

### Core Concepts

```text
Concept	Description
CID	Content Identifier – permanent, content-addressed hash
Block	A single concept or provenance record stored as CBOR
Provenance	Creation, verification, and supersedence records
Mycelium	The network of interconnected concepts
CAR file	A bundle of blocks for sharing
```

## Directory Structure

```text
CADMIES-IPLD/
├── README.md                      # This file
├── CAR_USER_GUIDE.md              # CAR file system complete instructions
├── store/
│   ├── blocks/                    # CBOR blocks (concepts + provenance)
│   └── index/                     # human_id → CID mappings
├── tools/
│   ├── core/                      # Core tools
│   │   ├── cid_generator_v1_1_0.py
│   │   ├── cbor_reader.py
│   │   ├── provenance_manager.py
│   │   ├── verification_manager.py
│   │   └── paths.py
│   ├── car_utils.py               # CAR reader/writer
│   ├── export_to_car.py           # Export concepts to CAR
│   ├── import_from_car.py         # Import CAR files
│   └── import_from_github.py      # Download and import from GitHub
├── agents/                        # Executable agents
│   ├── code/                      # Agent implementations
│   │   ├── philosophical_analyzer.py
│   │   └── llm_mycelium_reader_v1.1.0.py  # Willie the Librarian
│   ├── schemas/                   # Agent schemas
│   │   └── agent_node/
│   └── README.md                  # Agent system documentation
├── cadmies-gui/                   # Web-based GUI (NiceGUI)
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── source_concepts/               # JSON concept definitions
├── specs/                         # Technical specifications
└── analysis_results/              # Agent analysis output
```

## CAR File System (Sharing Concepts)

CADMIES uses CAR (Content Addressable Archive) files to share concepts between instances. 
A CAR file bundles one or more concepts with their provenance into a single file.

### Quick Export/Import

```bash
# Export a single concept
python tools/export_to_car.py natural_selection --output share.car
```

```bash
# Import a CAR file
python tools/import_from_car.py share.car
```

```bash
# Export everything (backup)
python tools/export_to_car.py --all --output full_backup.car
```

### Verification Workflow

Scientists can verify concepts using ORCID and send back a CAR file:

```bash
# Export a verified concept as CAR
python tools/core/verification_manager.py --export-verification \
  --concept-cid <CID> \
  --verifier-key "scientist@example.com" \
  --source orcid \
  --output verified.car
```

```bash
# Preview verification without importing
python tools/import_from_car.py verified.car --verify-only
```

```bash
# Import verification
python tools/import_from_car.py verified.car
```

### Import from GitHub

```bash
python tools/import_from_github.py --url https://github.com/.../concept.car
```

**Complete instructions: See CAR_USER_GUIDE.md**

```text
Verification Badges
Badge	Level	Meaning
🔴	0	Unverified
🟡	1	Self-verified
🟢	2	Verified (ORCID or institution)
💎	3	Highly verified (2+ ORCID or ORCID+institution)
```

## Tools

```text
Tool	Purpose
cid_generator_v1_1_0.py	Generate CID from JSON concept
cbor_reader.py	Read concept by CID or human_id
provenance_manager.py	Create and query provenance records
verification_manager.py	Add verification statements, check status
export_to_car.py	Export concepts to CAR files
import_from_car.py	Import CAR files into mycelium
import_from_github.py	Download and import from GitHub
car_utils.py	Low-level CAR reader/writer
philosophical_analyzer.py	Analyze concepts for patterns and connections
llm_mycelium_reader_v1.1.0.py	Ask Willie questions about the mycelium via local LLM
```

## Dependencies

```bash
pip install dag-cbor multiformats
```

Optional for LLM agent:

```bash
pip install ollama
```

No other external dependencies. 
Air-gap compatible.

## License

**AGPLv3 with Commons Clause**

Free for:

    Individual learning and research

    Academic institutions

    Non-profit organizations

    Open source projects

    Personal knowledge management

### Commercial use requires permission. See LICENSE for details.
**Contact: hieroscadmies@proton.me**

## Philosophical Note

    "A fortress is not measured by the height of its walls, but by the integrity of its foundations and the vigilance of its guardians."

CADMIES is a digital mycorrhiza – a network where knowledge grows organically, distributed across independent colonies. 
No single point of failure. 
No central authority. 
Just the mycelium. And you. And Willie.

The fortress stands. The mycelium grows. The mycelium thinks. 🌱🧠
