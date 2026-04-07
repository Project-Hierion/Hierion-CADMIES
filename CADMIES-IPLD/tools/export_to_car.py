#!/usr/bin/env python3
"""
Export to CAR v1.0.0
Purpose: Export CADMIES concepts (with provenance) to CAR files for sharing
Usage: python tools/export_to_car.py <human_id_or_cid> --output <file.car>
       python tools/export_to_car.py --concepts id1,id2,id3 --output bundle.car
       python tools/export_to_car.py --all --output full_mycelium.car
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Union, List, Set

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


def collect_concept_blocks(identifiers: List[str], index: Dict[str, str], include_provenance: bool = True) -> tuple:
    """
    Collect all blocks for given identifiers.
    Returns (blocks_dict, concept_cids_list, human_id_map)
    """
    blocks = {}
    concept_cids = []
    human_id_map = {}
    
    for identifier in identifiers:
        # Resolve to CID
        cid = resolve_identifier(identifier, index)
        if not cid:
            print(f"⚠️ Skipping invalid identifier: {identifier}")
            continue
        
        concept_cids.append(cid)
        
        # Load concept block
        concept_block = load_block_from_store(cid, BLOCKS_DIR)
        if not concept_block:
            print(f"⚠️ Concept block not found for {identifier} ({cid})")
            continue
        
        blocks[cid] = concept_block
        print(f"   📦 {identifier} → {cid[:16]}... ({len(concept_block)} bytes)")
        
        # Track human_id mapping
        human_id_map[identifier] = cid
        
        # Add provenance blocks
        if include_provenance:
            provenance = get_provenance_blocks(cid)
            blocks.update(provenance)
            if provenance:
                print(f"      📎 +{len(provenance)} provenance block(s)")
    
    return blocks, concept_cids, human_id_map


def export_concepts(identifiers: List[str], output_path: Path, include_provenance: bool = True) -> bool:
    """
    Export multiple concepts to a CAR file.
    """
    print("=" * 60)
    print("CADMIES Export to CAR (Multi-Concept)")
    print("=" * 60)
    
    # 1. Load index
    index = load_index()
    
    # 2. Collect all blocks
    print(f"\n📦 Collecting {len(identifiers)} concept(s)...")
    blocks, concept_cids, human_id_map = collect_concept_blocks(identifiers, index, include_provenance)
    
    if not blocks:
        print("❌ No valid concepts found to export")
        return False
    
    print(f"\n✅ Collected {len(blocks)} total block(s)")
    print(f"   Concept blocks: {len(concept_cids)}")
    print(f"   Total unique CIDs: {len(set(blocks.keys()))}")
    
    # 3. Add consolidated index block
    index_bytes = json.dumps(human_id_map, indent=2).encode('utf-8')
    index_cid = calculate_cid(index_bytes)
    blocks[index_cid] = index_bytes
    print(f"✅ Added consolidated index block with {len(human_id_map)} mapping(s)")
    
    # 4. Write CAR file
    try:
        blocks_for_car = {}
        for cid_str, block_data in blocks.items():
            cid_bytes = ensure_bytes(cid_str)
            blocks_for_car[cid_bytes] = block_data
        
        roots = [ensure_bytes(cid) for cid in concept_cids]
        
        write_car(blocks_for_car, roots, output_path)
        
        print(f"\n✅ Successfully exported to: {output_path}")
        print(f"   Total blocks: {len(blocks)}")
        print(f"   Root concepts: {len(concept_cids)}")
        print(f"   File size: {output_path.stat().st_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to write CAR file: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_all_concept_cids(index: Dict[str, str]) -> List[str]:
    """Get all unique concept CIDs from the index."""
    return list(set(index.values()))


def get_all_human_ids(index: Dict[str, str]) -> List[str]:
    """Get all human_ids from the index."""
    return list(index.keys())


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Export CADMIES concepts to CAR file",
        epilog="""
Examples:
  # Single concept
  export_to_car.py natural_selection --output single.car
  
  # Multiple concepts (comma-separated)
  export_to_car.py --concepts natural_selection,entropy,occams_razor --output bundle.car
  
  # Multiple concepts (file)
  export_to_car.py --concepts-file my_list.txt --output bundle.car
  
  # All concepts
  export_to_car.py --all --output full_mycelium.car
  
  # By CID
  export_to_car.py --cids bafy...,bafy... --output bundle.car
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Mutually exclusive input methods
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'identifier',
        nargs='?',
        help='Single CID or human_id'
    )
    input_group.add_argument(
        '--concepts', '-c',
        help='Comma-separated list of human_ids'
    )
    input_group.add_argument(
        '--concepts-file', '-f',
        help='File containing one human_id per line'
    )
    input_group.add_argument(
        '--cids',
        help='Comma-separated list of CIDs'
    )
    input_group.add_argument(
        '--all', '-a',
        action='store_true',
        help='Export all concepts in the mycelium'
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
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Parse identifiers based on input method
    identifiers = []
    
    if args.identifier:
        identifiers = [args.identifier]
    
    elif args.concepts:
        identifiers = [h.strip() for h in args.concepts.split(',') if h.strip()]
    
    elif args.concepts_file:
        path = Path(args.concepts_file)
        if not path.exists():
            print(f"❌ File not found: {path}")
            sys.exit(1)
        with open(path, 'r') as f:
            identifiers = [line.strip() for line in f if line.strip()]
    
    elif args.cids:
        identifiers = [c.strip() for c in args.cids.split(',') if c.strip()]
    
    elif args.all:
        index = load_index()
        identifiers = get_all_human_ids(index)
        print(f"📦 Exporting all {len(identifiers)} concepts from mycelium")
    
    if not identifiers:
        print("❌ No identifiers provided")
        sys.exit(1)
    
    print(f"📦 Exporting {len(identifiers)} concept(s)")
    if args.verbose:
        for i, id in enumerate(identifiers[:10]):
            print(f"   {i+1}. {id}")
        if len(identifiers) > 10:
            print(f"   ... and {len(identifiers) - 10} more")
    
    success = export_concepts(
        identifiers=identifiers,
        output_path=Path(args.output),
        include_provenance=not args.no_provenance
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()