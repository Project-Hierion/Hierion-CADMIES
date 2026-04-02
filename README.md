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

## Repository Structure
```text
CADMIES/
├── CADMIES-IPLD/ # Main system directory
│ ├── agents/ # Agent implementations
│ │ └── code/ # Agent Python modules
│ ├── agents_workspace/ # Agent schemas and definitions
│ │ └── schemas/agent_node/ # AgentNode schema specifications
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
│ └── core/ # Production tools
├── LICENSE # AGPLv3 with Commons Clause
├── README.md # This file
└── [documentation PDFs] # Project narratives and manifests
```


## Features

- **CID Generator** — Create deterministic CIDs from structured JSON concepts
- **CBOR Reader** — Retrieve concepts by CID or human-readable ID
- **Universal Schema** — Standardized representation for scientific/philosophical concepts
- **AgentNode Schema** — Extend concepts with executable agent capabilities
- **Agent Executor** — Runtime for executing cognitive agents
- **Scientific Validator** — Quality control before storage (4 validation levels)
- **IPLD Compatible** — Full DAG-CBOR support
- **Robust Error Handling** — Graceful failure with informative logging

## Graphical Interface

CADMIES includes a web-based GUI for easier interaction:

- **Dashboard** – System overview and recent activity
- **Add Concept** – Form interface with live preview
- **Browse Library** – Search and view existing concepts
- **Audit Trail** – Complete operation history

**[GUI Documentation](./CADMIES-IPLD/cadmies-gui/README.md)**

100% local, air-gapped by default, same ethical licensing.

## Quick Start

### Prerequisites
Install Python packages
```bash
pip install dag-cbor multiformats
```

### Generate Your First Concept
Navigate to the system directory
```bash
cd CADMIES-IPLD
```

### Generate a concept (creates CID and stores it)
```bash
python tools/core/cid_generator_v1_1_0.py
```

### Retrieve a Concept
Use the CID from the generation step
```bash
python tools/core/cbor_reader.py bafyreicxfbddn4nsovtujy53envoo6cmmeszv6kk6ypigy7n7omfblnrda
```
Or use a human-readable ID
```bash
python tools/core/cbor_reader.py Physics:Law/ConservationOfEnergy
```
### List All Stored Concepts
```bash
python tools/core/cbor_reader.py --list
```

### Validate a Concept
Test the scientific validator
```bash
python tools/core/scientific_validator_v1.0.0.py
```

### Run an Agent
Test the agent executor with a philosophical analyzer
```bash
python runtime/runtime-minimal_agent_executor.py --test
```

## Beginner's Guide

New to content-addressed systems? Let's walk through it.
What's Happening Under the Hood?

    You provide content — A concept like "Energy cannot be created or destroyed"

    System serializes — Converts to DAG-CBOR format

    System hashes — Creates a SHA2-256 hash of the content

    System generates CID — Packages hash into a Content Identifier

    System stores — Saves block with the CID as its address

**The magic: Same content → Same hash → Same CID → Same understanding**

### Step-by-Step Tutorial

Open your terminal in the project directory
Generate a concept:
```bash
cd CADMIES-IPLD
```
```bash
python tools/core/cid_generator_v1_1_0.py
```

Look for: 🎯 Generated CID: bafy...

Retrieve it:
```bash
python tools/core/cbor_reader.py [THE_CID_YOU_COPIED]
```

Verify determinism: Run step 2 again — same CID appears!

**Congratulations!** You've just used a content-addressed knowledge system.

## Testing

Test Core Functionality
```bash
cd CADMIES-IPLD
```

### Test CID determinism
```bash
python tools/core/cid_generator_v1_1_0.py
```

### Test retrieval
```bash
python tools/core/cbor_reader.py --list
```

### Test scientific validation
```bash
python tools/core/scientific_validator_v1.0.0.py
```

### Test agent executor
```bash
python runtime/runtime-minimal_agent_executor.py --test
```

### Expected Results
```text
    All concepts generate deterministic CIDs

    Retrieved concepts match stored content exactly

    Scientific validator passes/fails appropriately

    Agent executor handles missing data gracefully
```

## Documentation
```text
Document:	Location	| Description
Universal Scientific Concept Schema:	/CADMIES-IPLD/schemas/	| JSON schema for concepts
AgentNode Schema:	/CADMIES-IPLD/agents_workspace/schemas/agent_node/	| Executable agent specification
CID Structure Specification:	/CADMIES-IPLD/specs/	| Human-readable ID format
User Guide:	/CADMIES-IPLD/documentation/guides/	| Getting started guide
Technical Documentation:	/CADMIES-IPLD/documentation/	| Complete system documentation
Development
GitHub Codespaces
```

***This project is fully compatible with GitHub Codespaces.*** **Launch a codespace and the environment is ready to go:**
```text
    Click Code → Codespaces → Create codespace on main

    Dependencies are pre-installed

    Run the system immediately
```

## Running Locally
```bash
git clone https://github.com/Hieros-CADMIES/CADMIES.git
```
```bash
cd CADMIES/CADMIES-IPLD
```
```bash
pip install dag-cbor multiformats
```
```bash
python tools/core/cid_generator_v1_1_0.py
```

## License & Ethical Use
### License

AGPLv3 with Commons Clause — See LICENSE

**Permitted Uses:**

    ✅ Individual learning and research

    ✅ Academic institutions and non-profits

    ✅ Open source projects

    ✅ Personal knowledge management

**Restricted Uses (Commons Clause):**

    ❌ Commercial SaaS offerings without contributing back

    ❌ Proprietary AI training without reciprocity

    ❌ Commercial products that don't share improvements

**For commercial licensing:** hieroscadmies@proton.me

**Contributing**

This project welcomes educational and research-focused contributions. Please ensure all contributions align with the project's ethical framework and licensing terms.

We welcome contributions that align with:

    Knowledge sharing over commercial exploitation

    Reciprocity — If you use it commercially, contribute back

    Privacy preservation — No data leaks, no tracking

    Educational focus — Learning and research first

See our Contributing Guidelines and Code of Conduct.

**Related Resources**

    IPLD Documentation

    DAG-CBOR Specification

    CID Explanation

    Schema.org — Structured data standards

**Contact**

    Email: hieroscadmies@proton.me

    GitHub Issues: For bugs and feature requests

    Discussions: Join the conversation

**🌱 Philosophy**

    "You can put the tools for doing these things in people's hands, and you can show them how to use these tools. But whether they will use those tools for genius is quite unpredictable" — Alan Watts

***Let the mycelium grow! 🌱***
