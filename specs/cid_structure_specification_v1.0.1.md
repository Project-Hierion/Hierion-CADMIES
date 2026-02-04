---
System: CADMIES - Hierarchical Ontological Graph (HOG)
Document_ID: SPEC-2026-004-CID-STRUCTURE
Version: 1.0.1
Classification: PUBLIC
Author: CADMIES Project Contributors
Reviewers: [Technical Team]
Status: PUBLISHED
Created: 2026-02-03
Modified: 2026-02-03
Related_Docs:
  - schemas/universal_scientific_concept_schema_v1.0.0.json
  - cid_generator_v1_1_0.py
  - cbor_reader.py
  - LICENSE (AGPLv3 with Commons Clause)
NASA_Note: CID structure adheres to NASA standards for unambiguous identification
Ethical_Framework: AGPLv3 with Commons Clause - Knowledge sharing over commercial exploitation
---

# CADMIES CID Structure Specification v1.0.1
## Content Identifier Format for Hierarchical Ontological Graph (HOG)

### Document Control
| Field | Value |
|-------|-------|
| **System** | CADMIES (Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem) |
| **Subsystem** | Hierarchical Ontological Graph (HOG) |
| **Specification Type** | Data Structure Definition |
| **Effective Date** | 2026-02-03 |
| **Supersedes** | None (Initial Release) |
| **Applicability** | All HOG concept entries, RAG system, IPLD blocks |
| **Reference Implementation** | `cid_generator_v1_1_0.py` |
| **License** | AGPLv3 with Commons Clause |

---

## 1.0 PURPOSE AND SCOPE

### 1.1 Purpose

This document defines the standard Content Identifier (CID) structure for concepts within the Hierarchical Ontological Graph (HOG). The CID serves as the unique, permanent identifier for each knowledge unit in the CADMIES ecosystem.

### 1.2 Scope

Applies to all concept entries in HOG format, IPLD block generation, RAG system indexing, and any system that references CADMIES concepts.

### 1.3 Principles

- **Uniqueness**: Each distinct concept has a unique CID
- **Permanence**: CIDs are immutable; changes create new CIDs
- **Human-Readable**: CIDs follow predictable, understandable patterns
- **Machine-Parsable**: Structured for automated processing
- **Hierarchical**: Reflects domain/type relationships
- **Ethical**: All CIDs should reference ethically-sourced knowledge (educational/research focus per AGPLv3+Commons Clause)

---

## 2.0 CID STRUCTURE DEFINITION

### 2.1 Formal Syntax

Domain:Type/ConceptName
text


### 2.2 Component Specifications

#### 2.2.1 Domain Component

**Purpose**: Primary knowledge domain classification

**Format**: `[A-Z][a-z]*` (CamelCase, no spaces)

**Allowed Values**:
- `Physics`
- `Philosophy` 
- `CognitiveScience`
- `Spirituality`
- `Mathematics`
- `ComputerScience`
- `Biology`
- `Metaphysics`
- `Epistemology`
- `Methodology`
- `Hieros` (System-specific concepts)
- `CADMIES` (Project/ecosystem concepts)

#### 2.2.2 Type Component

**Purpose**: Classification of concept nature

**Format**: `[A-Z][a-z]*` (CamelCase, no spaces)

**Allowed Values**:
- `Principle` (Fundamental truth/law)
- `Concept` (Abstract idea/mental construct)
- `Method` (Procedure/approach)
- `System` (Organized set of components)
- `Pattern` (Recurring structure/arrangement)
- `Law` (Scientific/mathematical law)
- `Theorem` (Mathematically proven statement)
- `Framework` (Structural/analytical framework)
- `Analogy` (Cross-domain comparison)
- `Model` (Representational/descriptive model)

#### 2.2.3 ConceptName Component

**Purpose**: Unique identifier within Domain:Type namespace

**Format**: `[A-Z][a-zA-Z0-9]*` (CamelCase, no spaces, underscores, or special characters)

**Rules**:
- Start with capital letter
- Use CamelCase for multi-word names
- No spaces, underscores, or special characters
- Should be descriptive but concise
- Must be unique within its Domain:Type combination

**Examples**:
- `InformationIsPhysical`
- `NonDualReality`
- `ConsciousnessAsCosmicFeedback`

### 2.3 Complete CID Examples

#### 2.3.1 Valid Examples

Physics:Law/ConservationOfEnergy
Philosophy:Concept/NonDualReality
CognitiveScience:Model/AssociativeMindLLMAnalogy
Metaphysics:Principle/FractalReality
Methodology:Method/CrossDomainMetaphorMapping
text


#### 2.3.2 Invalid Examples (with reasons)

physics:principle/information_is_physical # Lowercase domain, underscores
Philosophy:concept/Non-Dual-Reality # Lowercase type, hyphens
Cognitive Science:Model/AssociativeMind # Space in domain
Philosophy:Concept/ # Missing concept name
:Principle/InformationIsPhysical # Missing domain
Physics:Info/InformationIsPhysical # Invalid type "Info"
text


