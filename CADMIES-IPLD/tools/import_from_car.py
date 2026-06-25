#!/usr/bin/env python3
"""
File: import_from_car.py
Tool: CADMIES CAR Import
Version: 1.2.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Import CADMIES concepts from CAR files into local mycelium.
         Automatic index update on every block save. Preserves provenance
         on CID changes between machines.

Usage:
    python tools/import_from_car.py <file.car>
    python tools/import_from_car.py <file.car> --dry-run
    python tools/import_from_car.py <file.car> --verify-only

Version History:
  v1.2.0 (2026-05-25): Automatic index update on every block save.
  v1.1.0 (2026-05-25): CID change on import now preserves provenance.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from core.car_utils import (
    read_car,
    save_block_to_store,
    load_block_from_store,
    verify_block_integrity,
    calculate_cid
)

PROJECT_ROOT = Path(__file__).parent.parent
BLOCKS_DIR = PROJECT_ROOT / "store" / "blocks"
INDEX_FILE = PROJECT_ROOT / "store" / "index" / "human_id_to_cid.json"


def load_index() -> Dict[str, str]:
    """Load current human_id to CID mapping."""
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)


def save_index(index: Dict[str, str]) -> None:
    """Save human_id to CID mapping."""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)


def update_index_entry(index: Dict[str, str], human_id: str, cid: str) -> bool:
    """Update a single index entry. Returns True if the entry was new or changed."""
    if human_id in index:
        if index[human_id] == cid:
            return False
    index[human_id] = cid
    return True


def get_verification_status_for_import(concept_cid: str):
    """Get verification status for a concept (import-safe)."""
    try:
        sys.path.insert(0, str(Path(__file__).parent / "core"))
        from verification_manager import get_verification_status
        return get_verification_status(concept_cid)
    except Exception as e:
        return {"badge": "❓", "label": f"Error: {e}", "level": 0, "chain_count": 0}


def import_car(car_path: Path, dry_run: bool = False, verbose: bool = False, verify_only: bool = False) -> bool:
    """
    Import a CAR file into the local mycelium.
    
    Automatically updates the index for every saved block, including
    reminted blocks with provenance-preserving CID changes.
    """
    print("=" * 60)
    print("CADMIES CAR IMPORT v1.2.0")
    if dry_run:
        print("** DRY RUN MODE - No changes will be made **")
    if verify_only:
        print("** VERIFY ONLY MODE - Showing verification status only **")
    print("=" * 60)
    
    if not car_path.exists():
        print(f"❌ CAR file not found: {car_path}")
        return False
    
    print(f"📦 Reading CAR file: {car_path}")
    print(f"   File size: {car_path.stat().st_size:,} bytes")
    
    try:
        blocks, roots = read_car(car_path)
        print(f"✅ Read {len(blocks)} block(s) from CAR")
        print(f"   Root CID(s): {roots}")
    except Exception as e:
        print(f"❌ Failed to read CAR file: {e}")
        return False
    
    current_index = load_index()
    index_modified = False
    index_updates = 0
    
    print("\n" + "-" * 40)
    print("Processing blocks...")
    print("-" * 40)
    
    stats = {
        "total_blocks": len(blocks),
        "new_blocks": 0,
        "existing_blocks": 0,
        "invalid_blocks": 0,
        "reminted_blocks": 0,
        "index_updated": 0
    }
    
    verification_blocks = []
    index_blocks = {}
    concept_blocks = {}
    
    for cid_str, block_data in blocks.items():
        try:
            decoded = json.loads(block_data.decode('utf-8'))
            if all(isinstance(v, str) and (v.startswith('bafy') or v.startswith('Qm')) for v in decoded.values()):
                index_blocks[cid_str] = decoded
                if verbose:
                    print(f"   📑 Found legacy index block: {cid_str[:16]}... ({len(decoded)} entries)")
                continue
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        
        try:
            import dag_cbor
            decoded = dag_cbor.decode(block_data)
            if decoded.get('record_type') == 'verification':
                verification_blocks.append({
                    "cid": cid_str,
                    "data": block_data,
                    "concept_cid": decoded.get('concept_cid'),
                    "source": decoded.get('source'),
                    "verifier": decoded.get('verifier_key')
                })
                if verbose:
                    print(f"   🔐 Found verification block for concept: {decoded.get('concept_cid', 'unknown')[:16]}...")
                continue
        except (ValueError, TypeError, ImportError):
            pass
        
        concept_blocks[cid_str] = block_data
    
    if verify_only:
        print("\n" + "-" * 40)
        print("VERIFICATION STATUS (VERIFY ONLY MODE)")
        print("-" * 40)
        
        if verification_blocks:
            print(f"\n🔐 Found {len(verification_blocks)} verification block(s) in CAR:")
            for vb in verification_blocks:
                print(f"\n   Verification CID: {vb['cid'][:16]}...")
                print(f"   Concept CID: {vb['concept_cid']}")
                print(f"   Source: {vb['source']}")
                print(f"   Verifier: {vb['verifier']}")
                
                concept_exists = (BLOCKS_DIR / f"{vb['concept_cid']}.cbor").exists()
                if concept_exists:
                    status = get_verification_status_for_import(vb['concept_cid'])
                    print(f"   Current badge: {status['badge']} ({status['label']})")
                    print(f"   Would upgrade to: {status['badge'] if status['chain_count'] > 0 else '🟢 (would add)'}")
                else:
                    print(f"   ⚠️ Concept not found locally - import concept first to see badge")
        else:
            print("\n   No verification blocks found in this CAR file.")
        
        print("\n⚠️  VERIFY ONLY MODE - No changes were made.")
        print("   Run without --verify-only to import and apply verifications.")
        return True
    
    if not dry_run:
        print(f"\n📦 Saving {len(concept_blocks)} concept/provenance block(s)...")
    
    for cid_str, block_data in concept_blocks.items():
        if cid_str.startswith('Qm'):
            if verbose:
                print(f"   🔓 Skipping integrity check for CIDv0: {cid_str[:16]}...")
            integrity_ok = True
        else:
            integrity_ok = verify_block_integrity(block_data, cid_str)
        
        if not integrity_ok:
            import dag_cbor
            decoded = dag_cbor.decode(block_data)
            normalized = dag_cbor.encode(decoded)
            
            if not dry_run:
                if 'extra_fields' not in decoded:
                    decoded['extra_fields'] = {}
                decoded['extra_fields']['original_car_cid'] = cid_str
                decoded['extra_fields']['import_date'] = datetime.now(timezone.utc).isoformat()
                enriched = dag_cbor.encode(decoded)
                final_cid = calculate_cid(enriched)
                success = save_block_to_store(final_cid, enriched, BLOCKS_DIR)
                
                if success:
                    print(f"   🔄 Reminted: {cid_str[:16]}... → {final_cid[:16]}... (provenance preserved)")
                    stats["new_blocks"] += 1
                    stats["reminted_blocks"] += 1
                    
                    human_id = decoded.get('human_id')
                    if human_id:
                        if update_index_entry(current_index, human_id, final_cid):
                            index_updates += 1
                            index_modified = True
                            if verbose:
                                print(f"      📑 Index updated: {human_id} → {final_cid[:16]}...")
                else:
                    print(f"   ❌ Failed to save: {cid_str[:16]}...")
                    stats["invalid_blocks"] += 1
            else:
                print(f"   [DRY RUN] Would re-mint with provenance: {cid_str[:16]}...")
                stats["new_blocks"] += 1
                stats["reminted_blocks"] += 1
            continue
        
        existing = load_block_from_store(cid_str, BLOCKS_DIR)
        if existing is not None:
            if verbose:
                print(f"   ⏭️  Already exists: {cid_str[:16]}...")
            stats["existing_blocks"] += 1
            
            try:
                import dag_cbor
                decoded = dag_cbor.decode(block_data)
                human_id = decoded.get('human_id')
                if human_id and update_index_entry(current_index, human_id, cid_str):
                    index_updates += 1
                    index_modified = True
                    if verbose:
                        print(f"      📑 Index updated: {human_id} → {cid_str[:16]}...")
            except (ValueError, TypeError):
                pass
            continue
        
        if not dry_run:
            success = save_block_to_store(cid_str, block_data, BLOCKS_DIR)
            if success:
                print(f"   ✅ Saved: {cid_str[:16]}... ({len(block_data)} bytes)")
                stats["new_blocks"] += 1
                
                try:
                    import dag_cbor
                    decoded = dag_cbor.decode(block_data)
                    human_id = decoded.get('human_id')
                    if human_id and update_index_entry(current_index, human_id, cid_str):
                        index_updates += 1
                        index_modified = True
                        if verbose:
                            print(f"      📑 Index updated: {human_id} → {cid_str[:16]}...")
                except (ValueError, TypeError):
                    pass
            else:
                print(f"   ❌ Failed to save: {cid_str[:16]}...")
                stats["invalid_blocks"] += 1
        else:
            print(f"   [DRY RUN] Would save: {cid_str[:16]}...")
            stats["new_blocks"] += 1
    
    if not dry_run and index_blocks:
        print(f"\n📑 Processing legacy index entries...")
        for idx_cid, index_data in index_blocks.items():
            for human_id, cid in index_data.items():
                if update_index_entry(current_index, human_id, cid):
                    index_updates += 1
                    index_modified = True
                    if verbose:
                        print(f"   ✅ Index: {human_id} → {cid[:16]}...")
    
    if index_modified and not dry_run:
        save_index(current_index)
        print(f"\n💾 Index saved with {index_updates} update(s)")
    elif index_modified and dry_run:
        print(f"\n[DRY RUN] Would update index with {index_updates} entry(s)")
    else:
        print(f"\n📑 Index unchanged (all entries already current)")
    
    if not dry_run and verification_blocks:
        print("\n" + "-" * 40)
        print("🔐 VERIFICATION BLOCKS DETECTED")
        print("-" * 40)
        
        for vb in verification_blocks:
            concept_cid = vb['concept_cid']
            if concept_cid:
                concept_exists = (BLOCKS_DIR / f"{concept_cid}.cbor").exists()
                if concept_exists:
                    status = get_verification_status_for_import(concept_cid)
                    print(f"\n   Concept: {concept_cid[:16]}...")
                    print(f"   Verification source: {vb['source']}")
                    print(f"   New badge: {status['badge']} ({status['label']})")
                    print(f"   Total verifications: {status['chain_count']}")
                else:
                    print(f"\n   ⚠️ Verification block for {concept_cid[:16]}... but concept not found")
                    print(f"      Import the concept block first, then re-import this CAR")
    
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"📦 Total blocks in CAR:    {stats['total_blocks']}")
    print(f"✅ New blocks saved:       {stats['new_blocks']}")
    print(f"🔄   Reminted on import:    {stats['reminted_blocks']}")
    print(f"⏭️  Already existed:        {stats['existing_blocks']}")
    print(f"❌ Invalid blocks:         {stats['invalid_blocks']}")
    print(f"📑 Index entries updated:  {index_updates}")
    print(f"🔐 Verification blocks:    {len(verification_blocks)}")
    print("=" * 60)
    
    if dry_run:
        print("\n⚠️  This was a DRY RUN. No changes were made.")
        print("   Run without --dry-run to actually import.")
    
    return stats["invalid_blocks"] == 0


def main():
    parser = argparse.ArgumentParser(
        description="CADMIES CAR Import v1.2.0",
        epilog="""
Examples:
  import_from_car.py cadmies_latest.car
  import_from_car.py my_export.car --dry-run
  import_from_car.py concept.car --verbose
  import_from_car.py verification.car --verify-only
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('car_file', help='Path to CAR file to import')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Preview import without making changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--verify-only', action='store_true', help='Show verification status from CAR without importing blocks')
    
    args = parser.parse_args()
    
    success = import_car(
        car_path=Path(args.car_file),
        dry_run=args.dry_run,
        verbose=args.verbose,
        verify_only=args.verify_only
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
