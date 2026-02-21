# AGENTNODE SCHEMA USAGE GUIDE v1.0.0

## EXECUTIVE SUMMARY

**Purpose:** Guide for creating valid AgentNode specifications that extend UniversalScientificConcept  
**Scope:** Field-by-field explanation, validation rules, examples, and best practices  
**Status:** ACTIVE - All new AgentNode specifications must comply  
**Schema Location:** `agents_workspace/schemas/agent_node/schema_v1.0.0.json`

## 1.0 OVERVIEW

### 1.1 What is AgentNode?

AgentNode is a JSON Schema that **extends** the existing `UniversalScientificConcept` schema to add intelligent agent capabilities:

UniversalScientificConcept (Base Schema)
└── AgentNode (Extension)
├── agent_type: Cognitive capability classification
├── execution_spec: How the agent executes
├── activation_state: Runtime state management
└── [Optional extensions for specific agent types]
text


### 1.2 Key Design Principles

1. **Backward Compatibility:** All AgentNode instances are valid UniversalScientificConcept instances
2. **Separation of Concerns:** Specification (what) vs Implementation (how)
3. **Content Addressing:** AgentNode specifications get CIDs like any other concept
4. **Runtime Independence:** Schema doesn't prescribe specific runtime implementation

### 1.3 Schema Inheritance

AgentNode uses JSON Schema `allOf` to extend the base:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentNode",
  "allOf": [
    {
      "$ref": "../universal_scientific_concept/universal_scientific_concept_schema_v1.0.0.json"
    }
  ],
  "required": ["agent_type", "execution_spec", "activation_state"],
  "properties": {
    // Agent-specific properties
  }
}

2.0 REQUIRED FIELDS
2.1 agent_type Field

Type: string
Required: Yes
Enum Values:
json

{
  "agent_type": {
    "type": "string",
    "enum": [
      "classifier",
      "reasoner", 
      "memory",
      "synthesizer",
      "sensor",
      "effector",
      "philosophical_analyzer",
      "scientific_reasoner",
      "metaphysical_explorer"
    ]
  }
}

Agent Type Definitions:
Agent Type	Purpose	Example Implementation
classifier	Categorize and classify concepts	classify_scientific_concepts()
reasoner	Logical inference and decision making	reason_about_physics()
memory	Information storage and retrieval	store_experience()
synthesizer	Content generation and combination	synthesize_new_theory()
sensor	Environmental input processing	analyze_data_stream()
effector	Action execution and output generation	generate_report()
philosophical_analyzer	Analyze philosophical concepts	analyze_philosophical_patterns()
scientific_reasoner	Scientific reasoning	evaluate_hypothesis()
metaphysical_explorer	Metaphysical exploration	explore_metaphysical_space()

Usage Example:
json

{
  "agent_type": "philosophical_analyzer"
}

2.2 execution_spec Field

Type: object
Required: Yes
Purpose: Defines how the agent executes

Structure:
json

{
  "execution_spec": {
    "type": "object",
    "required": ["language", "entry_point"],
    "properties": {
      "language": {"type": "string", "enum": ["python", "javascript", "wasm"]},
      "entry_point": {"type": "string"},
      "requirements": {
        "type": "array",
        "items": {"type": "string", "pattern": "^bafyrei[a-z2-7]{59}$"}
      },
      "environment_spec": {
        "type": "object",
        "properties": {
          "python_version": {"type": "string"},
          "libraries": {"type": "array", "items": {"type": "string"}},
          "resource_limits": {
            "type": "object",
            "properties": {
              "memory_mb": {"type": "integer", "minimum": 1},
              "timeout_seconds": {"type": "integer", "minimum": 1}
            }
          }
        }
      }
    }
  }
}

2.2.1 language Sub-field

    Required: Yes

    Values: "python", "javascript", "wasm"

    Purpose: Runtime language for agent execution

    Current Support: Only "python" fully implemented

Example:
json

{
  "language": "python"
}

2.2.2 entry_point Sub-field

    Required: Yes

    Type: string

    Format: Function signature following Python type hint conventions

    Purpose: Identifies which function to call in the implementation

