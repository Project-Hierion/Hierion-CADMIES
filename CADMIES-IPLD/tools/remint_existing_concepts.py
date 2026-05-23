#!/usr/bin/env python3
"""
File: remint_existing_concepts.py
Tool: CADMIES Concept Reminter
Version: 2.0.0
System: CADMIES
Status: ACTIVE — Session 019 / Phase 43

Purpose: Remints existing concepts whose block content has changed since
         original minting (e.g., relationships added, metadata updated).
         Computes the correct CID from current content, saves under new
         filename, removes old file, and updates the index.
         
         Originally built for Phase 29 library normalization (human_id renames).
         Updated in Phase 43/50C to handle stale CIDs from content modifications.

Usage:
    python tools/remint_existing_concepts.py                 # Dry run — preview stale blocks
    python tools/remint_existing_concepts.py --apply         # Re-mint all stale blocks
    python tools/remint_existing_concepts.py --concept entropy  # Check single concept
    python tools/remint_existing_concepts.py --concept entropy --apply  # Re-mint single
"""

import json, sys, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR, INDEX_FILE
from cid_generator import CIDGenerator
from provenance_manager import ProvenanceManager
import dag_cbor

cid_gen = CIDGenerator()
pm = ProvenanceManager()
now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def compute_current_cid(concept: dict) -> str:
    """Compute the correct CID for a concept dict from its current content.
    Uses the same method as cid_generator.py: dag_cbor.encode → sha256 → multihash.wrap → CID."""
    serialized = dag_cbor.encode(concept)
    hash_bytes = hashlib.sha256(serialized).digest()
    from multiformats import multihash, CID
    mh = multihash.wrap(hash_bytes, "sha2-256")
    return str(CID("base32", 1, "dag-cbor", mh))


def main():
    apply = "--apply" in sys.argv
    target = None
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--concept="):
            target = arg.split("=", 1)[1]
        elif arg == "--concept" and i + 1 < len(sys.argv):
            target = sys.argv[i + 1]

    mode = "APPLY" if apply else "DRY RUN"
    scope = f"concept '{target}'" if target else "ALL concepts"
    print(f"=== CADMIES Concept Reminter v2.0.0 — {mode} ===")
    print(f"Scope: {scope}")
    print(f"Blockstore: {BLOCKS_DIR}\n")

    # Load index
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)

    # Build work list
    if target:
        if target not in index:
            print(f"❌ Concept '{target}' not found in index.")
            sys.exit(1)
        work_list = {target: index[target]}
    else:
        work_list = dict(index)

    # Scan each concept
    stale_count = 0
    clean_count = 0
    missing_count = 0
    reminted = 0

    for human_id, old_cid in sorted(work_list.items()):
        # Load concept
        concept = load_concept(old_cid)
        if 'error' in concept:
            print(f"  ⚠️  {human_id}: cannot load (CID: {old_cid[:20]}...) — {concept['error']}")
            missing_count += 1
            continue

        # Compute correct CID from current content
        new_cid = compute_current_cid(concept)

        if new_cid == old_cid:
            clean_count += 1
            continue

        stale_count += 1
        print(f"  🔄 {human_id}")
        print(f"     Old CID: {old_cid}")
        print(f"     New CID: {new_cid}")

        if not apply:
            continue

        # === APPLY: re-mint the block ===

        # Update metadata
        concept['metadata']['supersedes'] = concept['metadata'].get('supersedes', old_cid)
        concept['metadata']['version'] = concept['metadata'].get('version', 1) + 1

        # Save under new CID
        new_path = BLOCKS_DIR / f"{new_cid}.cbor"
        serialized = dag_cbor.encode(concept)
        with open(new_path, 'wb') as f:
            f.write(serialized)

        # Create provenance record
        try:
            pm.create_provenance_record(
                concept_cid=new_cid,
                author="CADMIES Remint Script v2.0.0 (Session 019)",
                record_type="supersedes",
                comment=f"Re-minted due to content change. Old CID: {old_cid}"
            )
        except Exception as e:
            print(f"     ⚠️  Provenance failed: {e}")

        # Remove old file
        old_path = BLOCKS_DIR / f"{old_cid}.cbor"
        if not old_path.exists():
            old_path = BLOCKS_DIR / old_cid
        if old_path.exists():
            old_path.unlink()

        # Update index
        index[human_id] = new_cid

        reminted += 1
        print(f"     ✅ Re-minted. Old file removed. Index updated.")

    # Save index if changes were made
    if apply and reminted > 0:
        # Backup index first
        backup_dir = INDEX_FILE.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_name = f"human_id_to_cid.json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(INDEX_FILE, backup_dir / backup_name)

        with open(INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)
        print(f"\n💾 Index saved with {reminted} updated entries.")
        print(f"   Backup: {backup_name}")

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Clean (CID matches):    {clean_count}")
    print(f"  Stale (needs remint):   {stale_count}")
    print(f"  Missing (load failed):  {missing_count}")
    if apply:
        print(f"  Re-minted this run:     {reminted}")
    else:
        print(f"\n  DRY RUN — add --apply to re-mint {stale_count} stale blocks.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()