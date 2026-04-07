#!/usr/bin/env python3
"""
Export to CAR v1.0.0
Purpose: Export CADMIES concepts (with provenance) to CAR files for sharing
Usage: python tools/export_to_car.py <human_id_or_cid> --output <file.car>
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Union

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from car_utils import (
    write_car,
    load_block_from_store,
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
    """Load human_id to CID mapping from index."""
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)


def is_cid(value: str) -> bool:
    """Check if string looks like a CID (starts with bafy or Qm)."""
    return value.startswith('bafy') or value.startswith('Qm')


def ensure_bytes(value: Union[str, bytes]) -> bytes:
    """Convert string to bytes if needed."""
    if isinstance(value, str):
        return value.encode('utf-8')
    return value


def resolve_identifier(identifier: str, index: Dict[str, str]) -> Optional[str]:
    """
    Auto-detect if identifier is CID or human_id.
    Returns CID string or None if not found.
    """
    if is_cid(identifier):
        # It's a CID - verify block exists
        block_path = BLOCKS_DIR / f"{identifier}.cbor"
        if block_path.exists():
            return identifier
        else:
            print(f"❌ CID not found in blockstore: {identifier}")
            return None
    else:
        # It's a human_id - look up in index
        cid = index.get(identifier)
        if cid:
            return cid
        else:
            print(f"❌ Human ID not found in index: {identifier}")
            return None


def get_provenance_blocks(concept_cid: str) -> Dict[str, bytes]:
    """
    Find all provenance blocks that reference this concept.
    Returns dict of {cid: block_bytes}
    """
    provenance_blocks = {}
    
    # Scan all blocks in store
    for block_path in BLOCKS_DIR.glob("*.cbor"):
        cid = block_path.stem
        
        # Skip the concept block itself
        if cid == concept_cid:
            continue
        
        # Load block data
        block_data = load_block_from_store(cid, BLOCKS_DIR)
        if not block_data:
            continue
        
        # Try to decode as CBOR to check if it's a provenance block
        try:
            import dag_cbor
            decoded = dag_cbor.decode(block_data)
            
            # Check if this is a provenance block referencing our concept
            if (decoded.get('record_type') in ['creation', 'verification', 'supersession', 'comment'] 
                and decoded.get('concept_cid') == concept_cid):
                provenance_blocks[cid] = block_data
        except:
            pass
    
    return provenance_blocks


def export_concept(identifier: str, output_path: Path, include_provenance: bool = True) -> bool:
    """
    Export a concept and its provenance to a CAR file.
    """
    print("=" * 60)
    print("CADMIES Export to CAR")
    print("=" * 60)
    
    # 1. Load index
    index = load_index()
    
    # 2. Resolve identifier to CID
    concept_cid = resolve_identifier(identifier, index)
    if not concept_cid:
        return False
    
    print(f"✅ Resolved to CID: {concept_cid}")
    
    # 3. Load concept block
    concept_block = load_block_from_store(concept_cid, BLOCKS_DIR)
    if not concept_block:
        print(f"❌ Concept block not found: {concept_cid}")
        return False
    
    print(f"✅ Loaded concept block ({len(concept_block)} bytes)")
    
    # 4. Prepare blocks dictionary (key: CID string, value: block bytes)
    blocks: Dict[str, bytes] = {
        concept_cid: concept_block
    }
    
    # 5. Find and add provenance blocks
    if include_provenance:
        provenance_blocks = get_provenance_blocks(concept_cid)
        blocks.update(provenance_blocks)
        print(f"✅ Found {len(provenance_blocks)} provenance block(s)")
    else:
        print(f"⚠️ Skipping provenance blocks")
    
    # 6. Add index block (human_id → CID mapping)
    human_id = None
    for hid, cid in index.items():
        if cid == concept_cid:
            human_id = hid
            break
    
    if human_id:
        index_block = {human_id: concept_cid}
        index_bytes = json.dumps(index_block, indent=2).encode('utf-8')
        index_cid = calculate_cid(index_bytes)
        blocks[index_cid] = index_bytes
        print(f"✅ Added index block with human_id: {human_id}")
    
    # 7. Write CAR file
    try:
        # Convert blocks from {cid_str: bytes} to {cid_bytes: bytes}
        blocks_for_car = {}
        for cid_str, block_data in blocks.items():
            cid_bytes = ensure_bytes(cid_str)
            blocks_for_car[cid_bytes] = block_data
        
        roots = [ensure_bytes(concept_cid)]
        
        write_car(blocks_for_car, roots, output_path)
        
        print(f"\n✅ Successfully exported to: {output_path}")
        print(f"   Total blocks: {len(blocks)}")
        print(f"   File size: {output_path.stat().st_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to write CAR file: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Export CADMIES concept to CAR file",
        epilog="""
Examples:
  export_to_car.py natural_selection --output natural_selection.car
  export_to_car.py bafyreiestgqzxnxmpb27s7s5pjv4fjawra6rexgomkni6itljrhlqkf3ee --output concept.car
        """
    )
    
    parser.add_argument(
        'identifier',
        help='CID or human_id of concept to export'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output CAR file path'
    )
    
    parser.add_argument(
        '--no-provenance',
        action='store_true',
        help='Exclude provenance blocks'
    )
    
    args = parser.parse_args()
    
    success = export_concept(
        identifier=args.identifier,
        output_path=Path(args.output),
        include_provenance=not args.no_provenance
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()