Valid Formats:
json

// Simple function name
"entry_point": "analyze_concepts"

// With parameter types
"entry_point": "analyze_concepts(concept_cids: list) -> dict"

// Full signature with parameter and return types
"entry_point": "analyze_concepts(concept_cids: list, context: dict) -> dict"

Best Practice: Use simple signature without default values:
json

"entry_point": "function_name(param1: type1, param2: type2) -> return_type"

Extraction Rule: Runtime extracts function name as everything before the first (

Example:
json

{
  "entry_point": "analyze_philosophical_patterns(concept_cids: list, context: dict) -> dict"
}
// Function name extracted: "analyze_philosophical_patterns"

2.2.3 requirements Sub-field

    Required: No (optional)

    Type: array of string (CIDs)

    Pattern: Must match ^bafyrei[a-z2-7]{59}$

    Purpose: List of CIDs that this agent requires as input

Example:
json

{
  "requirements": [
    "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
    "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m"
  ]
}

Validation Rules:

    All CIDs must exist in the blockstore at creation time

    CIDs must reference valid IPLD blocks

    No circular dependencies allowed

    Maximum of 100 requirements recommended (performance)

2.2.4 environment_spec Sub-field

    Required: No (optional)

    Type: object

    Purpose: Runtime environment requirements

Structure:
json

{
  "environment_spec": {
    "python_version": "3.9+",
    "libraries": ["json", "re", "collections"],
    "resource_limits": {
      "memory_mb": 512,
      "timeout_seconds": 30
    }
  }
}

Field Details:

    python_version: String like "3.9+", "3.8", ">=3.7"

    libraries: Array of Python standard library module names

    resource_limits.memory_mb: Maximum memory in megabytes (minimum: 1)

    resource_limits.timeout_seconds: Maximum execution time (minimum: 1)

Air-Gapped Constraint: Only Python standard library modules allowed in libraries
2.3 activation_state Field

Type: object
Required: Yes
Purpose: Track runtime activation state and history

Structure:
json

{
  "activation_state": {
    "type": "object",
    "properties": {
      "active": {"type": "boolean", "default": false},
      "last_activated": {"type": "string", "format": "date-time"},
      "activation_count": {"type": "integer", "minimum": 0},
      "threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5}
    }
  }
}

Field Details:

    active: Whether agent is currently active (runtime-managed)

    last_activated: ISO 8601 timestamp of last activation

    activation_count: Total number of activations

    threshold: Activation threshold (0.0-1.0) for connection graphs

Initial State Example:
json

{
  "activation_state": {
    "active": false,
    "last_activated": null,
    "activation_count": 0,
    "threshold": 0.5
  }
}

3.0 OPTIONAL FIELDS
3.1 connection_graph Field

Type: object
Required: No (optional)
Purpose: Define connections to other agents/concepts

Structure:
json

{
  "connection_graph": {
    "type": "object",
    "properties": {
      "nodes": {
        "type": "array",
        "items": {"type": "string", "pattern": "^bafyrei[a-z2-7]{59}$"}
      },
      "edges": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "source": {"type": "string", "pattern": "^bafyrei[a-z2-7]{59}$"},
            "target": {"type": "string", "pattern": "^bafyrei[a-z2-7]{59}$"},
            "weight": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "type": {"type": "string", "enum": ["data_flow", "control_flow", "semantic"]},
            "description": {"type": "string"}
          },
          "required": ["source", "target"]
        }
      },
      "graph_type": {"type": "string", "enum": ["data_flow", "control_flow", "hybrid"]},
      "directed": {"type": "boolean", "default": true}
    }
  }
}

Usage Example:
json

{
  "connection_graph": {
    "nodes": [
      "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
      "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m"
    ],
    "edges": [
      {
        "source": "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
        "target": "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m",
        "weight": 0.75,
        "type": "semantic",
        "description": "Fractal patterns inform liberation mechanisms"
      }
    ],
    "graph_type": "semantic",
    "directed": true
  }
}

3.2 memory_schema Field

Type: object
Required: No (optional)
Purpose: Define memory configuration for the agent

