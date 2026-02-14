CADMIES - Content-Addressed Digital Mycorrhizal Intelligence EcoSystem

https://img.shields.io/badge/License-AGPLv3%2520with%2520Commons%2520Clause-blue.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/IPLD-DAG--CBOR-green.svg
https://img.shields.io/badge/Atlas-Compatible-orange.svg

🌿 Overview

CADMIES (Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem) is a decentralized knowledge system using IPLD/DAG-CBOR for storing verifiable concepts with content-addressed identifiers (CIDs). Think of it as mycelium for knowledge—structured, interconnected, and resilient.

Core Principles:

    Deterministic addressing — Same content → Same CID → Same understanding

    Local-first — Air-gapped by default, network optional

    Schema-enforced — All concepts validate against UniversalScientificConcept schema

    Privacy by design — Directory-level visibility control

    Ethical knowledge sharing — AGPLv3 with Commons Clause

✨ Features

    CID Generator — Create deterministic CIDs from structured JSON concepts

    CBOR Reader — Retrieve concepts by CID or human-readable ID

    Universal Schema — Standardized representation for scientific/philosophical concepts

    IPLD Compatible — Full DAG-CBOR support

    Test Suite — Determinism verification and validation tools

    Atlas Network Ready — Optional integration with decentralized discovery

🚀 Quick Start

Prerequisites

# Install Python packages
pip install dag-cbor multiformats

Clone and Test

git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES

# Generate your first concept
python cid_generator_v1.1.0.py

# Retrieve it (use the CID from previous step)
python cbor_reader.py bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji

# List all stored concepts
python cbor_reader.py --list

For complete beginners, see our Beginner's Guide section.

📚 Beginner's Guide

New to content-addressed systems? We've got you covered.

Step-by-Step Tutorial

    Open your terminal/command line

        Windows: Press Windows Key → type cmd → Enter

        Mac: Press Command + Space → type Terminal → Enter

        Linux: Press Ctrl + Alt + T

    Check Python installation

    python --version

    You should see Python 3.8 or higher.

    Install required packages

    pip install dag-cbor multiformats

    Clone this repository

    git clone https://github.com/Hieros-CADMIES/CADMIES.git
    cd CADMIES

    Run your first CID generation

    python cid_generator_v1.1.0.py

    Look for: 🎯 Generated CID: bafy...

    Retrieve the concept

    python cbor_reader.py [THE_CID_YOU_COPIED]

    Verify determinism (run step 5 again—same CID appears!)

Congratulations! You've just used a content-addressed knowledge system.

🌐 Atlas Network Integration

CADMIES nodes can optionally join the Atlas decentralized network, making public knowledge concepts discoverable and queryable by other peers worldwide.

Why Connect to Atlas?

    Discoverability — Your public concepts become searchable across the network

    Interoperability — Structured data that other applications can use

    No lock-in — Your node remains fully functional offline

    Privacy controlled — Only directories you explicitly mark as public are visible

Quick Start with Atlas

# Install additional dependencies
pip install -r atlas-integration/requirements.txt

# Configure which directories are visible
cp atlas-integration/config/visible_dirs.yaml.example atlas-integration/config/visible_dirs.yaml
# Edit visible_dirs.yaml to set your privacy preferences

# Generate node keys
python -c "from atlas_integration.auth.keys import generate_node_keys; generate_node_keys()"

# Start the Atlas-compatible API server
python atlas-integration/api/server.py

Your node will be available at http://localhost:8080 and will:

    Advertise CADMIES concepts to the Atlas network

    Respond to queries for public knowledge

    Keep private directories completely invisible

Privacy First

Directories not listed in visible_dirs.yaml are invisible to the network. Queries for private paths receive 404 Not Found with no hint they exist. Your data stays yours.

Test the Integration

# Run the full integration test
python test_cadmies_atlas_integration.py

See atlas-integration/README.md for complete documentation.

📁 Project Structure

CADMIES/
├── cid_generator_v1.1.0.py      # Create CIDs from concepts
├── cbor_reader.py                # Retrieve concepts by CID/ID
├── test_cadmies_atlas_integration.py  # Atlas integration test
├── blocks/                       # Stored DAG-CBOR concepts
├── index/                        # Human-readable ID mappings
├── logs/                         # Operation history
├── atlas-integration/            # Optional network layer
│   ├── README.md
│   ├── config/                   # Privacy settings
│   ├── auth/                      # Atlas authentication
│   ├── api/                        # REST endpoints
│   ├── adapters/                  # CADMIES wrapper
│   └── tests/                      # Integration tests
└── docs/                           # Additional documentation

📖 Documentation

Document	Description
Universal Scientific Concept Schema	JSON schema for concepts
CID Structure Specification	Human-readable ID format
Philosophical Framework	Design principles
Atlas Integration Guide	Network setup

🧪 Testing

# Test core functionality
python cid_generator_v1.1.0.py --educational-only
python cbor_reader.py --list --verbose

# Test Atlas integration
python atlas-integration/tests/test_auth.py
python atlas-integration/tests/test_api.py      # (server must be running)
python test_cadmies_atlas_integration.py

🤝 Contributing

We welcome contributions that align with our ethical framework:

    Knowledge sharing over commercial exploitation

    Reciprocity — If you use it commercially, contribute back

    Privacy preservation — No data leaks, no tracking

    Educational focus — Learning and research first

See our Contributing Guidelines and Code of Conduct.

License: AGPLv3 with Commons Clause — Free for educational, research, and non-profit use. Commercial use requires permission or contributing improvements back.

🔗 Related Projects

    Atlas Protocol — Decentralized discovery network

    IPLD — InterPlanetary Linked Data

    Schema.org — Structured data standards

📬 Contact

    Email: hieroscadmies@proton.me

    GitHub Issues: For bugs and feature requests

    Discussions: Join the conversation

🌱 Philosophy

    "We are not building containers for knowledge, but creating frameworks for understanding to grow."

CADMIES treats knowledge as living, connected, and evolving—like mycelium. It grows underground (local-first), fruits when conditions are right (optional network connectivity), and forms symbiotic relationships with other systems (Atlas integration).

The same understanding should always have the same address.