---

## 3.0 RELATIONSHIP TO SYSTEM TOOLS

### 3.1 CID Generator Integration

The `cid_generator_v1_1_0.py` tool:
- Validates CID format during concept processing
- Generates IPLD CIDs using DAG-CBOR + SHA2-256
- Maintains human-readable indexes

### 3.2 JSON Schema Integration

The `schemas/universal_scientific_concept_schema_v1.0.0.json` expects CIDs in the `human_id` field.

### 3.3 CBOR Reader Integration

The `cbor_reader.py` tool retrieves concepts using either:
- **CID**: Content-addressed identifier
- **Human ID**: `Domain:Type/ConceptName` format

---

## 4.0 VALIDATION RULES

### 4.1 Syntax Validation

A valid CID must:
1. Match regex: `^[A-Z][a-z]+:[A-Z][a-z]+/[A-Z][a-zA-Z0-9]+$`
2. Use allowed domain from list
3. Use allowed type from list
4. Follow CamelCase for ConceptName

### 4.2 Implementation

The reference implementation validates these rules in `cid_generator_v1_1_0.py`.

---

## 5.0 EXAMPLES

### 5.1 Educational Examples

Physics:Law/ConservationOfEnergy
Philosophy:Concept/NonDualReality
Mathematics:Theorem/PythagoreanTheorem
ComputerScience:Algorithm/DijkstraAlgorithm
Biology:Principle/EvolutionByNaturalSelection
text


### 5.2 Project Examples

CADMIES:Framework/DigitalMycorrhizalIntelligence
Hieros:System/HOGFramework
Methodology:Method/CrossDomainMetaphorMapping
text


---

## 6.0 IMPLEMENTATION GUIDELINES

### 6.1 Creating New CIDs

1. Select domain from allowed list
2. Select type from allowed list
3. Create descriptive ConceptName (CamelCase)
4. Validate format
5. Use `cid_generator_v1_1_0.py` for CID generation

### 6.2 Ethical Implementation

All concepts should:
- Include educational/research purpose
- Respect source attribution
- Align with AGPLv3+Commons Clause
- Contribute to knowledge sharing

---

## 7.0 APPENDICES

### Appendix A: Domain Reference

| Domain | Description | Example |
|--------|-------------|---------|
| Physics | Physical laws, principles | `Physics:Law/ConservationOfEnergy` |
| Philosophy | Philosophical concepts | `Philosophy:Concept/NonDualReality` |
| CognitiveScience | Mind, consciousness studies | `CognitiveScience:Model/GlobalWorkspace` |
| Spirituality | Spiritual frameworks | `Spirituality:Framework/NonDualAwareness` |
| Mathematics | Mathematical concepts | `Mathematics:Theorem/PythagoreanTheorem` |
| ComputerScience | Computing concepts | `ComputerScience:Algorithm/DijkstraAlgorithm` |
| Biology | Biological principles | `Biology:Principle/EvolutionByNaturalSelection` |
| Metaphysics | Metaphysical concepts | `Metaphysics:Principle/FractalReality` |
| Epistemology | Knowledge theory | `Epistemology:Method/ScientificMethod` |
| Methodology | Methods, techniques | `Methodology:Method/FirstPrinciplesThinking` |
| Hieros | System-specific concepts | `Hieros:System/HOGFramework` |
| CADMIES | Project concepts | `CADMIES:Framework/DigitalMycorrhizalIntelligence` |

### Appendix B: Type Reference  

| Type | When to Use | Example |
|------|-------------|---------|
| Principle | Fundamental truth | `Physics:Principle/InformationIsPhysical` |
| Concept | Abstract idea | `Philosophy:Concept/NonDualReality` |
| Method | Procedure, approach | `Methodology:Method/CrossDomainMapping` |
| System | Organized components | `ComputerScience:System/OperatingSystem` |
| Pattern | Recurring structure | `Biology:Pattern/FibonacciSequence` |
| Law | Scientific law | `Physics:Law/ConservationOfEnergy` |
| Theorem | Mathematical proof | `Mathematics:Theorem/PythagoreanTheorem` |
| Framework | Analytical structure | `Spirituality:Framework/NonDualAwareness` |
| Analogy | Cross-domain comparison | `CognitiveScience:Analogy/ComputerBrainAnalogy` |
| Model | Descriptive model | `CognitiveScience:Model/GlobalWorkspaceTheory` |

---

## 8.0 RELATED DOCUMENTS

1. **`schemas/universal_scientific_concept_schema_v1.0.0.json`** - JSON Schema
2. **`cid_generator_v1_1_0.py`** - CID generation tool
3. **`cbor_reader.py`** - Concept retrieval tool
4. **`LICENSE`** - AGPLv3 with Commons Clause

---

*End of CADMIES CID Structure Specification v1.0.1*

**Document Status:** PUBLISHED  
**Reference Implementation:** `cid_generator_v1_1_0.py`  
**Educational Focus:** Content addressing for knowledge sharing  
**License:** AGPLv3 with Commons Clause