Structure:
json

{
  "memory_schema": {
    "type": "object",
    "properties": {
      "memory_type": {
        "type": "string",
        "enum": ["episodic", "semantic", "procedural", "working"]
      },
      "storage_cid": {"type": "string", "pattern": "^bafyrei[a-z2-7]{59}$"},
      "capacity": {"type": "integer", "minimum": 1},
      "retrieval_mechanism": {"type": "string"}
    }
  }
}

Usage Example:
json

{
  "memory_schema": {
    "memory_type": "semantic",
    "storage_cid": "bafyreihlh4vwiexvuq667arus727jqs7sifuf3vjuyczwmqqcfpcopghsq",
    "capacity": 1000,
    "retrieval_mechanism": "pattern_similarity"
  }
}

3.3 learning_parameters Field

Type: object
Required: No (optional)
Purpose: Parameters for agent learning and adaptation

Structure:
json

{
  "learning_parameters": {
    "type": "object",
    "properties": {
      "learning_rate": {"type": "number", "minimum": 0.0, "maximum": 1.0},
      "exploration_rate": {"type": "number", "minimum": 0.0, "maximum": 1.0},
      "update_frequency": {
        "type": "string",
        "enum": ["immediate", "batch", "periodic"]
      }
    }
  }
}

Usage Example:
json

{
  "learning_parameters": {
    "learning_rate": 0.01,
    "exploration_rate": 0.1,
    "update_frequency": "batch"
  }
}

4.0 INHERITED FIELDS FROM UNIVERSALSCIENTIFICCONCEPT

AgentNode inherits all fields from the base schema. Key inherited fields:
4.1 Required Inherited Fields
Field	Type	Purpose	AgentNode Usage
schema_version	string	Schema version	Should be "1.0.0" for AgentNode
human_id	string	Human-readable identifier	Agent identifier (e.g., "philosophical_pattern_finder_v1")
title	string	Concept title	Agent name/title
definition	string	Complete definition	Agent purpose and capabilities
type	string	Concept type	Should be "CognitiveAgent" or similar
domain	string	Primary domain	Agent domain (e.g., "Metaphysics")
subdomain	string	Specialized area	Agent specialization (e.g., "Pattern Recognition")
proofs	array	Scientific evidence	Agent validation evidence
metadata	object	Provenance tracking	Agent creation metadata
relationships	object	Links to other concepts	Can include agent dependencies
difficulty_levels	object	Educational levels	Agent complexity levels
4.2 AgentNode-Specific Values for Inherited Fields

type Field:
json

{
  "type": "CognitiveAgent"
}

Recommended Values: "CognitiveAgent", "IntelligentSystem", "AI_Agent"

domain Field:
json

{
  "domain": "Artificial Intelligence"
}

Common Domains: "Artificial Intelligence", "Cognitive Science", "Metaphysics", "Science"

difficulty_levels Field:
json

{
  "difficulty_levels": {
    "beginner": "An AI assistant that [simple description]",
    "intermediate": "A cognitive agent that [technical description]",
    "expert": "IPLD-based intelligent agent extending UniversalScientificConcept schema with [detailed technical]"
  }
}

5.0 VALIDATION RULES
5.1 Schema Compliance Validation

All AgentNode specifications must:

    Pass JSON Schema validation against schema_v1.0.0.json

    Include all required fields from both base and extension schemas

    Have valid field types and enum values

    Have CIDs that match the pattern ^bafyrei[a-z2-7]{59}$

5.2 Semantic Validation

Agent Type Consistency:

    agent_type must match implementation file name: {agent_type}.py

    entry_point function must exist in implementation

    requirements CIDs must exist in blockstore

Execution Spec Validation:

    language must be supported by runtime (currently only "python")

    entry_point must be parseable to extract function name

    environment_spec.libraries must be Python stdlib modules only

5.3 Content Validation

Before CID Generation:

    Validate against JSON Schema

    Verify all requirement CIDs exist

    Check entry_point format is parseable

    Ensure agent_type has corresponding implementation

After Creation:

    Generated CID must match content

    Must be stored in blockstore

    Must be indexed by human_id

