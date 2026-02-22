# CADMIES - IPLD Knowledge Tools

**Content-Addressed Systems for Educational Knowledge Management**
![License](https://img.shields.io/badge/license-AGPLv3%20with%20Commons%20Clause-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-orange.svg)

## Overview

CADMIES (Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem) is a decentralized knowledge system using IPLD/DAG-CBOR for storing verifiable concepts with content-addressed identifiers (CIDs). Think of it as mycelium for knowledge — structured, interconnected, and resilient.

Core Principles:
- **Deterministic addressing** — Same content → Same CID → Same understanding
- **Local-first** — Air-gapped by default, network optional
- **Schema-enforced** — All concepts validate against UniversalScientificConcept schema
- **Privacy by design** — Directory-level visibility control
- **Ethical knowledge sharing** — AGPLv3 with Commons Clause

## Repository Structure

This repo contains **two parallel systems**:

### `/testable_system/`
**The sanitized demo version** - Perfect for:
- Beginners learning content-addressed systems
- Educators running classroom demonstrations
- Quick testing without setup complexity
- Exploring the IPLD knowledge concept structure

👉 Start here if you're new to CADMIES.

### 🧠 `/CADMIES-IPLD/`
**The complete production system** - For:
- Advanced users running their own knowledge base
- Researchers working with metaphysical concepts
- Developers extending the platform
- Full read/write cycle with actual stored concepts
- Agent runtime and schema extensions
- DNA/genomics experimental data

👉 Dive here when you're ready for the real thing.

## Features

- **CID Generator** — Create deterministic CIDs from structured JSON concepts
- **CBOR Reader** — Retrieve concepts by CID or human-readable ID
- **Universal Schema** — Standardized representation for scientific/philosophical concepts
- **AgentNode Schema** — Extend concepts with executable agent capabilities
- **Scientific Validator** — Quality control before storage
- **IPLD Compatible** — Full DAG-CBOR support
- **Test Suite** — Determinism verification and validation tools
- **Atlas Network Ready** — Optional integration with decentralized discovery

## Graphical Interface

CADMIES includes a web-based GUI for easier interaction:

- **Dashboard** – System overview and recent activity
- **Add Concept** – Form interface with live preview
- **Browse Library** – Search and view existing concepts
- **Audit Trail** – Complete operation history

**[GUI Documentation](./cadmies-gui/README.md)**

100% local, air-gapped by default, same ethical licensing.

## Quick Start

### Prerequisites
```bash
# Install Python packages
pip install dag-cbor multiformats

Clone and Test (Demo Version)
bash

git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES/testable_system

bash

# Generate your first concept
python cid_generator_v1.1.0.py

# Retrieve it (use the CID from previous step)
python cbor_reader.py bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji

# List all stored concepts
python cbor_reader.py --list

Beginner's Guide

New to content-addressed systems? We've got you covered.
Step-by-Step Tutorial

    Open your terminal/command line

        Windows: Press Windows Key → type cmd → Enter

        Mac: Press Command + Space → type Terminal → Enter

        Linux: Press Ctrl + Alt + T

    Check Python installation
    bash

    python --version

    You should see Python 3.8 or higher.

    Install required packages
    bash

    pip install dag-cbor multiformats

    Clone this repository
    bash

    git clone https://github.com/Hieros-CADMIES/CADMIES.git
    cd CADMIES/testable_system

    Run your first CID generation
    bash

    python cid_generator_v1.1.0.py

    Look for: 🎯 Generated CID: bafy...

    Retrieve the concept
    bash

    python cbor_reader.py [THE_CID_YOU_COPIED]

    Verify determinism (run step 5 again—same CID appears!)

Congratulations! You've just used a content-addressed knowledge system.
Project Structure
text

CADMIES/
├── cadmies-gui/                    # Web interface (works with both systems)
├── testable_system/                 # Sanitized demo version
│   ├── cadmies_demo/               # Core tools package
│   ├── docs/                        # User documentation
│   ├── examples/                    # Example concepts
│   ├── schemas/                     # JSON schemas
│   ├── specs/                       # Formal specifications
│   └── tests/                       # Test suite
├── CADMIES-IPLD/                    # Complete production system
│   ├── agents_workspace/            # Agent schemas and implementations
│   ├── archive/                      # Versioned tool history
│   ├── audits/                       # Scientific audit system
│   ├── documentation/                 # Complete documentation suite
│   ├── experiments/                   # DNA/genomics experimental data
│   ├── genome_lab/                    # Sequencing workflow
│   ├── runtime/                       # Agent runtime (Phase 3)
│   ├── scientific_continuity/         # Peer-review system
│   ├── store/                         # Authoritative IPLD data
│   ├── tests/                         # Test files
│   └── tools/                         # Authoritative toolset
│       └── core/                       # Production tools
├── [root files]                      # PDFs, licenses, README, etc.
└── README.md                          # This file

Documentation
Document	Location	Description
Universal Scientific Concept Schema	/schemas/	JSON schema for concepts
AgentNode Schema	/CADMIES-IPLD/agents_workspace/schemas/agent_node/	Executable agent specification
CID Structure Specification	/specs/	Human-readable ID format
User Guide	/testable_system/docs/	Getting started guide
Technical Documentation	/CADMIES-IPLD/documentation/	Complete system documentation
Testing
Test the Demo System
bash

cd testable_system
python tests/test_determinism.py
python tests/test_core_functionality.py
python tests/test_read_write_cycle.py

Test the Production System
bash

cd CADMIES-IPLD
python audits/scientific_audit.py
python tests/test_autonomous_mining.py

⚖️ License & Ethical Use
License

AGPLv3 with Commons Clause - See LICENSE
Permitted Uses

    ✅ Individual learning and research

    ✅ Academic institutions and non-profits

    ✅ Open source projects

    ✅ Personal knowledge management

Restricted Uses (Commons Clause)

    ❌ Commercial SaaS offerings without contributing back

    ❌ Proprietary AI training without reciprocity

    ❌ Commercial products that don't share improvements

For commercial licensing: Contact hieroscadmies@proton.me
Contributing

This project welcomes educational and research-focused contributions. Please ensure all contributions align with the project's ethical framework and licensing terms.

We welcome contributions that align with our ethical framework:

    Knowledge sharing over commercial exploitation

    Reciprocity — If you use it commercially, contribute back

    Privacy preservation — No data leaks, no tracking

    Educational focus — Learning and research first

See our Contributing Guidelines and Code of Conduct.
Related Resources

    IPLD Documentation: https://ipld.io/

    DAG-CBOR Specification: https://ipld.io/specs/codecs/dag-cbor/

    CID Explanation: https://docs.ipfs.tech/concepts/content-addressing/

    Schema.org — Structured data standards

Contact

    Email: hieroscadmies@proton.me

    GitHub Issues: For bugs and feature requests

    Discussions: Join the conversation

🌱 Philosophy

"You can put the tools for doing these things in people's hands, and you can show them how to use these tools. But whether they will use those tools for genius is quite unpredictable" - Alan Watts

Let the mycelium grow! 🌱
