# CADMIES - IPLD Knowledge Tools

**Content-Addressed Systems for Educational Knowledge Management**

![License](https://img.shields.io/badge/license-AGPLv3%20with%20Commons%20Clause-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
[![Codespaces](https://img.shields.io/badge/GitHub-Codespaces-181717?logo=github)](https://github.com/features/codespaces)

## Overview

CADMIES (Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem) is a decentralized knowledge system using IPLD/DAG-CBOR for storing verifiable concepts with content-addressed identifiers (CIDs). Think of it as mycelium for knowledge — structured, interconnected, and resilient.

**Core Principles:**
- **Deterministic addressing** — Same content → Same CID → Same understanding
- **Local-first** — Air-gapped by default, network optional
- **Schema-enforced** — All concepts validate against UniversalScientificConcept schema
- **Privacy by design** — Directory-level visibility control
- **Ethical knowledge sharing** — AGPLv3 with Commons Clause

## Understanding CIDs (Content Identifiers)

**How CIDs work:**
- Same content → Same hash → Same CID → Same understanding
- CIDs are deterministic across all users and systems
- Content includes: definition, equations, relationships, proofs
- Timestamps and authorship are stored separately (see Provenance)

**Why this matters:**
- You can verify someone else's concept by checking its CID
- No central authority needed to validate knowledge
- The system is trustless by design

## Provenance: The Story Behind the Knowledge

Every concept in CADMIES has two parts:

1. **The Concept Block** — Immutable knowledge (same CID for everyone)
2. **The Provenance Block** — Sticky note with timestamp + author

When you retrieve a concept, you automatically see both:
- What was claimed (the concept)
- Who claimed it and when (the provenance)

**Version History:** When a concept is updated, the new version includes a `supersedes` link to the old CID, preserving the complete evolution of knowledge.

This enables scientific verification, attribution, and trust without a central authority.

## Mycelium Map: Visual Knowledge Graph

CADMIES includes an interactive graph visualization of your knowledge ecosystem:

- **173+ nodes** — Every concept and its connections
- **160+ edges** — Builds upon, relates to, specializes, contradicts
- **Color-coded domains** — Physics, Philosophy, Biology, Mathematics
- **Click any node** — Reveals concept details
- **Type `cadmies`** — Hidden easter egg

The mycelium map helps you discover unexpected connections and see the shape of your knowledge.

## Repository Structure
```text
CADMIES/
├── CADMIES-IPLD/ # Main system directory
│ ├── agents/ # Agent implementations
│ ├── agents_workspace/ # Agent schemas and definitions
│ ├── audits/ # Scientific audit tools
│ ├── cadmies-gui/ # Web-based graphical interface
│ ├── documentation/ # Complete documentation suite
│ ├── experiments/ # Experimental data (DNA, genomics)
│ ├── genome_lab/ # Sequencing workflows
│ ├── runtime/ # Agent execution runtime
│ ├── schemas/ # JSON schemas for concepts
│ ├── scientific_continuity/ # Peer-review and methodology
│ ├── scripts/ # Utility scripts
│ ├── specs/ # Formal specifications
│ ├── store/ # IPLD block storage
│ │ ├── blocks/ # Content-addressed blocks
│ │ └── index/ # Human ID to CID mappings
│ └── tools/ # Core toolset
│   └── core/ # Production tools
├── LICENSE # AGPLv3 with Commons Clause
├── README.md # This file
└── [documentation PDFs] # Project narratives and manifests

Features

    CID Generator — Create deterministic CIDs from structured JSON concepts

    CBOR Reader — Retrieve concepts by CID or human-readable ID

    Universal Schema — Standardized representation for scientific/philosophical concepts

    Provenance Tracking — Automatic timestamp and author attribution (separate from concept CID)

    Version History — Supersedes links preserve knowledge evolution

    Mycelium Map — Interactive graph visualization of connected concepts

    AgentNode Schema — Extend concepts with executable agent capabilities

    Scientific Validator — Quality control before storage (4 validation levels)

    IPLD Compatible — Full DAG-CBOR support

Graphical Interface

CADMIES includes a web-based GUI with persistent sidebar navigation:

    Dashboard – System overview, statistics, recent activity, clickable easter egg

    Add Concept – Form interface with client-side live preview (air-gap compatible)

    Browse Library – Search and view existing concepts with provenance sticky notes

    Audit Trail – Complete operation history with timeline

    Mycelium Map – Interactive knowledge graph visualization

GUI Documentation

100% local, air-gapped by default, same ethical licensing.
Quick Start

Prerequisites
Install Python packages
bash

pip install dag-cbor multiformats

First-time users: Generate the initial knowledge store
bash

cd CADMIES-IPLD
python tools/core/cid_generator_v1_1_0.py

Launch the GUI
bash

cd CADMIES-IPLD/cadmies-gui
python gui_main.py

Then open http://localhost:8081 in your browser.

Generate Your First Concept via GUI

    Click "Add Concept" in the sidebar

    Fill in the form (name, type, domain, description)

    Preview updates as you click out of each field

    Click "Generate CID & Store"

Retrieve a Concept via CLI
Use the CID from the generation step
bash

python tools/core/cbor_reader.py bafyreicxfbddn4nsovtujy53envoo6cmmeszv6kk6ypigy7n7omfblnrda

Or use a human-readable ID
bash

python tools/core/cbor_reader.py conservation_of_energy

List All Stored Concepts
bash

python tools/core/cbor_reader.py --list

View the Mycelium Map
Click "Mycelium Map" in the GUI sidebar to explore your knowledge graph.
Beginner's Guide

New to content-addressed systems? Let's walk through it.

What's Happening Under the Hood?

    You provide content — A concept like "Energy cannot be created or destroyed"

    System serializes — Converts to DAG-CBOR format

    System hashes — Creates a SHA2-256 hash of the content

    System generates CID — Packages hash into a Content Identifier

    System stores — Saves block with the CID as its address

The magic: Same content → Same hash → Same CID → Same understanding
Step-by-Step Tutorial

    Open your terminal in the project directory

    Launch the GUI:

bash

cd CADMIES-IPLD/cadmies-gui
python gui_main.py

    Click "Add Concept" in the sidebar

    Enter a concept name: test_concept

    Select Type and Domain

    Add a description

    Click out of each field to see the live preview update

    Click "Generate CID & Store"

    Note the CID returned

    Click "Browse Library" to see your concept

Congratulations! You've just used a content-addressed knowledge system.
Testing

Test Core Functionality
bash

cd CADMIES-IPLD

Test CID determinism
bash

python tools/core/cid_generator_v1_1_0.py

Test retrieval
bash

python tools/core/cbor_reader.py --list

Test the GUI
bash

cd cadmies-gui
python gui_main.py

Expected Results

    All concepts generate deterministic CIDs

    Retrieved concepts match stored content exactly

    Provenance sticky notes appear with every concept

    Mycelium map shows all connections

    GUI sidebar persists across all pages

Documentation
Document	Location	Description
Universal Scientific Concept Schema	/CADMIES-IPLD/schemas/	JSON schema for concepts
CID Structure Specification v2.0.0	/CADMIES-IPLD/specs/	Human-readable ID format (snake_case)
User Guide	/CADMIES-IPLD/documentation/guides/	Getting started guide
Technical Documentation	/CADMIES-IPLD/documentation/	Complete system documentation
Development
GitHub Codespaces

This project is fully compatible with GitHub Codespaces. Launch a codespace and the environment is ready to go:

    Click Code → Codespaces → Create codespace on main

    Dependencies are pre-installed

    Run the system immediately

Running Locally
bash

git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES/CADMIES-IPLD
pip install dag-cbor multiformats nicegui pydantic python-dotenv aiofiles
python cadmies-gui/gui_main.py

License & Ethical Use
License

AGPLv3 with Commons Clause — See LICENSE file.

Permitted Uses:

    ✅ Individual learning and research

    ✅ Academic institutions and non-profits

    ✅ Open source projects

    ✅ Personal knowledge management

Restricted Uses (Commons Clause):

    ❌ Commercial SaaS offerings without contributing back

    ❌ Proprietary AI training without reciprocity

    ❌ Commercial products that don't share improvements

For commercial licensing: hieroscadmies@proton.me
Contributing

This project welcomes educational and research-focused contributions. Please ensure all contributions align with the project's ethical framework and licensing terms.

We welcome contributions that align with:

    Knowledge sharing over commercial exploitation

    Reciprocity — If you use it commercially, contribute back

    Privacy preservation — No data leaks, no tracking

    Educational focus — Learning and research first

Easter Eggs

CADMIES contains hidden surprises for the curious:

    Mycelium Map: Type cadmies anywhere to let the good times roll

    Dashboard: Click the 🌱 seedling next to "CADMIES Dashboard" for a bittersweet symphony

Discover them yourself. The mycelium rewards exploration.
Contact

    Email: hieroscadmies@proton.me

    GitHub Issues: For bugs and feature requests

    Discussions: Join the conversation

🌱 Philosophy

    "You can put the tools for doing these things in people's hands, and you can show them how to use these tools. But whether they will use those tools for genius is quite unpredictable"
    — Alan Watts

Let the mycelium grow! 🌱