6.0 CREATION WORKFLOW
6.1 Step-by-Step Creation

Step 1: Define Agent Purpose
json

{
  "human_id": "science:analyzer/scientific_concept_classifier_v1",
  "title": "Scientific Concept Classifier Agent v1.0",
  "definition": "Cognitive agent that classifies scientific concepts into domains and subdomains based on their content and relationships.",
  "type": "CognitiveAgent",
  "domain": "Artificial Intelligence",
  "subdomain": "Classification Systems"
}

Step 2: Define Execution Specification
json

{
  "agent_type": "classifier",
  "execution_spec": {
    "language": "python",
    "entry_point": "classify_scientific_concepts(concept_cids: list, context: dict) -> dict",
    "requirements": [
      "bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji",
      "bafyreignyf5lwzy2npt7bx3w7fllx55dnhjohdjxbjk5vpuknldw4xiovi"
    ],
    "environment_spec": {
      "python_version": "3.9+",
      "libraries": ["json", "collections", "re"],
      "resource_limits": {
        "memory_mb": 256,
        "timeout_seconds": 30
      }
    }
  }
}

Step 3: Define Agent State
json

{
  "activation_state": {
    "active": false,
    "last_activated": null,
    "activation_count": 0,
    "threshold": 0.6
  }
}

Step 4: Add Optional Fields (if needed)
json

{
  "connection_graph": {
    "nodes": [...],
    "edges": [...]
  },
  "memory_schema": {...},
  "learning_parameters": {...}
}

Step 5: Complete Inherited Fields
json

{
  "schema_version": "1.0.0",
  "proofs": [
    {
      "type": "implementation_exists",
      "reference": "agents/code/classifier.py",
      "confidence": 0.9,
      "description": "Implementation file exists and passes syntax check"
    }
  ],
  "metadata": {
    "created": "2025-12-29T18:30:00Z",
    "creator": "Agent Development Team",
    "version": "1.0.0"
  },
  "relationships": {
    "builds_upon": [
      "bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji"
    ],
    "related_to": [...]
  },
  "difficulty_levels": {
    "beginner": "An AI that sorts scientific ideas into categories",
    "intermediate": "A classification agent that analyzes concept content and metadata",
    "expert": "IPLD-based cognitive agent using content-addressed scientific concepts with pattern recognition algorithms"
  }
}

6.2 Validation Command
bash

# Validate against schema
python3 -c "
import json
from jsonschema import validate, ValidationError

# Load schema
with open('agents_workspace/schemas/agent_node/schema_v1.0.0.json', 'r') as f:
    schema = json.load(f)

# Load agent spec
with open('new_agent_spec.json', 'r') as f:
    agent_spec = json.load(f)

try:
    validate(instance=agent_spec, schema=schema)
    print('Schema validation passed')
except ValidationError as e:
    print(f'Validation failed: {e.message}')
    print(f'Path: {e.json_path}')
"

6.3 CID Generation
bash

# Use existing cid_generator
python3 tools/core/cid_generator_v1.1.0.py new_agent_spec.json

7.0 EXAMPLES
7.1 Complete Minimal AgentNode
json

{
  "schema_version": "1.0.0",
  "human_id": "ai:classifier/scientific_concept_classifier_v1",
  "title": "Scientific Concept Classifier Agent v1.0",
  "definition": "Cognitive agent that classifies scientific concepts into domains and subdomains.",
  "type": "CognitiveAgent",
  "domain": "Artificial Intelligence",
  "subdomain": "Classification",
  "proofs": [
    {
      "type": "design_specification",
      "confidence": 0.8,
      "description": "Agent design follows AgentNode schema v1.0.0"
    }
  ],
  "metadata": {
    "created": "2025-12-29T18:30:00Z",
    "creator": "Agent Development Team",
    "version": "1.0.0"
  },
  "relationships": {
    "builds_upon": []
  },
  "difficulty_levels": {
    "beginner": "An AI that sorts scientific ideas",
    "intermediate": "Classification agent for scientific concepts",
    "expert": "IPLD-based cognitive agent for scientific concept classification"
  },
  "agent_type": "classifier",
  "execution_spec": {
    "language": "python",
    "entry_point": "classify_scientific_concepts(concept_cids: list, context: dict) -> dict",
    "requirements": [],
    "environment_spec": {
      "python_version": "3.9+",
      "libraries": ["json", "collections"],
      "resource_limits": {
        "memory_mb": 256,
        "timeout_seconds": 30
      }
    }
  },
  "activation_state": {
    "active": false,
    "last_activated": null,
    "activation_count": 0,
    "threshold": 0.5
  }
}

