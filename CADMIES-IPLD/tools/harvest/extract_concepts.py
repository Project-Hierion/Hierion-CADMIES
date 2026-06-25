#!/usr/bin/env python3
"""
File: harvest_full_pipeline.py
Tool: CADMIES Conversation Harvester
Version: 2.0.0
System: CADMIES / tools/harvest
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Chunks a conversation, queries the mycelium for relevant existing
         concepts, and feeds both to Mistral for philosophical concept
         extraction with automatic relationship mapping to the existing
         knowledge graph. Mycelium-aware — searches CADMIES before extracting
         so new concepts are born already linked to the mycelium.

Usage:
    python tools/harvest/harvest_full_pipeline.py

Version History:
  v2.0.0: Mycelium-aware extraction — searches CADMIES before extracting.
  v1.0.0: Initial harvester release.
"""

import json
import sys
import time
from pathlib import Path
import ollama

# === CONFIG ===
CONVERSATION_FILE = Path(__file__).parent / "conversation_01.json"
OUTPUT_FILE = Path(__file__).parent / "harvested_concepts_01.json"
MODEL = "mistral:7b"
CHUNK_SIZE = 3000
DELAY = 2
RELEVANCE_THRESHOLD = 0.1

sys.path.insert(0, str(Path(__file__).parent.parent / "agents" / "code"))
try:
    from cadmies_concept_reader import search_mycelium, load_all_concept_cids, load_concept
    MYCELIUM_AVAILABLE = True
except ImportError:
    MYCELIUM_AVAILABLE = False
    print("WARNING: Could not import mycelium search — running without mycelium awareness")

EXTRACTION_PROMPT = """You are a philosophical concept extractor working with the CADMIES mycelium knowledge system.

Below is a conversation to mine for NEW philosophical concepts, arguments, insights, and principles.

Also provided are RELEVANT EXISTING CONCEPTS already in the mycelium. DO NOT extract these as new concepts. 
They are reference ONLY. Use them to:
- Identify connections between the new concepts you extract and existing ones
- Build richer definitions informed by related concepts
- Place new concepts in the correct philosophical domain

For each NEW concept you discover in the conversation, return a JSON object with these fields:
- "name": A short, descriptive title in snake_case (e.g., "craving_tanha_cycle")
- "definition": A clear 1-3 sentence definition
- "domain": The philosophical domain (e.g., "Philosophy", "Buddhist_Philosophy", "Cognitive_Science")
- "insight": The novel or noteworthy observation made in the conversation
- "builds_upon": List of existing concept human_ids this concept directly extends (use EXACT names from the reference concepts below)
- "related_to": List of existing concept human_ids with meaningful connections
- "contradicts": List of existing concept human_ids or axioms this challenges

Return ONLY a JSON array of concept objects. No other text.

EXISTING MYCELIUM CONCEPTS (reference only — do not extract these):
{mycelium_context}

CONVERSATION TO MINE:
{chunk}"""


def load_conversation_robust(filepath):
    """Load conversation text from JSON, handling unescaped content gracefully."""
    with open(filepath, "r") as f:
        raw_text = f.read().strip()

    try:
        data = json.loads(raw_text)
        return data["content"]
    except json.JSONDecodeError:
        pass

    content_key = '"content":'
    key_pos = raw_text.find(content_key)
    if key_pos == -1:
        raise ValueError("Could not find 'content' key in JSON file")

    value_start = key_pos + len(content_key)
    raw_value = raw_text[value_start:].strip()

    depth = 0
    cut_at = len(raw_value)
    for i, char in enumerate(raw_value):
        if char == '{':
            depth += 1
        elif char == '}':
            if depth == 0:
                cut_at = i
                break
            depth -= 1

    content = raw_value[:cut_at].strip()

    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]

    print("  (used robust loader — unescaped text detected)")
    return content


