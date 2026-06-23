---
system: CADMIES
date: 2026-06-23
status: Active
related: [[Three-Model Arsenal]], [[Two-System Setup]], [[Workflows-Pipeline]]
---

# Architecture Overview

## What Is CADMIES?

CADMIES is a decentralized knowledge graph. It takes conversations — human
dialogues about science, philosophy, consciousness, everything — and extracts
the concepts within them. Those concepts are validated, given permanent
identifiers, and connected to each other through relationships. The result
is a living map of ideas that grows over time.

The name stands for Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem.
The mycelium metaphor is deliberate: concepts are like fungi, connected
underground by threads (relationships) that share nutrients (insights)
across domains. What looks like separate ideas above ground is actually
one interconnected network.

## How It Works (The Short Version)

1. A conversation happens. It gets saved as text.
2. The Harvester reads the text and asks an AI model (Mistral) to identify
   the concepts being discussed.
3. Each concept gets validated against a scientific schema — it needs a
   definition, a domain, and supporting evidence.
4. Valid concepts are "minted" into the blockstore — a permanent, content-addressed
   storage system. Each concept gets a unique fingerprint (CID) based on its
   content. Change one word, the fingerprint changes. This means concepts
   are immutable and verifiable.
5. The Relationship Generator finds connections between concepts — does
   Concept A build upon Concept B? Do they contradict? Are they related?
6. The Mycelium Map visualizes everything as an interactive graph. Nodes are
   concepts. Edges are relationships. Users can click, zoom, filter by domain,
   and explore how ideas connect across disciplines.
7. The Public Gateway makes all concepts browsable as cards, organized by
   domain, freely accessible to anyone.

## The Three Machines

CADMIES runs across three environments, each doing what it's best at:

**Development Machine (Local)**
A personal computer. This is where code is written, concepts are reviewed,
and the mycelium is tended by hand. It holds the master copy of the
blockstore and the Scientific Obsidian vault. It can run lightweight
operations but is not used for heavy AI inference.

**GPU Compute Instance (Cloud)**
A cloud-based machine with a powerful graphics card (GPU). AI models need
GPUs to run efficiently — without one, generating concepts takes minutes
instead of seconds. This machine runs the Harvester, the Relationship
Generator, and hosts the AI models (Mistral, Codestral, Dr. Mistral).

**Public Server (Cloud)**
A web server that hosts the CADMIES website, the mycelium map, the public
gateway, and (eventually) the Dr. Mistral chat interface. It serves static
files to visitors and handles API requests. It does not run AI models —
those stay on the GPU machine. It talks to the GPU machine behind the scenes
when it needs AI inference.

## The Four Models

CADMIES uses four AI models, each with a different role:

- **TinyLlama (1.1B parameters):** The smallest and fastest. Runs on the
  development machine for quick searches and lightweight tasks.
- **Mistral (7B parameters):** The workhorse. Extracts concepts from
  conversations. Runs on the GPU machine.
- **Codestral (22B parameters):** The deep thinker. Finds subtle relationships
  between concepts that simpler models miss. Also runs on the GPU machine.
- **Dr. Amanda Mistral (fine-tuned):** The librarian. Trained specifically
  on CADMIES knowledge — all 636 concepts, the canon, the character lore.
  She answers questions about the mycelium in her own voice. A custom
  version of Mistral 7B.

## The Data Layer

**Blockstore**
The permanent home for concepts. Each concept is stored as a CBOR block
with a content-addressed identifier (CID). If you have the CID, you can
verify the concept hasn't been tampered with — the CID IS the hash of
the content. The blockstore lives in a directory called `store/blocks/`.

**Index**
A lookup table that maps human-readable concept names (like "emergence" or
"bayes_theorem") to their CIDs. Without the index, you'd need to know the
CID to find anything. Lives at `store/index/`.

**Source Concepts**
The JSON files that concepts are created from, before they're minted into
the blockstore. These are human-readable and editable. After editing, a
concept can be "reminted" — given a new CID reflecting its updated content.

**CAR Files**
Content-Addressable Archive files. A way to bundle up multiple concepts
(blocks + index entries) into a single file for sharing, backup, or transfer
between machines. Think of them as ZIP files for the knowledge graph.

## The Tools

**Harvester:** Feeds conversation text to Mistral, extracts concepts, validates
them, and saves them as source concept files ready for minting.

**Relationship Generator:** Takes existing concepts and asks Codestral or
Mistral to find connections between them. Outputs edges (builds_upon,
related_to, specializes, contradicts).

**Mycelium Map Generator:** Reads the blockstore and generates an interactive
HTML visualization — a force-directed graph where nodes are concepts and
edges are relationships. Supports zoom, pan, click-to-highlight, and
domain filtering.

**Public Gateway Generator:** Creates a browsable card-based view of all
concepts, organized by domain. Each card shows the concept name, definition,
and related concepts.

**CID Generator:** Mints a source concept into the blockstore — creates the
CBOR block, generates the CID, updates the index, and records provenance.

## The Vault

Scientific Obsidian is the documentation system. It contains:
- Session notes (the lab notebook — what happened, when)
- Polished documentation (PhD-ready explanations of phases and systems)
- The CADMIES Canon (character lore, naming conventions, foundational metaphors)
- How-to guides and protocols

The vault is a graph too — notes link to other notes, phases, and concepts,
mirroring the mycelium it documents.

## The Flow

Conversation → Harvester → Source Concepts → CID Generator → Blockstore  
│  
Relationship Generator │  
│  
Mycelium Map ← Blockstore + Index ←───┘  
│  
Public Gateway


## Design Principles

**Content addressing over location addressing.** Concepts are found by what
they contain, not where they're stored. This means concepts can be shared,
copied, and verified across machines without trusting the carrier.

**Immutable history.** When a concept is updated, the old version is not
deleted. The new version gets a new CID. The index updates to point to the
newest version. Provenance is preserved.

**The hyphen is a handshake.** CADMIES-Mistral, CADMIES-IPLD, CADMIES-Codestral.
The hyphen acknowledges partnership. CADMIES does not absorb the tools it
uses — it connects with them.

**Local first, cloud for power.** The development machine is the source of
truth. The GPU machine provides compute. The public server provides access.
No single machine is irreplaceable.

**Privacy by design.** The public gateway shares knowledge, not personal
information. No names beyond first initial. No emails. No IP addresses.
The mycelium is about ideas, not identities.