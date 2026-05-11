# CADMIES Agent System

**Executable concepts that think, analyze, and connect.**

## Overview

Agents in CADMIES are **first-class IPLD nodes** — they have CIDs, provenance, relationships, and can read from the mycelium. An agent is a concept that *acts*.

| Property | Description |
|----------|-------------|
| **Minted** | Every agent definition has a permanent CID |
| **Provenance** | Who created the agent and when |
| **Executable** | Runtime code that performs analysis |
| **Air-Gapped** | No external dependencies (Python stdlib only) |
| **Extensible** | Create new agents by implementing the schema |

## Available Agents
### Agent 01. Willie the Librarian (LLM Bridge Agent)

The primary user-facing agent. Answers natural language questions by searching the mycelium and synthesizing responses via local LLM.

| Field | Value |
|-------|-------|
| **Human ID** | `willie_the_librarian` |
| **Runtime** | `agents/code/llm_mycelium_reader.py` |
| **Agent Type** | `llm_mycelium_reader` |
| **Version** | v1.2.1 |
| **Domain** | Knowledge Retrieval / LLM Bridge |

**Capabilities:**
- Hybrid search: keyword matching + semantic query expansion via Mistral
- Connects concepts across domains (Mycelial Rosetta Effect)
- Accuracy tags on all factual claims
- Terminal and GUI interfaces
- Finding cross-domain connections even when vocabularies differ


### Agent 02. Philosophical Analyzer Agent

The flagship agent that analyzes concepts for patterns, connections, and insights.

| Field | Value |
|-------|-------|
| **Human ID** | `philosophical_pattern_finder_v1` |
| **CID** | `bafyreiespm2eqtzr7d233hyiqqfwnqc2vu7uwz7msr2qxijhj6gvxifpqe` |
| **Runtime** | `agents/code/philosophical_analyzer.py` |
| **Agent Type** | `philosophical_analyzer` |
| **Domain** | Metaphysics / Epistemology |

**Capabilities:**
- Load concepts from `store/blocks/` by CID
- Extract key terms and domain distributions
- Find semantic connections between concepts
- Generate insights and recommendations
- Save analysis results to JSON

## Directory Structure

