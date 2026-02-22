#!/usr/bin/env python3
"""
Store the Digital Seed concept in IPLD
"""

import json
import dag_cbor
from multiformats import multihash, CID
import hashlib
from datetime import datetime
from pathlib import Path

# Digital Seed in IPLD format
DIGITAL_SEED = {
  "schema_version": "1.0.0",
  "human_id": "Hieros:CoreConcept/DigitalSeed",
  "title": "Digital Seed",
  "definition": "A packaged knowledge unit containing core concepts, relationships, and growth potential. Designed for distribution and collaborative development across research domains. Represents the minimal viable knowledge structure for project propagation.",
  "type": "CoreConcept",
  "domain": "Hieros",
  "subdomain": "Knowledge Distribution",
  "proofs": [
    {
      "type": "core_vision",
      "description": "Project Hieros Core Vision",
      "confidence": 0.7,
      "date": "2024-10-01",
      "reference": "Project Hieros Core Vision"
    }
  ],
  "metadata": {
    "created": datetime.now().isoformat() + "Z",
    "creator": "System:CADMIES_Migration",
    "certainty_score": 0.7,
    "version": 1
  },
  "relationships": {
    "complements": ["Hieros:CoreConcept/HierarchicalOrganicGraph"]
  },
  "difficulty_levels": {
    "intermediate": "A packaged knowledge unit designed for distribution and collaborative development",
    "expert": "Minimal viable knowledge structure for cross-domain project propagation with embedded growth potential"
  }
}

print("Storing Digital Seed Concept")
print("=" * 60)

# Generate CID
cbor_bytes = dag_cbor.encode(DIGITAL_SEED)
digest = hashlib.sha256(cbor_bytes).digest()
mh = multihash.wrap(digest, 'sha2-256')
cid = CID('base32', 1, 'dag-cbor', mh)

print(f"Concept: {DIGITAL_SEED['title']}")
print(f"   ID: {DIGITAL_SEED['human_id']}")
print(f"Generated CID: {cid}")
print(f"Size: {len(cbor_bytes)} bytes")

# Store in blockstore
store = Path("./store")
blocks = store / "blocks"
index_file = store / "index" / "human_id_to_cid.json"

blocks.mkdir(parents=True, exist_ok=True)
index_file.parent.mkdir(parents=True, exist_ok=True)

# Save block
filename = str(cid).replace(':', '_').replace('/', '_')
block_path = blocks / filename
with open(block_path, 'wb') as f:
    f.write(cbor_bytes)
print(f"Stored: {filename}")

# Update index
if index_file.exists():
    with open(index_file, 'r') as f:
        index = json.load(f)
else:
    index = {}

index[DIGITAL_SEED['human_id']] = str(cid)

with open(index_file, 'w') as f:
    json.dump(index, f, indent=2)
print(f"Index updated: {DIGITAL_SEED['human_id']} -> {str(cid)[:16]}...")

# Verify
print(f"\nVerifying storage...")
with open(block_path, 'rb') as f:
    verify_bytes = f.read()
verify_digest = hashlib.sha256(verify_bytes).digest()
verify_mh = multihash.wrap(verify_digest, 'sha2-256')
verify_cid = CID('base32', 1, 'dag-cbor', verify_mh)

if str(verify_cid) == str(cid):
    print(f"Integrity verified: CID matches")
else:
    print(f"Integrity FAILED: CIDs don't match")

print(f"\nDigital Seed is now stored in IPLD!")
print(f"Ready for the mycelial network...")