7.2 Complex Agent with Dependencies
json

{
  "schema_version": "1.0.0",
  "human_id": "metaphysics:analyzer/philosophical_pattern_finder_v1",
  "title": "Philosophical Pattern Finder Agent v1.0.0",
  "definition": "Cognitive agent that identifies self-similar patterns and connections across metaphysical concepts using our existing philosophical knowledge base.",
  "type": "CognitiveAgent",
  "domain": "Metaphysics",
  "subdomain": "Pattern Recognition",
  "proofs": [
    {
      "type": "design_specification",
      "confidence": 0.9,
      "reference": "AgentNode schema v1.0.0",
      "description": "Agent schema validates against AgentNode v1.0.0 specification"
    }
  ],
  "metadata": {
    "created": "2025-12-29T16:30:00Z",
    "creator": "MDI Development Team",
    "version": "1",
    "certainty_score": 0.85
  },
  "relationships": {
    "builds_upon": [
      "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
      "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m",
      "bafyreigcii5de4qhwnn25i62gxa245s5fwn5nbrzz3in346ut5kem4j474",
      "bafyreihlh4vwiexvuq667arus727jqs7sifuf3vjuyczwmqqcfpcopghsq",
      "bafyreiht7rhfuixpxqtfelgckhwboi7ytzar4sullw2f73mksbbsn74f4q"
    ]
  },
  "difficulty_levels": {
    "beginner": "An AI assistant that finds connections between philosophical ideas",
    "intermediate": "A cognitive agent that analyzes metaphysical concepts for patterns",
    "expert": "IPLD-based intelligent agent extending UniversalScientificConcept schema with executable pattern recognition capabilities for philosophical concept analysis"
  },
  "agent_type": "philosophical_analyzer",
  "execution_spec": {
    "language": "python",
    "entry_point": "analyze_philosophical_patterns(concept_cids: list, context: dict) -> dict",
    "requirements": [
      "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
      "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m",
      "bafyreigcii5de4qhwnn25i62gxa245s5fwn5nbrzz3in346ut5kem4j474",
      "bafyreihlh4vwiexvuq667arus727jqs7sifuf3vjuyczwmqqcfpcopghsq",
      "bafyreiht7rhfuixpxqtfelgckhwboi7ytzar4sullw2f73mksbbsn74f4q"
    ],
    "environment_spec": {
      "python_version": "3.9+",
      "libraries": ["json", "re", "collections"],
      "resource_limits": {
        "memory_mb": 512,
        "timeout_seconds": 30
      }
    }
  },
  "activation_state": {
    "active": false,
    "last_activated": null,
    "activation_count": 0,
    "threshold": 0.5
  },
  "connection_graph": {
    "nodes": [
      "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
      "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m",
      "bafyreigcii5de4qhwnn25i62gxa245s5fwn5nbrzz3in346ut5kem4j474",
      "bafyreihlh4vwiexvuq667arus727jqs7sifuf3vjuyczwmqqcfpcopghsq",
      "bafyreiht7rhfuixpxqtfelgckhwboi7ytzar4sullw2f73mksbbsn74f4q"
    ],
    "edges": [
      {
        "source": "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",
        "target": "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m",
        "weight": 0.75,
        "type": "semantic",
        "description": "Fractal patterns inform liberation mechanisms"
      }
    ],
    "graph_type": "semantic",
    "directed": true
  },
  "memory_schema": {
    "memory_type": "semantic",
    "capacity": 100,
    "retrieval_mechanism": "pattern_similarity"
  }
}