def get_mycelium_context(conversation_text):
    """Search the mycelium for concepts relevant to this conversation."""
    if not MYCELIUM_AVAILABLE:
        return "Mycelium search unavailable — proceeding without existing concept references."

    print("\n  Searching mycelium for relevant existing concepts...")
    all_cids = load_all_concept_cids()
    results = search_mycelium(conversation_text, all_cids)

    relevant = [r for r in results if r['relevance_score'] >= RELEVANCE_THRESHOLD]

    if not relevant:
        print(f"  No concepts above relevance threshold ({RELEVANCE_THRESHOLD})")
        return "No strongly relevant existing concepts found in the mycelium."

    print(f"  Found {len(relevant)} relevant concepts (threshold: {RELEVANCE_THRESHOLD}):")

    context_parts = []
    for i, r in enumerate(relevant):
        cid = r['cid']
        concept = load_concept(cid)
        if 'error' in concept:
            continue

        human_id = concept.get('human_id', '')
        title = concept.get('title', 'Unknown')
        definition = concept.get('definition', '')[:500]
        domain = concept.get('domain', 'Unknown')

        print(f"    {i+1}. {human_id} [{domain}] (score: {r['relevance_score']:.3f})")

        context_parts.append(f"CONCEPT {i+1}:")
        context_parts.append(f"  human_id: {human_id}")
        context_parts.append(f"  title: {title}")
        context_parts.append(f"  domain: {domain}")
        context_parts.append(f"  definition: {definition}")
        context_parts.append("")

    return "\n".join(context_parts)


def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of roughly chunk_size words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def extract_from_chunk(chunk, mycelium_context, index, total):
    """Send a chunk to Mistral with mycelium context and parse the response."""
    prompt = EXTRACTION_PROMPT.format(
        mycelium_context=mycelium_context,
        chunk=chunk
    )
    print(f"\n  Sending chunk {index + 1}/{total} ({len(chunk.split())} words)...")

    try:
        response = ollama.generate(model=MODEL, prompt=prompt)
        raw = response["response"].strip()

        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:]) if lines[0].startswith("```") else raw
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        concepts = json.loads(raw)
        print(f"  Extracted {len(concepts)} new concepts.")
        return concepts

    except json.JSONDecodeError:
        print(f"  Warning: Could not parse JSON from chunk {index + 1}. Saving raw output.")
        return [{"error": "json_parse_failed", "raw_output": raw}]
    except Exception as e:
        print(f"  Error on chunk {index + 1}: {e}")
        return []


def merge_and_deduplicate(all_concepts):
    """Combine concepts from all chunks, remove duplicates by name."""
    seen = set()
    merged = []
    for chunk_concepts in all_concepts:
        for concept in chunk_concepts:
            name = concept.get("name", "")
            if name and name not in seen:
                seen.add(name)
                merged.append(concept)
    return merged


def main():
    print("=" * 60)
    print("CADMIES CONVERSATION HARVESTER v2.0.0")
    print(f"Model: {MODEL}")
    print(f"Source: {CONVERSATION_FILE}")
    if MYCELIUM_AVAILABLE:
        print("Mycelium search: ENABLED (relevance-gated)")
    else:
        print("Mycelium search: DISABLED")
    print("=" * 60)

    text = load_conversation_robust(CONVERSATION_FILE)
    print(f"\nLoaded conversation: {len(text.split())} words")

    mycelium_context = get_mycelium_context(text)

    chunks = chunk_text(text, CHUNK_SIZE)
    print(f"\nSplit into {len(chunks)} chunk(s) for extraction")

    all_concepts = []
    for i, chunk in enumerate(chunks):
        concepts = extract_from_chunk(chunk, mycelium_context, i, len(chunks))
        all_concepts.append(concepts)
        if i < len(chunks) - 1:
            time.sleep(DELAY)

    merged = merge_and_deduplicate(all_concepts)
    print(f"\n{'='*60}")
    print(f"Total unique NEW concepts extracted: {len(merged)}")

    output = {
        "source_file": str(CONVERSATION_FILE.name),
        "model": MODEL,
        "harvester_version": "2.0.0",
        "mycelium_aware": MYCELIUM_AVAILABLE,
        "concepts": merged
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved to: {OUTPUT_FILE}")

    print("\n=== CONCEPT PREVIEW ===")
    for c in merged:
        name = c.get('name', 'UNNAMED')
        domain = c.get('domain', 'unknown')
        definition = c.get('definition', 'No definition')[:100]
        builds = c.get('builds_upon', [])
        relates = c.get('related_to', [])
        print(f"  • {name} [{domain}]")
        print(f"    {definition}...")
        if builds:
            print(f"    Builds upon: {', '.join(builds[:3])}")
        if relates:
            print(f"    Related to: {', '.join(relates[:3])}")
        print()


if __name__ == "__main__":
    main()
