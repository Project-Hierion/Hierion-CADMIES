#!/usr/bin/env python3
"""
Import from CAR v1.1.0
Purpose: Import CADMIES concepts from CAR files into local mycelium
Usage: python tools/import_from_car.py <file.car>

v1.1.0 (2026-05-25): CID change on import now preserves provenance.
  When a block's CID doesn't match locally (encoding differences between
  machines), the block is re-encoded and saved under its new CID with
  original_car_cid and import_cid preserved in extra_fields.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Tuple
from datetime import datetime, timezone

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from core.car_utils import (
    read_car,
    save_block_to_store,
    load_block_from_store,
    verify_block_integrity,
    calculate_cid
)

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
BLOCKS_DIR = PROJECT_ROOT / "store" / "blocks"
INDEX_FILE = PROJECT_ROOT / "store" / "index" / "human_id_to_cid.json"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

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


def merge_index_entry(index: Dict[str, str], human_id: str, cid: str, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Merge a single index entry.
    Returns (was_added, message)
    """
    if human_id in index:
        existing_cid = index[human_id]
        if existing_cid == cid:
            return False, f"⚠️  Skipped {human_id} (already exists with same CID)"
        else:
            return False, f"❌ Conflict: {human_id} points to different CID (existing: {existing_cid[:16]}..., new: {cid[:16]}...)"
    else:
        if not dry_run:
            index[human_id] = cid
        return True, f"✅ Added {human_id} → {cid[:16]}..."


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
    
    Args:
        car_path: Path to CAR file
        dry_run: If True, preview without writing
        verbose: Show detailed output
        verify_only: If True, show verification status without saving blocks
    
    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print("CADMIES Import from CAR v1.1.0")
    if dry_run:
        print("** DRY RUN MODE - No changes will be made **")
    if verify_only:
        print("** VERIFY ONLY MODE - Showing verification status only **")
    print("=" * 60)
    
    # 1. Check if CAR file exists
    if not car_path.exists():
        print(f"❌ CAR file not found: {car_path}")
        return False
    
    print(f"📦 Reading CAR file: {car_path}")
    print(f"   File size: {car_path.stat().st_size:,} bytes")
    
    # 2. Read CAR file
    try:
        blocks, roots = read_car(car_path)
        print(f"✅ Read {len(blocks)} block(s) from CAR")
        print(f"   Root CID(s): {roots}")
    except Exception as e:
        print(f"❌ Failed to read CAR file: {e}")
        return False
    
    # 3. Load current index
    current_index = load_index()
    
    # 4. Process each block
    print("\n" + "-" * 40)
    print("Processing blocks...")
    print("-" * 40)
    
    stats = {
        "total_blocks": len(blocks),
        "new_blocks": 0,
        "existing_blocks": 0,
        "invalid_blocks": 0,
        "reminted_blocks": 0,
        "index_added": 0,
        "index_conflicts": 0,
        "index_skipped": 0
    }
    
    # Track verification blocks for post-processing
    verification_blocks = []
    
    # First, find index blocks and regular blocks
    index_blocks = {}
    concept_blocks = {}
    
    for cid_str, block_data in blocks.items():
        # Check if block is an index.json block
        try:
            decoded = json.loads(block_data.decode('utf-8'))
            # Check if it's our index format (keys are human_ids, values are CIDs)
            if all(isinstance(v, str) and (v.startswith('bafy') or v.startswith('Qm')) for v in decoded.values()):
                index_blocks[cid_str] = decoded
                if verbose:
                    print(f"   📑 Found index block: {cid_str[:16]}... ({len(decoded)} entries)")
                continue
        except:
            pass
        
        # Check if this is a verification block
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
        except:
            pass
        
        # Regular block
        concept_blocks[cid_str] = block_data
    
    # If verify_only mode, just show verification info and exit
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
                
                # Check if concept exists locally
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
    
    # 5. Save regular blocks to store (skip if dry_run)
    if not dry_run:
        print(f"\n📦 Saving {len(concept_blocks)} concept/provenance block(s)...")
    
    for cid_str, block_data in concept_blocks.items():
        # Skip integrity check for CIDv0 blocks (Qm prefix)
        if cid_str.startswith('Qm'):
            if verbose:
                print(f"   🔓 Skipping integrity check for CIDv0: {cid_str[:16]}...")
            integrity_ok = True
        else:
            integrity_ok = verify_block_integrity(block_data, cid_str)
        
        if not integrity_ok:
            # CID mismatch during import — re-encode and save under new CID
            # This preserves provenance by recording both the original CAR CID
            # and the new locally-computed CID inside the block's extra_fields.
            import dag_cbor
            decoded = dag_cbor.decode(block_data)
            normalized = dag_cbor.encode(decoded)
            
            # Save under the new CID with provenance embedded
            if not dry_run:
                # Preserve the original CAR CID in the block metadata
                if 'extra_fields' not in decoded:
                    decoded['extra_fields'] = {}
                decoded['extra_fields']['original_car_cid'] = cid_str
                decoded['extra_fields']['import_date'] = datetime.now(timezone.utc).isoformat()
                # Re-encode with the added provenance fields
                enriched = dag_cbor.encode(decoded)
                # Recalculate CID with provenance embedded
                final_cid = calculate_cid(enriched)
                success = save_block_to_store(final_cid, enriched, BLOCKS_DIR)
                if success:
                    print(f"   🔄 CID changed during import: {cid_str[:16]}... → {final_cid[:16]}... (provenance preserved)")
                    stats["new_blocks"] += 1
                    stats["reminted_blocks"] += 1
                else:
                    print(f"   ❌ Failed to save: {cid_str[:16]}...")
                    stats["invalid_blocks"] += 1
            else:
                print(f"   [DRY RUN] Would re-mint with provenance: {cid_str[:16]}...")
                stats["new_blocks"] += 1
                stats["reminted_blocks"] += 1
            continue
        
        # Check if already exists
        existing = load_block_from_store(cid_str, BLOCKS_DIR)
        if existing is not None:
            if verbose:
                print(f"   ⏭️  Already exists: {cid_str[:16]}...")
            stats["existing_blocks"] += 1
            continue
        
        # Save new block
        if not dry_run:
            success = save_block_to_store(cid_str, block_data, BLOCKS_DIR)
            if success:
                print(f"   ✅ Saved: {cid_str[:16]}... ({len(block_data)} bytes)")
                stats["new_blocks"] += 1
            else:
                print(f"   ❌ Failed to save: {cid_str[:16]}...")
                stats["invalid_blocks"] += 1
        else:
            print(f"   [DRY RUN] Would save: {cid_str[:16]}...")
            stats["new_blocks"] += 1
    
    # 6. Merge index blocks
    if not dry_run:
        print(f"\n📑 Processing index entries...")
    
    for idx_cid, index_data in index_blocks.items():
        for human_id, cid in index_data.items():
            was_added, message = merge_index_entry(current_index, human_id, cid, dry_run)
            
            if "Added" in message:
                print(f"   {message}")
                stats["index_added"] += 1
            elif "Conflict" in message:
                print(f"   {message}")
                stats["index_conflicts"] += 1
            else:
                if verbose:
                    print(f"   {message}")
                stats["index_skipped"] += 1
    
    # 7. Save updated index (if not dry run and changes made)
    if not dry_run and (stats["index_added"] > 0):
        save_index(current_index)
        print(f"\n💾 Saved index with {stats['index_added']} new entry(s)")
    elif dry_run and stats["index_added"] > 0:
        print(f"\n[DRY RUN] Would add {stats['index_added']} entry(s) to index")
    
    # 8. Post-import: Check verification blocks and refresh badges
    if not dry_run and verification_blocks:
        print("\n" + "-" * 40)
        print("🔐 VERIFICATION BLOCKS DETECTED")
        print("-" * 40)
        
        for vb in verification_blocks:
            concept_cid = vb['concept_cid']
            if concept_cid:
                # Check if concept block exists
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
    
    # 9. Print summary
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"📦 Total blocks in CAR:    {stats['total_blocks']}")
    print(f"✅ New blocks saved:       {stats['new_blocks']}")
    print(f"🔄   Reminted on import:    {stats['reminted_blocks']}")
    print(f"⏭️  Already existed:        {stats['existing_blocks']}")
    print(f"❌ Invalid blocks:         {stats['invalid_blocks']}")
    print(f"📑 Index entries added:    {stats['index_added']}")
    print(f"⚠️  Index conflicts:        {stats['index_conflicts']}")
    print(f"⏭️  Index entries skipped:  {stats['index_skipped']}")
    print(f"🔐 Verification blocks:    {len(verification_blocks)}")
    print("=" * 60)
    
    if dry_run:
        print("\n⚠️  This was a DRY RUN. No changes were made.")
        print("   Run without --dry-run to actually import.")
    
    return stats["invalid_blocks"] == 0


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Import CADMIES concept from CAR file",
        epilog="""
Examples:
  import_from_car.py natural_selection.car
  import_from_car.py my_export.car --dry-run
  import_from_car.py concept.car --verbose
  import_from_car.py verification.car --verify-only
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'car_file',
        help='Path to CAR file to import'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview import without making changes'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Show verification status from CAR without importing blocks'
    )
    
    args = parser.parse_args()
    
    # Run import
    success = import_car(
        car_path=Path(args.car_file),
        dry_run=args.dry_run,
        verbose=args.verbose,
        verify_only=args.verify_only
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()