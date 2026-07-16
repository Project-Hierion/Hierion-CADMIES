# Quick test to verify the fix
import yaml

test = """---
phase: 35
date: 2026-05-14
status: Complete
related: [[Harvester Pipeline]], [[bayes_theorem]], [[Session-006]]
---

# Phase 35: Three-Tier Difficulty Levels"""

# Current broken logic
parts = test.split("---", 2)
print(f"Split parts: {len(parts)}")
for i, p in enumerate(parts):
    print(f"  Part {i}: {repr(p[:50])}")

# Fixed logic
if test.startswith("---"):
    parts = test.split("---", 2)
    if len(parts) >= 3:
        try:
            fm = yaml.safe_load(parts[1])
            print(f"\nParsed OK: {fm}")
        except yaml.YAMLError as e:
            print(f"\nParse error: {e}")