8.0 BEST PRACTICES
8.1 Naming Conventions

Human ID Format:
text

{domain}:{type}/{agent_name}_v{version}

Examples:

    metaphysics:analyzer/philosophical_pattern_finder_v1

    science:classifier/scientific_concept_classifier_v1

    ai:reasoner/logical_inference_engine_v2

Title Format:
text

{Agent Name} Agent v{version}

Examples:

    Philosophical Pattern Finder Agent v1.0.0

    Scientific Concept Classifier Agent v1.0

8.2 Versioning

Schema Version: Always "1.0.0" for AgentNode v1.0.0

Agent Version: Increment with changes:

    v1.0.0: Initial release

    v1.0.1: Bug fixes, no API changes

    v1.1.0: New features, backward compatible

    v2.0.0: Breaking changes

8.3 Documentation Quality

Definition Field: Should clearly state:

    What the agent does

    What inputs it requires

    What outputs it produces

    Any special capabilities or limitations

Difficulty Levels:

    Beginner: Simple, non-technical description

    Intermediate: Technical description for developers

    Expert: Full technical details including schema references

8.4 Security Considerations

Air-Gapped Compliance:

    Only Python stdlib in libraries

    No network operations in implementation

    No external dependencies

Resource Limits:

    Set reasonable memory_mb (typically 256-1024)

    Set timeout_seconds to prevent hanging (typically 30-60)

    Consider agent complexity when setting limits

9.0 TROUBLESHOOTING
9.1 Common Validation Errors

Error: 'agent_type' is a required property
Solution: Add agent_type field with valid enum value

Error: 'bafy...' does not match pattern '^bafyrei[a-z2-7]{59}$'
Solution: Verify CID format, ensure it's a valid CIDv1

Error: 'entry_point' is a required property
Solution: Add entry_point with function signature

Error: Additional properties not allowed
Solution: Remove fields not defined in schema
9.2 Runtime Errors

Error: Function 'function_name' not found in module
Solution: Ensure entry_point function name matches implementation

Error: Agent implementation not found
Solution: Create agents/code/{agent_type}.py file

Error: Required block not found
Solution: Verify requirement CIDs exist in blockstore
9.3 Debugging Checklist

    Validate against schema: Use JSON Schema validator

    Check CIDs exist: Verify all requirement CIDs in blockstore

    Test implementation: Run agent implementation directly

    Verify paths: Check agents/code/ directory exists

    Check runtime: Test with python3 runtime/runtime-minimal_agent_executor.py --test

10.0 APPENDICES
Appendix A: Schema Location Reference

Primary Schema:

    agents_workspace/schemas/agent_node/schema_v1.0.0.json

Base Schema:

    agents_workspace/schemas/universal_scientific_concept/universal_scientific_concept_schema_v1.0.0.json

Example Agent:

    agents_workspace/schemas/agent_node/examples/philosophical_pattern_finder_agent_v1.0.0.json

Appendix B: Field Reference Table
Field	Required	Type	Description
AgentNode Specific			
agent_type	Yes	string (enum)	Type of cognitive capability
execution_spec	Yes	object	How the agent executes
execution_spec.language	Yes	string (enum)	Runtime language
execution_spec.entry_point	Yes	string	Function signature
execution_spec.requirements	No	array of CIDs	Required inputs
execution_spec.environment_spec	No	object	Runtime requirements
activation_state	Yes	object	Runtime state
connection_graph	No	object	Agent connections
memory_schema	No	object	Memory configuration
learning_parameters	No	object	Learning parameters
Inherited from UniversalScientificConcept			
schema_version	Yes	string	Schema version
human_id	Yes	string	Human-readable ID
title	Yes	string	Agent title
definition	Yes	string	Agent definition
type	Yes	string	Should be "CognitiveAgent"
domain	Yes	string	Primary domain
subdomain	Yes	string	Specialized area
proofs	Yes	array	Validation evidence
metadata	Yes	object	Creation metadata
relationships	Yes	object	Links to other concepts
difficulty_levels	Yes	object	Complexity levels
Appendix C: Quick Start Template
json