```text
agents/
├── code/                              # Agent runtime implementations
│   └── philosophical_analyzer.py      # Philosophical analyzer agent
├── schemas/                           # Agent schemas and documentation
│   └── agent_node/
│       ├── schema_v1.0.0.json         # AgentNode JSON schema
│       ├── agentnode_ipld_schema_definition_v1.0.0.md
│       └── AGENTNODE_SCHEMA_USAGE_GUIDE_v1.0.0.md
└── README.md                          # This file
```
```
## Usage

### Prerequisites

- Python 3.9+
    
- CADMIES blockstore with concepts (existing CIDs)
    

### Run the Philosophical Analyzer

**Analyze specific concepts by CID:**

bash

cd CADMIES-IPLD
python agents/code/philosophical_analyzer.py --cids CID1 CID2 CID3 --depth detailed

**Analyze all concepts in your mycelium:**

bash

python agents/code/philosophical_analyzer.py --cids $(python -c "import json; f=open('store/index/human_id_to_cid.json'); d=json.load(f); print(' '.join(d.values()))") --depth comprehensive

**Run the self-test (validates agent works):**

bash

python agents/code/philosophical_analyzer.py --test

### Analysis Depth Levels

|Depth|What It Does|Use Case|
|---|---|---|
|`basic`|Domain distribution, type distribution, top terms|Quick overview|
|`detailed`|All basic + pairwise semantic connections|Finding relationships|
|`comprehensive`|All detailed + cluster analysis, deeper insights|Full knowledge mapping|

### Output

Results are saved to `analysis_results/analysis_results_YYYYMMDD_HHMMSS.json` with:

json

{
  "success": true,
  "concepts_analyzed": 122,
  "domain_distribution": {"Physics": 7, "Philosophy": 3, ...},
  "type_distribution": {"ScientificLaw": 2, "CognitiveAgent": 1, ...},
  "common_terminology": {"system": 8, "physical": 6, ...},
  "connections": [...],
  "insights": [...],
  "recommendations": [...],
  "metadata": {
    "analyzer_version": "1.0.0",
    "analysis_timestamp": "2026-04-05T02:24:52Z",
    "execution_time_seconds": 0.08,
    "analysis_depth": "comprehensive"
  }
}

## Agent Schema

Agent definitions extend the `UniversalScientificConcept` schema with agent-specific fields:

### Required Fields

|Field|Type|Description|
|---|---|---|
|`agent_type`|string|`classifier`, `reasoner`, `philosophical_analyzer`, etc.|
|`execution_spec`|object|Runtime configuration|
|`activation_state`|object|Current state and history|

### execution_spec Structure

json

{
  "language": "python",
  "entry_point": "function_name(concept_cids: list, context: dict) -> dict",
  "requirements": ["bafyrei...", "bafyrei..."],
  "environment_spec": {
    "python_version": "3.9+",
    "libraries": ["json", "re", "collections"],
    "resource_limits": {
      "memory_mb": 256,
      "timeout_seconds": 30
    }
  }
}

### activation_state Structure

json

{
  "active": false,
  "last_activated": "2026-04-05T00:00:00Z",
  "activation_count": 5,
  "threshold": 0.5
}

### Optional Fields

|Field|Purpose|
|---|---|
|`connection_graph`|Links to other agents/concepts|
|`memory_schema`|Memory configuration|
|`learning_parameters`|Learning rate, exploration, update frequency|

## Creating a New Agent

### Step 1: Define the Agent (JSON)

Create a JSON file in `source_concepts/` following the AgentNode schema:

json

{
  "schema_version": "1.0.0",
  "human_id": "your_agent_v1",
  "title": "Your Agent Name",
  "definition": "What this agent does...",
  "type": "CognitiveAgent",
  "domain": "Your Domain",
  "agent_type": "your_agent_type",
  "execution_spec": {
    "language": "python",
    "entry_point": "your_function(concept_cids: list, context: dict) -> dict",
    "requirements": [],
    "environment_spec": {
      "python_version": "3.9+",
      "libraries": ["json"],
      "resource_limits": {"memory_mb": 256, "timeout_seconds": 30}
    }
  },
  "activation_state": {
    "active": false,
    "activation_count": 0,
    "threshold": 0.5
  }
}

### Step 2: Implement the Runtime

Create `agents/code/your_agent.py` with the entry point function:

python

def your_function(concept_cids: list, context: dict = None) -> dict:
    """
    Your agent logic here.
    
    Args:
        concept_cids: List of CIDs to analyze
        context: Optional execution context
    
    Returns:
        Dict with analysis results
    """
    # Load concepts from blockstore
    # Perform analysis
    # Return results
    return {"success": True, "results": {...}}

### Step 3: Mint the Agent Definition

bash

python tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/your_agent.json

The agent now has a permanent CID and is part of the mycelium.

### Step 4: Test Your Agent

bash

python agents/code/your_agent.py --cids CID1 CID2

## Agent Types (Schema Enum)

|Type|Purpose|
|---|---|
|`classifier`|Categorize concepts|
|`reasoner`|Logical inference|
|`memory`|Information storage/retrieval|
|`synthesizer`|Content generation|
|`sensor`|Environmental input|
|`effector`|Action execution|
|`philosophical_analyzer`|Philosophical pattern finding|
|`scientific_reasoner`|Scientific hypothesis testing|
|`metaphysical_explorer`|Metaphysical exploration|

## Design Principles

1. **Air-Gapped First** — No external API calls; use Python stdlib only
    
2. **Deterministic** — Same inputs → Same outputs (for given blockstore state)
    
3. **Content-Addressed** — Agents reference concepts by CID
    
4. **Provenance-Aware** — Agent actions can be tracked (future)
    
5. **Composable** — Agents can call other agents (future)
    

## Future Capabilities

|Feature|Status|
|---|---|
|Multi-agent orchestration|📋 Planned|
|Agent-to-agent messaging|📋 Planned|
|Agent signing (crypto provenance)|📋 Planned|
|GUI integration (Analyze button)|📋 Planned|
|Agent scheduling (cron-like)|📋 Planned|
|Embedding-based similarity|📋 Planned|
|Local LLM integration|📋 Planned|

## Troubleshooting

### "Concept block not found"

- Ensure CID exists in `store/blocks/`
    
- Check that `paths.py` has correct `PROJECT_ROOT`
    

### Agent runs but finds no connections

- Try `--depth comprehensive` for deeper analysis
    
- Ensure concepts have populated `domain`, `type`, `definition` fields
    

### Import errors

- Agent uses Python stdlib only (json, re, collections, pathlib, typing)
    
- No external dependencies required
    

## Related Documentation

|Document|Location|
|---|---|
|AgentNode Schema|`agents/schemas/agent_node/schema_v1.0.0.json`|
|Schema Usage Guide|`agents/schemas/agent_node/AGENTNODE_SCHEMA_USAGE_GUIDE_v1.0.0.md`|
|Schema Definition|`agents/schemas/agent_node/agentnode_ipld_schema_definition_v1.0.0.md`|
|CID Structure Spec|`specs/CADMIES_CID_STRUCTURE_SPECIFICATION_v2.0.1.md`|

---

> _"A well-specified agent is half-executed." — MDI Development Principle_

**Let the mycelium think. 🌱🧠**
