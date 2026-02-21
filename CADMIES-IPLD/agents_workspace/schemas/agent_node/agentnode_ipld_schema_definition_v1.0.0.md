# AgentNode IPLD Schema v1.0.0

**Schema Name:** AgentNode  
**Extends:** UniversalScientificConcept v1.0.0  
**Status:** ACTIVE DEVELOPMENT  
**Created:** 2025-12-29  
**Location:** `agents_workspace/schemas/agent_node/agentnode_ipld_schema_definition_v1.0.0.md`

## EXECUTIVE SUMMARY

The **AgentNode** schema defines intelligent agents within the CADMIES → Mycorrhizal Digital Intelligence (MDI) ecosystem. It extends the foundational `UniversalScientificConcept` schema by adding capabilities for executable logic, network connections, memory, and learning.

## ARCHITECTURAL HIERARCHY

UniversalScientificConcept (Base - v1.0.0)
└── AgentNode (Extension - v1.0.0)
├── Inherits all UniversalScientificConcept fields
├── Adds agent-specific capabilities
└── Enables executable cognitive functions
text


## SCHEMA SPECIFICATION

### Core Extension Fields

#### 1. `agent_type` (Required)
**Purpose:** Defines the cognitive capability of the agent.
**Values:**
- `classifier`: Pattern recognition, categorization
- `reasoner`: Logical inference, decision making  
- `memory`: Information storage and retrieval
- `synthesizer`: Content generation, combination
- `sensor`: Environmental input processing
- `effector`: Action execution, output generation
- `philosophical_analyzer`: Specialized for metaphysical concepts
- `scientific_reasoner`: Scientific hypothesis testing
- `metaphysical_explorer`: Pattern finding in philosophical systems

#### 2. `execution_spec` (Required)
**Purpose:** Specifies how the agent executes.
```json
{
  "language": "python",
  "entry_point": "process(input: dict, context: dict) -> dict",
  "requirements": ["bafyreidependency1", "bafyreidependency2"],
  "environment_spec": {
    "python_version": "3.9+",
    "libraries": ["numpy"],
    "resource_limits": {
      "memory_mb": 512,
      "timeout_seconds": 30
    }
  }
}

3. activation_state (Required)

Purpose: Tracks agent activation status and history.
json

{
  "active": false,
  "last_activated": "2025-12-29T10:00:00Z",
  "activation_count": 5,
  "threshold": 0.5
}

Optional Extension Fields
4. connection_graph

Purpose: Defines network connections to other agents/concepts.
json

{
  "nodes": ["bafyreiagent1", "bafyreiagent2"],
  "edges": [
    {
      "source": "bafyreiagent1",
      "target": "bafyreiagent2",
      "weight": 0.75,
      "type": "data_flow",
      "description": "Passes processed patterns"
    }
  ],
  "graph_type": "data_flow",
  "directed": true
}

5. memory_schema

Purpose: Configures agent memory capabilities.
json

{
  "memory_type": "semantic",
  "storage_cid": "bafyreistorage",
  "capacity": 1000,
  "retrieval_mechanism": "similarity_search"
}

6. learning_parameters

Purpose: Controls agent learning behavior.
json

{
  "learning_rate": 0.01,
  "exploration_rate": 0.1,
  "update_frequency": "batch"
}

🔗 BACKWARD COMPATIBILITY

Guarantee: Every AgentNode instance is also a valid UniversalScientificConcept instance.

Validation Chain:

    AgentNode must pass UniversalScientificConcept validation

    AgentNode must pass additional agent-specific validation

    Existing concepts can be referenced by agents via CIDs

EXAMPLE AGENT STRUCTURE
json

{
  "schema_version": "1.0.0",
  "human_id": "philosophical_pattern_finder",
  "title": "Philosophical Pattern Finder Agent",
  "definition": "Agent that identifies self-similar patterns across metaphysical concepts",
  "type": "CognitiveAgent",
  "domain": "Metaphysics",
  "metadata": {
    "created": "2025-12-29T10:00:00Z",
    "creator": "MDI Development Team",
    "certainty_score": 0.8,
    "version": 1
  },
  "agent_type": "philosophical_analyzer",
  "execution_spec": {
    "language": "python",
    "entry_point": "find_patterns(concepts: list) -> dict",
    "requirements": [
      "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja"
    ]
  },
  "activation_state": {
    "active": false,
    "threshold": 0.6
  }
}

🔄 INTEGRATION WITH EXISTING SYSTEM
CID Generation

Same cid_generator_v1.1.0.py tool works for AgentNode:
bash

python3 tools/core/cid_generator_v1.1.0.py --concept-file agent_definition.json

Block Storage

Same store/blocks/ location stores AgentNode CBOR files.
Reading

Same cbor_reader.py tool can read AgentNode blocks.
Indexing

Same human_id_to_cid.json index includes AgentNode entries.
NEXT DEVELOPMENT STEPS

    Validator Extension: Update validator to handle AgentNode-specific validation

    Test Agent Creation: Create first philosophical analyzer agent

    Storage Testing: Store/retrieve agent via existing tools

    Runtime Integration: Begin Phase 3 (runtime interpreter development)

RELATED DOCUMENTS

    UniversalScientificConcept Schema

    Agent Schema Development Roadmap (CA-2025-044-ROADMAP)

    Universal Scientific Concept Specification (CA-2025-043-SPEC-REV)

Schema Version: 1.0.0
Status: ACTIVE DEVELOPMENT
Last Updated: 2025-12-29

"From storing knowledge to thinking with knowledge."