{
  "schema_version": "1.0.0",
  "human_id": "{domain}:{type}/{agent_name}_v1",
  "title": "{Agent Name} Agent v1.0",
  "definition": "Complete description of what this agent does, its inputs, outputs, and purpose.",
  "type": "CognitiveAgent",
  "domain": "{Primary Domain}",
  "subdomain": "{Specialization}",
  "proofs": [
    {
      "type": "design_specification",
      "confidence": 0.8,
      "description": "Agent design follows AgentNode schema v1.0.0"
    }
  ],
  "metadata": {
    "created": "{ISO_TIMESTAMP}",
    "creator": "{Your Name/Team}",
    "version": "1.0.0"
  },
  "relationships": {
    "builds_upon": []
  },
  "difficulty_levels": {
    "beginner": "Simple description for non-technical users",
    "intermediate": "Technical description for developers",
    "expert": "Detailed technical description with schema references"
  },
  "agent_type": "{agent_type}",
  "execution_spec": {
    "language": "python",
    "entry_point": "{function_name}(concept_cids: list, context: dict) -> dict",
    "requirements": [],
    "environment_spec": {
      "python_version": "3.9+",
      "libraries": ["json", "collections"],
      "resource_limits": {
        "memory_mb": 256,
        "timeout_seconds": 30
      }
    }
  },
  "activation_state": {
    "active": false,
    "last_activated": null,
    "activation_count": 0,
    "threshold": 0.5
  }
}

Appendix D: Change Log & Version History
Version	Date	Changes	Author
1.0.0	2025-12-29	Initial release: Complete AgentNode schema usage guide	MDI Development Team
1.0.0-alpha	2025-12-28	Draft for Phase 3 integration	Schema Architecture Team
Appendix E: Related Resources

    Runtime Implementation: runtime/runtime-minimal_agent_executor.py

    Agent Implementation Specification: 2025-12-29_agent_implementation_specification_v1.0.0.md

    Runtime API Reference: 2025-12-29_runtime_api_reference_v1.0.0.md

    Example Agent: agents_workspace/schemas/agent_node/examples/philosophical_pattern_finder_agent_v1.0.0.json

    Agent Implementation: agents/code/philosophical_analyzer.py

11.0 CONCLUSION & NEXT STEPS

11.1 Current Status

The AgentNode schema v1.0.0 is production-ready and has been validated through:

    Schema Validation: All AgentNode instances validate against JSON Schema

    Runtime Execution: First agent (philosophical_pattern_finder_v1) executed successfully

    Backward Compatibility: All AgentNode instances are valid UniversalScientificConcept instances

    Content Addressing: Agents receive deterministic CIDs like any other concept

    Air-Gapped Compliance: No external dependencies required

11.2 Implementation Checklist

Before deploying a new AgentNode:

    Validate against schema_v1.0.0.json

    Create implementation in agents/code/{agent_type}.py

    Test implementation directly with Python

    Generate CID using cid_generator_v1.1.0.py

    Store in blockstore (store/blocks/)

    Verify indexing in store/index/human_id_to_cid.json

    Test execution with runtime-minimal_agent_executor.py

11.3 Future Evolution Considerations

Schema Evolution (v2.0.0):

    Add input_schema for type validation

    Add output_schema for result validation

    Add security_spec for permissions and access control

    Add composability for agent chaining

Runtime Enhancements:

    Multi-agent orchestration

    Connection graph execution

    State persistence across activations

    Performance monitoring and optimization

11.4 Getting Help

    Validation Issues: Check Section 9.0 Troubleshooting

    Runtime Errors: Review runtime API documentation

    Implementation Questions: Refer to Agent Implementation Specification

    Schema Questions: Contact Schema Architecture Team

REFERENCES

    JSON Schema Specification: Draft 7 - http://json-schema.org/draft-07/schema#

    IPLD Specification: https://ipld.io/

    DAG-CBOR Encoding: https://ipld.io/specs/codecs/dag-cbor/

    Multiformats CID: https://github.com/multiformats/cid

*"A well-specified agent is half-executed." - MDI Development Principle*
