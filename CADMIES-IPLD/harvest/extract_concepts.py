#!/usr/bin/env python3
"""
Conversation Harvester — Chunks a conversation and feeds it to Mistral
for philosophical concept extraction. Outputs structured JSON for mycelium ingestion.
Handles messy conversation JSON files gracefully.
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
CHUNK_SIZE = 3000  # words per chunk
DELAY = 2  # seconds between API calls to avoid overwhelming Mistral

EXTRACTION_PROMPT = """You are a philosophical concept extractor. Read the conversation below and extract all philosophical concepts, arguments, insights, and principles discussed.

For each distinct concept you find, return a JSON object with these fields:
- "name": A short, descriptive title for the concept (use underscores, like "Craving_Cycle")
- "definition": A clear 1-3 sentence definition
- "domain": The philosophical domain (e.g., "Buddhist_Philosophy", "Ethics", "Cognitive_Science")
- "relations": A list of related concepts mentioned in the text and how they connect (e.g., ["Impermanence:drives", "Suffering:results_from"])
- "insight": The novel or noteworthy observation made in the conversation

Return ONLY a JSON array of concept objects. No other text.

Conversation:
{chunk}"""


def load_conversation_robust(filepath):
    """Load conversation text from JSON, handling unescaped content gracefully."""
    with open(filepath, "r") as f:
        raw_text = f.read().strip()

    # Try standard JSON first
    try:
        data = json.loads(raw_text)
        return data["content"]
    except json.JSONDecodeError:
        pass

    # Fallback: extract everything between first "content": and the final }
    # Find where content value starts
    content_key = '"content":'
    key_pos = raw_text.find(content_key)
    if key_pos == -1:
        raise ValueError("Could not find 'content' key in JSON file")

    # Find the start of the value (skip whitespace and optional opening quote)
    value_start = key_pos + len(content_key)
    raw_value = raw_text[value_start:].strip()

    # Remove surrounding curly braces and trailing brace if present
    # The value is everything from content's value to the last }
    # Find the outermost closing brace that isn't inside the content
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

    # Remove surrounding quotes if present
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]

    print("  (used robust loader — unescaped text detected)")
    return content


def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of roughly chunk_size words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def extract_from_chunk(chunk, index, total):
    """Send a chunk to Mistral and parse the response."""
    prompt = EXTRACTION_PROMPT.format(chunk=chunk)
    print(f"  Sending chunk {index + 1}/{total} ({len(chunk.split())} words)...")

    try:
        response = ollama.generate(model=MODEL, prompt=prompt)
        raw = response["response"].strip()

        # Mistral sometimes wraps in markdown code fences — strip them
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:]) if lines[0].startswith("```") else raw
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        concepts = json.loads(raw)
        print(f"  Got {len(concepts)} concepts.")
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
    print("CADMIES Conversation Harvester")
    print(f"Model: {MODEL}")
    print(f"Source: {CONVERSATION_FILE}")
    print("=" * 60)

    # Load (robust — handles broken JSON)
    text = load_conversation_robust(CONVERSATION_FILE)
    print(f"\nLoaded conversation: {len(text.split())} words")

    # Chunk
    chunks = chunk_text(text, CHUNK_SIZE)
    print(f"Split into {len(chunks)} chunk(s)\n")

    # Extract
    all_concepts = []
    for i, chunk in enumerate(chunks):
        concepts = extract_from_chunk(chunk, i, len(chunks))
        all_concepts.append(concepts)
        if i < len(chunks) - 1:
            time.sleep(DELAY)

    # Merge
    merged = merge_and_deduplicate(all_concepts)
    print(f"\nTotal unique concepts extracted: {len(merged)}")

    # Save
    output = {
        "source_file": str(CONVERSATION_FILE.name),
        "model": MODEL,
        "concepts": merged
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved to: {OUTPUT_FILE}")

    # Preview
    print("\n=== CONCEPT PREVIEW ===")
    for c in merged:
        print(f"  • {c.get('name', 'UNNAMED')} [{c.get('domain', 'unknown')}]")
        print(f"    {c.get('definition', 'No definition')[:100]}...")


if __name__ == "__main__":
    main()