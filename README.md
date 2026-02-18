# IPLD Knowledge Tools

**Content-Addressed Systems for Educational Knowledge Management**
![License](https://img.shields.io/badge/license-AGPLv3%20with%20Commons%20Clause-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-orange.svg)

## Overview

CADMIES (Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem) is a decentralized knowledge system using IPLD/DAG-CBOR for storing verifiable concepts with content-addressed identifiers (CIDs). Think of it as mycelium for knowledge—structured, interconnected, and resilient.

Core Principles:
- **Deterministic addressing** — Same content → Same CID → Same understanding
- **Local-first** — Air-gapped by default, network optional
- **Schema-enforced** — All concepts validate against UniversalScientificConcept schema
- **Privacy by design** — Directory-level visibility control
- **Ethical knowledge sharing** — AGPLv3 with Commons Clause

## Features

- **CID Generator** — Create deterministic CIDs from structured JSON concepts
- **CBOR Reader** — Retrieve concepts by CID or human-readable ID
- **Universal Schema** — Standardized representation for scientific/philosophical concepts
- **IPLD Compatible** — Full DAG-CBOR support
- **Test Suite** — Determinism verification and validation tools
- **Atlas Network Ready** — Optional integration with decentralized discovery

## Graphical Interface

CADMIES now includes a web-based GUI for easier interaction:

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
```

### Clone and Test
```bash
git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES
```

# Generate your first concept
```bash
python cid_generator_v1.1.0.py
```

# Retrieve it (use the CID from previous step)
```bash
python cbor_reader.py bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji
```

# List all stored concepts
```bash
python cbor_reader.py --list
```

## Beginner's Guide

New to content-addressed systems? We've got you covered.

### Step-by-Step Tutorial
1. **Open your terminal/command line**
   -Windows: Press Windows Key → type cmd → Enter
   -Mac: Press Command + Space → type Terminal → Enter
   -Linux: Press Ctrl + Alt + T

2. **Check Python installation**
    ```bash
    python --version
    ```
    You should see Python 3.8 or higher.

3. **Install required packages**
   ```bash
   pip install dag-cbor multiformats
   ```

4. **Clone this repository**
   ```bash
   git clone https://github.com/Hieros-CADMIES/CADMIES.git
   cd CADMIES
   ```

5. **Run your first CID generation**
   ```bash
   python cid_generator_v1.1.0.py
   ```
   Look for: `🎯 Generated CID: bafy...`

6. **Retrieve the concept**
   ```bash
   python cbor_reader.py [THE_CID_YOU_COPIED]
   ```

7. **Verify determinism** (run step 5 again—same CID appears!)

Congratulations! You've just used a content-addressed knowledge system.

### 🌐 Atlas Network Integration

CADMIES nodes can optionally join the Atlas decentralized network, making public knowledge concepts discoverable and queryable by other peers worldwide.

### Why Connect to Atlas?

- **Discoverability** — Your public concepts become searchable across the network
- **Interoperability** — Structured data that other applications can use
- **No lock-in** — Your node remains fully functional offline
- **Privacy controlled** — Only directories you explicitly mark as public are visible

### Quick Start with Atlas
```bash

# Install additional dependencies
pip install -r atlas-integration/requirements.txt

# Configure which directories are visible
cp atlas-integration/config/visible_dirs.yaml.example atlas-integration/config/visible_dirs.yaml
# Edit visible_dirs.yaml to set your privacy preferences

# Generate node keys
python -c "from atlas_integration.auth.keys import generate_node_keys; generate_node_keys()"

# Start the Atlas-compatible API server
python atlas-integration/api/server.py
```

Your node will be available at http://localhost:8080 and will:

- Advertise CADMIES concepts to the Atlas network
- Respond to queries for public knowledge
- Keep private directories completely invisible

### Privacy First
Directories not listed in visible_dirs.yaml are invisible to the network. Queries for private paths receive 404 Not Found with no hint they exist. Your data stays yours.

### Test the Integration
```bash

# Run the full integration test
python test_cadmies_atlas_integration.py
```

See atlas-integration/README.md for complete documentation.

## Project Structure
```text
CADMIES/
├── cid_generator_v1.1.0.py      # Create CIDs from concepts
├── cbor_reader.py                # Retrieve concepts by CID/ID
├── test_cadmies_atlas_integration.py  # Atlas integration test
├── gui/                          # Web-based graphical interface
│   ├── README.md
│   ├── gui_main.py
│   ├── gui_system.py
│   ├── gui_concept.py
│   ├── gui_tools/
│   └── ui/
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
├── specs/                         # Formal specifications
│   └── cid_structure_specification_v1.0.1.md
├── schemas/                       # Knowledge schemas
│   └── universal_scientific_concept_schema_v1.0.0.json
└── docs/                           # Additional documentation
```

## Documentation
```text
| Document | Description |
|----------|-------------|
| Universal Scientific Concept Schema | JSON schema for concepts |
| CID Structure Specification | Human-readable ID format |
| Philosophical Framework | Design principles |
| Atlas Integration Guide | Network setup |
```

## Testing

```bash
# Test core functionality
python cid_generator_v1.1.0.py --educational-only
python cbor_reader.py --list --verbose
```

# Test Atlas integration
```bash
python atlas-integration/tests/test_auth.py
python atlas-integration/tests/test_api.py      # (server must be running)
python test_cadmies_atlas_integration.py
```

## ⚖️ License & Ethical Use

### License
AGPLv3 with Commons Clause - See [LICENSE](LICENSE)

### Permitted Uses
```text
- ✅ Individual learning and research
- ✅ Academic institutions and non-profits
- ✅ Open source projects
- ✅ Personal knowledge management
```

### Restricted Uses (Commons Clause)
```text
- ❌ Commercial SaaS offerings without contributing back
- ❌ Proprietary AI training without reciprocity
- ❌ Commercial products that don't share improvements
```

**For commercial licensing:** Contact hieroscadmies@proton.me

## Contributing

This project welcomes educational and research-focused contributions. Please ensure all contributions align with the project's ethical framework and licensing terms.

We welcome contributions that align with our ethical framework:

- **Knowledge sharing** over commercial exploitation
- **Reciprocity** — If you use it commercially, contribute back
- **Privacy preservation** — No data leaks, no tracking
- **Educational focus** — Learning and research first

See our Contributing Guidelines and Code of Conduct.

## Related Resources

- **IPLD Documentation**: https://ipld.io/
- **DAG-CBOR Specification**: https://ipld.io/specs/codecs/dag-cbor/
- **CID Explanation**: https://docs.ipfs.tech/concepts/content-addressing/
- **Atlas Protocol** — Decentralized discovery network
- **Schema.org** — Structured data standards

## Contact

- **Email**: hieroscadmies@proton.me
- **GitHub Issues**: For bugs and feature requests https://github.com/Hieros-CADMIES/CADMIES/
- **Discussions**: Join the conversation

## 🌱 Philosophy

*"You can put the tools for doing these things in people's hands, and you can show them how to use these tools. But whether they will use those tools for genius is quite unpredictable" - Alan Watts*

*Let the mycelium grow! 🌱*
