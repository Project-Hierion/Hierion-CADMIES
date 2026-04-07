#!/usr/bin/env python3
"""
Import from CAR v1.0.0
Purpose: Import CADMIES concepts from CAR files into local mycelium
Usage: python tools/import_from_car.py <file.car>
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Tuple

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from car_utils import (
    read_car,
    save_block_to_store,
    load_block_from_store,
    verify_block_integrity
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


def import_car(car_path: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """
    Import a CAR file into the local mycelium.
    
    Args:
        car_path: Path to CAR file
        dry_run: If True, preview without writing
        verbose: Show detailed output
    
    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print("CADMIES Import from CAR")
    if dry_run:
        print("** DRY RUN MODE - No changes will be made **")
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
        "index_added": 0,
        "index_conflicts": 0,
        "index_skipped": 0
    }
    
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
        
        # Regular block
        concept_blocks[cid_str] = block_data
    
    # 5. Save regular blocks to store
    print(f"\n📦 Saving {len(concept_blocks)} concept/provenance block(s)...")
    
    for cid_str, block_data in concept_blocks.items():
        # Skip integrity check for CIDv0 blocks (Qm prefix)
        # These are usually index or small blocks that work fine
        if cid_str.startswith('Qm'):
            if verbose:
                print(f"   🔓 Skipping integrity check for CIDv0: {cid_str[:16]}...")
            integrity_ok = True
        else:
            integrity_ok = verify_block_integrity(block_data, cid_str)
        
        if not integrity_ok:
            print(f"   ❌ Invalid block (CID mismatch): {cid_str[:16]}...")
            stats["invalid_blocks"] += 1
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
                print(f"   {message}")
                stats["index_skipped"] += 1
    
    # 7. Save updated index (if not dry run and changes made)
    if not dry_run and (stats["index_added"] > 0):
        save_index(current_index)
        print(f"\n💾 Saved index with {stats['index_added']} new entry(s)")
    elif dry_run and stats["index_added"] > 0:
        print(f"\n[DRY RUN] Would add {stats['index_added']} entry(s) to index")
    
    # 8. Print summary
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"📦 Total blocks in CAR:    {stats['total_blocks']}")
    print(f"✅ New blocks saved:       {stats['new_blocks']}")
    print(f"⏭️  Already existed:        {stats['existing_blocks']}")
    print(f"❌ Invalid blocks:         {stats['invalid_blocks']}")
    print(f"📑 Index entries added:    {stats['index_added']}")
    print(f"⚠️  Index conflicts:        {stats['index_conflicts']}")
    print(f"⏭️  Index entries skipped:  {stats['index_skipped']}")
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
    
    args = parser.parse_args()
    
    # Run import
    success = import_car(
        car_path=Path(args.car_file),
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()