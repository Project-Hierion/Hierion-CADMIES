#!/usr/bin/env python3
"""
File: normalize_concept_schema.py
CLI: CADMIES Schema Normalizer
Version: 1.0.0
System: CADMIES
Status: ACTIVE
Purpose: Normalizes all source_concept JSONs to a unified superset schema.
         Preserves ALL existing data. Adds missing fields as null/empty.
         No LLM. No blockstore changes. Local-only.

Version History:
  1.0.0 — Initial normalizer: merge all fields, add missing, preserve everything
"""

import json
from pathlib import Path
from collections import OrderedDict

# === PATH SETUP ===
PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_CONCEPTS_DIR = PROJECT_ROOT / "source_concepts"

# === TARGET SCHEMA (superset of all known fields) ===

TARGET_SCHEMA = OrderedDict([
    ("schema_version", "1.0.0"),
    ("human_id", ""),
    ("title", ""),
    ("definition", ""),
    ("type", "Concept"),
    ("domain", "Unknown"),
    ("subdomain", ""),
    ("formula", None),  # Only for math/physics concepts, null otherwise
    ("proofs", [
        {
            "type": "",
            "description": "",
            "confidence": 0.8,
            "date": "",
            "reference": ""
        }
    ]),
    ("metadata", OrderedDict([
        ("created", ""),
        ("creator", ""),
        ("certainty_score", 0.8),
        ("version", 1),
        ("license", "CC BY-SA 4.0"),
        ("purpose", "educational"),
        ("supersedes", None),
        ("superseded_by", None)
    ])),
    ("relationships", OrderedDict([
        ("builds_upon", []),
        ("contradicts", []),
        ("related_to", []),
        ("specializes", [])
    ])),
    ("difficulty_levels", OrderedDict([
        ("beginner", ""),
        ("intermediate", ""),
        ("expert", "")
    ])),
    ("learning_path", OrderedDict([
        ("prerequisites", []),
        ("next_steps", [])
    ])),
    ("cross_references", {}),
    ("extra_fields", OrderedDict([
        ("insight", ""),
        ("source_chunk", None),
        ("origin_file", ""),
        ("harvester_version", ""),
        ("discoverer", "Unknown"),
        ("discovery_year", None),
        ("historical_context", ""),
        ("limitations", []),
        ("applications", []),
        ("key_references", []),
        ("poetic_versions", []),
        ("mantras", [])
    ]))
])


def deep_merge(target, source):
    """Recursively merge source into target. Preserves target structure, adds source data."""
    if isinstance(target, dict) and isinstance(source, dict):
        result = OrderedDict()
        # Keep all target keys
        for key, default_value in target.items():
            if key in source:
                result[key] = deep_merge(default_value, source[key])
            else:
                result[key] = default_value
        # Add any source keys not in target
        for key, value in source.items():
            if key not in result:
                result[key] = value
        return result
    elif isinstance(target, list) and isinstance(source, list):
        # For lists, if target has a template and source has items, use source
        if source:
            return source
        return target
    else:
        # For scalar values, use source if it exists and is not empty, else target default
        if source is not None and source != "" and source != []:
            return source
        return target


def normalize_concept(concept):
    """Normalize a single concept to the target schema, preserving all data."""
    # Start with target schema as template
    normalized = json.loads(json.dumps(TARGET_SCHEMA))  # Deep copy
    
    # Merge existing data on top
    normalized = deep_merge(normalized, concept)
    
    # Ensure human_id matches filename convention
    if not normalized.get("human_id"):
        normalized["human_id"] = normalized.get("title", "unknown").lower().replace(" ", "_")
    
    # Ensure metadata.created exists if not set
    if not normalized["metadata"]["created"]:
        from datetime import datetime, timezone
        normalized["metadata"]["created"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    return normalized


def main():
    print("=" * 60)
    print("CADMIES SCHEMA NORMALIZER v1.0.0")
    print("=" * 60)
    
    if not SOURCE_CONCEPTS_DIR.exists():
        print(f"Source concepts directory not found: {SOURCE_CONCEPTS_DIR}")
        return
    
    json_files = sorted(SOURCE_CONCEPTS_DIR.glob("*.json"))
    print(f"\nFound {len(json_files)} concept(s)")
    
    for jf in json_files:
        try:
            with open(jf, "r") as f:
                concept = json.load(f)
            
            original_human_id = concept.get("human_id", jf.stem)
            normalized = normalize_concept(concept)
            
            # Write back
            with open(jf, "w") as f:
                json.dump(normalized, f, indent=2)
            
            print(f"  ✅ {original_human_id}")
            
        except Exception as e:
            print(f"  ❌ {jf.name}: {e}")
    
    print(f"\nDone. All concepts normalized to unified schema.")
    print("Review changes with: git diff source_concepts/")


if __name__ == "__main__":
    main()