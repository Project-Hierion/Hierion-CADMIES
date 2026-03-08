# CADMIES IPLD KNOWLEDGE SYSTEM
## User Guide v1.0.0
### How to Grow Your Mycelial Garden

---

## QUICK START: THE 3-STEP WORKFLOW

### Step 1: Find a Concept (Mining)
Find an interesting idea in conversations, research, or your own thoughts.

### Step 2: Format It (Cultivation)  
Put it in the right format so the system can understand it.

### Step 3: Store It (Planting)
Let the system give it a permanent ID and store it.

**That's it!** Concept -> Format -> Store.

---

## PART 1: MINING CONCEPTS (FINDING SEEDS)

### 1.1 Where to Mine
Look for concepts in:
- **Conversations** (with colleagues, AI, yourself)
- **Research papers** (key findings, methods)
- **Books/articles** (core ideas, principles)
- **Your own thoughts** (insights, connections)
- **System documentation** (how things work)

### 1.2 What to Look For
A good concept has:
- **A clear name** (what it's called)
- **A definition** (what it means)
- **Evidence** (why we believe it)
- **Connections** (how it relates to other concepts)

**Example from a conversation:**
> "You know, our backup system is like a fortress - layered protection, multiple copies, secure locations."

**Mined concept:** "Backup Fortress" analogy.

---

## PART 2: CULTIVATION (FORMATTING CONCEPTS)

### 2.1 The IPLD Format Template
Every concept needs this structure:

```json
{
  "human_id": "Domain:Type/ConceptName",
  "title": "Human Readable Name",
  "definition": "Clear, complete definition here...",
  "type": "Concept|Law|Theory|Principle|Method",
  "domain": "Physics|Philosophy|ComputerScience|Hieros",
  "subdomain": "More specific area",
  "proofs": [
    {
      "type": "experimental|theoretical|observational",
      "description": "Where this came from",
      "confidence": 0.0-1.0,
      "date": "YYYY-MM-DD",
      "reference": "Source or citation"
    }
  ],
  "difficulty_levels": {
    "beginner": "Simple explanation",
    "intermediate": "Detailed explanation", 
    "expert": "Advanced explanation"
  }
}
```

### 2.2 Field-by-Field Guide
human_id (Required)

Format: Domain:Type/ConceptName

    Domain: Broad category (Physics, Hieros, Philosophy)

    Type: What kind of concept (Concept, Law, Method, System)

    ConceptName: Short, memorable name

Examples:

    Physics:Law/ConservationOfEnergy

    Hieros:Concept/DigitalSeed

    Philosophy:Principle/OccamsRazor

title (Required)

Human-readable name. Make it clear and descriptive.
definition (Required)

At least 2-3 sentences. Complete thought. No fragments.
type (Required)

Choose one:

    Concept (General idea)

    Law (Fundamental rule)

    Theory (Explanatory framework)

    Principle (Guiding rule)

    Method (Way of doing something)

    System (Organized collection)

    Observation (Noticed pattern)

domain & subdomain (Required)

Categorize your concept:

    Physics -> Classical Mechanics, Quantum Physics

    ComputerScience -> Algorithms, Data Structures

    Hieros -> Knowledge Systems, Infrastructure

    Philosophy -> Epistemology, Ethics

proofs (Required - at least one)

Every concept needs evidence:

```json

{
  "type": "experimental",  // or theoretical, observational, anecdotal
  "description": "What evidence supports this?",
  "confidence": 0.7,  // 0.0-1.0 scale
  "date": "2024-10-01",
  "reference": "Where this came from"
}
```

Confidence scale:

    0.9-1.0: Well-established, repeatedly verified

    0.7-0.9: Strong evidence, generally accepted

    0.5-0.7: Moderate evidence, some uncertainty

    0.3-0.5: Preliminary, needs more verification

    0.0-0.3: Speculative, weak evidence

difficulty_levels (Required - at least "intermediate")

Explain the concept at different levels:

    beginner: Simple analogy or metaphor

    intermediate: Clear explanation with details

    expert: Technical or advanced perspective

At minimum, provide "intermediate".

### 2.3 Optional Fields
relationships (Optional, but encouraged)

Connect to other concepts:

```json

{
  "builds_upon": ["OtherConceptID"],
  "contradicts": ["OpposingConceptID"],
  "related_to": ["SimilarConceptID"],
  "specializes": ["MoreGeneralConceptID"]
}
```

extra_fields (Optional)

Any additional information:

```json

{
  "tags": ["tag1", "tag2"],
  "formula": "E = mc²",
  "units": "Joules",
  "discovery_year": 1905
}
```

### 2.4 Formatting Example: From Conversation to Concept

Conversation snippet:

    "The way we structure knowledge should be both hierarchical (organized) and organic (able to make unexpected connections)."

Formatted concept:

```json

{
  "human_id": "Hieros:Concept/HierarchicalOrganic",
  "title": "Hierarchical Organic Structure",
  "definition": "A knowledge organization method that combines hierarchical categorization with organic, non-linear connections. Allows both structured navigation and emergent relationship discovery.",
  "type": "Concept",
  "domain": "Hieros",
  "subdomain": "Knowledge Architecture",
  "proofs": [
    {
      "type": "theoretical",
      "description": "Developed through Project Hieros system design discussions",
      "confidence": 0.8,
      "date": "2024-11-15",
      "reference": "Hieros design conversation #42"
    }
  ],
  "difficulty_levels": {
    "beginner": "Organizing information with both clear categories and flexible connections",
    "intermediate": "Dual-mode knowledge structure supporting both taxonomy and emergent graph relationships",
    "expert": "Hybrid knowledge representation combining directed acyclic hierarchies with small-world network properties"
  }
}
```

## PART 3: PLANTING (STORING CONCEPTS)
### 3.1 Using the Workflow Tool

We have a simple tool to store concepts:

```bash

# Navigate to the IPLD system
cd /path/to/CADMIES-IPLD

# Use the workflow tool
python3 tools/ipld_workflow_v1.0.0.py
```

### 3.2 Manual Storage (Advanced)

If you want to store concepts manually:

Create a Python script:
```python

from tools.ipld_workflow import IPLDWorkflow_v1_0_0

workflow = IPLDWorkflow_v1_0_0("./store", "STANDARD")

concept = {
    "human_id": "Your:Concept/Name",
    # ... all required fields
}

result = workflow.create_concept(concept)
if result["success"]:
    print(f"Stored! CID: {result['cid']}")
```

Or use command line:
```bash

# Create a JSON file with your concept
echo '{
  "human_id": "Test:Concept/Example",
  "title": "Example Concept",
  "definition": "An example for testing",
  "type": "Concept",
  "domain": "Test",
  "subdomain": "Examples",
  "proofs": [{"type": "test", "description": "Testing", "confidence": 0.9, "date": "2024-12-24"}],
  "difficulty_levels": {"intermediate": "Example concept"}
}' > my_concept.json

# Use Python to store it
python3 -c "
import json, sys
sys.path.append('.')
from tools.ipld_workflow import IPLDWorkflow_v1_0_0
with open('my_concept.json') as f:
    concept = json.load(f)
workflow = IPLDWorkflow_v1_0_0('./store')
result = workflow.create_concept(concept)
print(f'Result: {result}')
"
```

### 3.3 What Happens When You Store

    Validation: System checks if concept has all required fields

    CID Generation: Creates cryptographic ID from concept content

    Storage: Saves in content-addressed blockstore

    Indexing: Adds to human_id -> CID lookup table

    Confirmation: Returns the CID for future reference

Important: The same concept always gets the same CID. Change anything -> new CID.

## PART 4: FINDING & USING CONCEPTS

### 4.1 Finding by Human ID

```bash

# List all concepts
python3 -c "
import json
with open('store/index/human_id_to_cid.json') as f:
    index = json.load(f)
print('Available concepts:')
for human_id in sorted(index.keys()):
    print(f'   • {human_id}')
"

# Search for specific concepts
python3 -c "
import json
with open('store/index/human_id_to_cid.json') as f:
    index = json.load(f)
search = 'Hieros'
print(f'Concepts containing \"{search}\":')
for human_id, cid in index.items():
    if search in human_id:
        print(f'   • {human_id} -> {cid[:20]}...')
"
```

### 4.2 Retrieving Concepts
```python

from tools.ipld_workflow import IPLDWorkflow_v1_0_0

workflow = IPLDWorkflow_v1_0_0("./store")

# Get by human ID
result = workflow.retrieve_by_human_id("Hieros:Concept/DigitalSeed")
if result["success"]:
    concept = result["concept"]
    print(f"Title: {concept['title']}")
    print(f"Definition: {concept['definition']}")
    print(f"Difficulty levels: {concept['difficulty_levels']}")

# Get all concepts
all_concepts = workflow.list_concepts()
for c in all_concepts["concepts"]:
    print(f"{c['human_id']}: {c['title']}")
```

### 4.3 Using in Different Contexts

For Learning (Beginner mode):
```python

concept = workflow.retrieve_by_human_id("Physics:Law/ConservationOfEnergy")
if concept["success"]:
    explanation = concept["concept"]["difficulty_levels"]["beginner"]
    print(f"Explanation: {explanation}")
```

For Research (Expert mode):
```python

concept = workflow.retrieve_by_human_id("Physics:Law/ConservationOfEnergy")  
if concept["success"]:
    explanation = concept["concept"]["difficulty_levels"]["expert"]
    proofs = concept["concept"]["proofs"]
    print(f"Expert explanation: {explanation}")
    print(f"Evidence: {proofs}")
```

For AI Assistant:
AI assistants can:

    Read concepts directly from IPLD format

    Use difficulty_levels to adjust explanations

    Follow relationships to provide context

    Reference proofs for credibility

## PART 5: UPDATING CONCEPTS

### 5.1 Important Rule: Immutability

Concepts cannot be changed! Once stored, they're permanent.

### 5.2 How to Update

    Retrieve the existing concept

    Create new version with changes

    Store as new concept (new CID)

    Link versions using relationships

Example:
```json

{
  "human_id": "Physics:Law/ConservationOfEnergy_v2",
  "title": "Law of Conservation of Energy (Revised)",
  // ... other fields with updates
  "metadata": {
    "supersedes": "bafyrei...",  // CID of old version
    "version": 2
  },
  "relationships": {
    "supersedes": ["bafyrei..."]  // CID of old version
  }
}
```

### 5.3 Version Naming Convention

    Keep same human_id base

    Add version suffix: _v2, _v3

    Or date: _20241224

## PART 6: QUALITY CONTROL

### 6.1 Validation Levels

The system checks concepts at different rigor levels:

    BASIC: Has required fields

    STANDARD: (Default) Fields have valid content

    RIGOROUS: Evidence quality checked

    STRICT: Maximum scientific standards

### 6.2 Common Validation Errors

    Missing required fields -> Add missing fields

    Definition too short -> Expand to at least 10 characters

    No proofs -> Add at least one evidence source

    Invalid confidence -> Use 0.0-1.0 scale

    Missing difficulty levels -> Add at least "intermediate"

### 6.3 Quality Checklist Before Storing

    human_id follows Domain:Type/Name format

    title is clear and descriptive

    definition is complete (≥2 sentences)

    type is valid (Concept, Law, Theory, etc.)

    domain and subdomain make sense

    At least one proof with confidence score

    At least difficulty_levels.intermediate exists

    Confidence scores are realistic (0.0-1.0)

    Dates are in YYYY-MM-DD format

## PART 7: SYSTEM STATUS & MAINTENANCE

### 7.1 Checking System Health
```bash

# Check storage
ls -la store/blocks/ | wc -l
du -sh store/

# Check index
cat store/index/human_id_to_cid.json | jq '. | length' 2>/dev/null || \
  python3 -c "import json; print(len(json.load(open('store/index/human_id_to_cid.json'))))"

# View logs
tail -n 5 store/logs/operations_*.jsonl 2>/dev/null || echo "No logs yet"
```

### 7.2 Current Concepts in System

As of 2025-12-24, the system contains:

    Demo concepts (for testing)

    Digital Seed (first real concept)

    Workflow demonstration (system example)

Total: ~6 concepts, ~2.5KB storage

### 7.3 Adding More Concepts

Simply follow the 3-step workflow:

    Mine concepts from your work

    Format them using the template

    Store using the workflow tool

## PART 8: TROUBLESHOOTING

### 8.1 Common Issues

"ModuleNotFoundError: No module named 'multiformats'"
bash

pip3 install --user multiformats dag-cbor

"Validation failed: Missing required field"
Check your concept has all required fields.

"CID generation error"
Make sure all dates are strings (not Python date objects).

"Can't find stored concept"
Check the index: cat store/index/human_id_to_cid.json

### 8.2 Getting Help

    Check documentation: This guide and technical docs

    Look at examples: Existing concepts in the system

    Use validation: Run validator on your concept first

    Start simple: Basic concept first, add complexity later

## PART 9: BEST PRACTICES

### 9.1 Concept Mining Tips

    Capture ideas immediately when they occur

    Use voice memos or quick notes then format later

    Look for patterns across different domains

    Connect new concepts to existing ones

    Record source context for evidence

### 9.2 Formatting Tips

    Be specific in definitions

    Use examples in difficulty levels

    Cite sources in proofs

    Add relationships when possible

    Tag generously for searchability

### 9.3 Storage Tips

    Validate first before storing

    Keep backups of your JSON concepts

    Version important changes

    Link related concepts

    Review periodically for updates

### 9.4 Collaboration Tips

    Share interesting concepts with team

    Use consistent naming conventions

    Reference each other's concepts

    Build on existing work

    Credit sources properly

## PART 10: THE BIGGER PICTURE

### 10.1 Why This System Matters

You're not just "storing information." You're:

    Building a living knowledge graph

    Creating verifiable intellectual assets

    Enabling cross-disciplinary connections

    Supporting lifelong learning

    Preserving ideas with cryptographic certainty

### 10.2 Your Role as Gardener

Think of yourself as tending a mycelial garden:

    You plant seeds (store concepts)

    You nurture connections (add relationships)

    You prune when needed (update/version)

    You harvest insights (retrieve and use)

    You share abundance (collaborate)

### 10.3 The Future Vision

This system will eventually:

    Connect to interactive creation environments

    Integrate with retrieval systems for intelligent access

    Work with AI assistants for natural language interaction

    Support collaboration across teams

    Enable knowledge discovery through AI

GETTING STARTED TODAY
Your First Mission:

    Find one concept from your recent work

    Format it using the template

    Store it using the workflow tool

    Retrieve it to verify storage

    Share it with a colleague

Quick Reference Card:
```text

MINE -> Find concepts in your work
FORMAT -> Use IPLD template (all required fields)
STORE -> python3 tools/ipld_workflow.py
FIND -> Check store/index/human_id_to_cid.json
UPDATE -> Create new version, link to old
```

SUPPORT & RESOURCES

Documentation:

    This User Guide (how to use)

    Technical Documentation (how it works)

    Narrative Documentation (why it matters)

Tools:

    Workflow tool: tools/ipld_workflow_v1.0.0.py

    Validator: tools/scientific_validator_v1.0.0.py

    CID Generator: tools/cid_generator_v1.0.0.py

Location:
```text

/path/to/CADMIES-IPLD/
```

Questions? Check documentation first.

Happy knowledge gardening!

"We are not building machines that think; we are building gardens where thoughts can grow like mycelium, connecting everything in cosmic patterns."

