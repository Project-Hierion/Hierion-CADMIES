#!/usr/bin/env python3
"""
File: verification_manager.py
Tool: CADMIES Verification Manager
Version: 1.0.0
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Manage verification statements on concepts.
         Four-tier verification system (🔴🟡🟢💎).
         Export verifications as CAR files for scientific exchange.

Usage:
    python tools/core/verification_manager.py --status <cid>
    python tools/core/verification_manager.py --export-verification --concept-cid <cid> --verifier-key <key> --source <type> --output <path>

Dependencies: provenance_manager.py, paths.py, car_utils.py
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from provenance_manager import ProvenanceManager
from paths import PROJECT_ROOT, BLOCKS_DIR


# ============================================================================
# VERIFICATION LEVELS
# ============================================================================

VERIFICATION_LEVELS = {
    0: {"badge": "🔴", "label": "Unverified", "requirement": "No verification blocks"},
    1: {"badge": "🟡", "label": "Self-verified", "requirement": "Only verifications with source='self'"},
    2: {"badge": "🟢", "label": "Verified", "requirement": "At least one source='orcid' OR source='institution'"},
    3: {"badge": "💎", "label": "Highly Verified", "requirement": "2+ ORCID verifications OR 1 ORCID + 1 institution"}
}


pm = ProvenanceManager()


def add_verification_statement(verifier_key: str, concept_cid: str, statement_type: str,
                                source: str, metadata: Optional[Dict] = None) -> Optional[str]:
    """
    Add a verification statement to a concept's provenance.
    
    Args:
        verifier_key: Key identifying the verifier (ORCID, public key, or "self")
        concept_cid: CID of the concept being verified
        statement_type: Type of verification (e.g., "endorses", "confirms", "agrees")
        source: Source type ("self", "orcid", "institution", "peer")
        metadata: Additional metadata (ORCID ID, institution name, etc.)
    
    Returns:
        CID of the created provenance block, or None if failed
    """
    record_data = {
        "verifier_key": verifier_key,
        "statement_type": statement_type,
        "source": source,
        "metadata": metadata or {}
    }
    
    result = pm.create_provenance_record(
        concept_cid=concept_cid,
        author=verifier_key,
        record_type="verification",
        **record_data
    )
    
    return result.get("provenance_cid") if result.get("stored") else None


def get_verification_chain(concept_cid: str) -> List[Dict]:
    """Get all verification blocks for a concept."""
    all_provenance = pm.query_provenance(concept_cid)
    return [p for p in all_provenance if p.get("record_type") == "verification"]


def calculate_verification_level(verification_chain: List[Dict]) -> int:
    """
    Calculate verification level based on chain.
    
    Level 0: No verifications
    Level 1: Only self-verifications
    Level 2: At least one ORCID or institution verification
    Level 3: 2+ ORCID verifications OR 1 ORCID + 1 institution
    """
    if not verification_chain:
        return 0
    
    source_counts = {"self": 0, "orcid": 0, "institution": 0, "peer": 0}
    
    for v in verification_chain:
        source = v.get("source", "unknown")
        if source in source_counts:
            source_counts[source] += 1
    
    if source_counts["self"] > 0 and sum(source_counts.values()) == source_counts["self"]:
        return 1
    
    if source_counts["orcid"] >= 2 or (source_counts["orcid"] >= 1 and source_counts["institution"] >= 1):
        return 3
    
    if source_counts["orcid"] >= 1 or source_counts["institution"] >= 1:
        return 2
    
    if source_counts["self"] > 0:
        return 1
    
    return 0


def get_verification_status(concept_cid: str) -> Dict:
    """
    Get complete verification status for a concept.
    
    Returns:
        Dict with keys: level, badge, label, chain_count, chain
    """
    chain = get_verification_chain(concept_cid)
    level = calculate_verification_level(chain)
    
    return {
        "level": level,
        "badge": VERIFICATION_LEVELS[level]["badge"],
        "label": VERIFICATION_LEVELS[level]["label"],
        "chain_count": len(chain),
        "chain": chain
    }


def cids_equivalent(cid1: str, cid2: str) -> bool:
    """Check if two CIDs refer to the same content."""
    if cid1 == cid2:
        return True
    try:
        from multiformats import CID
        obj1 = CID.decode(cid1)
        obj2 = CID.decode(cid2)
        return obj1.digest == obj2.digest
    except (ValueError, ImportError):
        return False


def verify_block_integrity(block_data: bytes, expected_cid: str) -> bool:
    """Verify that block data matches its CID."""
    from car_utils import calculate_cid
    actual_cid = calculate_cid(block_data)
    return cids_equivalent(actual_cid, expected_cid)


def load_block_from_store(cid: str) -> Optional[bytes]:
    """Load a block from CADMIES blockstore by CID."""
    block_path = BLOCKS_DIR / f"{cid}.cbor"
    if block_path.exists():
        with open(block_path, 'rb') as f:
            return f.read()
    
    block_path = BLOCKS_DIR / cid
    if block_path.exists():
        with open(block_path, 'rb') as f:
            return f.read()
    
    return None


def ensure_bytes(value) -> bytes:
    """Convert string to bytes if needed."""
    if isinstance(value, str):
        return value.encode('utf-8')
    return value


def export_verification_as_car(concept_cid: str, verifier_key: str, statement_type: str,
                                source: str, output_path: Path, metadata: dict = None) -> bool:
    """
    Create a verification block for a concept and export both to a CAR file.
    
    Args:
        concept_cid: CID of concept being verified
        verifier_key: Key identifying the verifier (e.g., ORCID, public key)
        statement_type: Type of verification (e.g., "endorses", "confirms")
        source: Source type ("self", "orcid", "institution")
        output_path: Where to save the CAR file
        metadata: Optional additional metadata
    
    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print("Export Verification as CAR")
    print("=" * 60)
    
    provenance_cid = add_verification_statement(
        verifier_key=verifier_key,
        concept_cid=concept_cid,
        statement_type=statement_type,
        source=source,
        metadata=metadata
    )
    
    if not provenance_cid:
        print(f"❌ Failed to create verification block")
        return False
    
    print(f"✅ Created verification block: {provenance_cid}")
    
    concept_block = load_block_from_store(concept_cid)
    if not concept_block:
        print(f"❌ Concept block not found: {concept_cid}")
        return False
    
    print(f"✅ Loaded concept block ({len(concept_block)} bytes)")
    
    verification_block = load_block_from_store(provenance_cid)
    if not verification_block:
        print(f"❌ Verification block not found: {provenance_cid}")
        return False
    
    print(f"✅ Loaded verification block ({len(verification_block)} bytes)")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from car_utils import write_car
        
        blocks_for_car = {}
        
        concept_bytes = ensure_bytes(concept_cid)
        blocks_for_car[concept_bytes] = concept_block
        
        verification_bytes = ensure_bytes(provenance_cid)
        blocks_for_car[verification_bytes] = verification_block
        
        roots = [concept_bytes]
        
        write_car(blocks_for_car, roots, output_path)
        
        print(f"\n✅ Successfully exported verification CAR to: {output_path}")
        print(f"   Concept: {concept_cid}")
        print(f"   Verification: {provenance_cid}")
        print(f"   File size: {output_path.stat().st_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to write CAR file: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CADMIES Verification Manager")
    parser.add_argument('--export-verification', action='store_true', help='Export verification as CAR')
    parser.add_argument('--concept-cid', help='CID of concept to verify')
    parser.add_argument('--verifier-key', help='Verifier key (ORCID, etc.)')
    parser.add_argument('--statement-type', default='endorses', help='Type of verification')
    parser.add_argument('--source', help='Source type (self, orcid, institution)')
    parser.add_argument('--output', help='Output CAR file path')
    parser.add_argument('--status', help='Show verification status for a concept CID')
    
    args = parser.parse_args()
    
    if args.status:
        status = get_verification_status(args.status)
        print(f"Verification Status for {args.status}:")
        print(f"  Badge: {status['badge']}")
        print(f"  Level: {status['level']}")
        print(f"  Label: {status['label']}")
        print(f"  Verifications: {status['chain_count']}")
    
    elif args.export_verification:
        if not args.concept_cid or not args.verifier_key or not args.source or not args.output:
            print("ERROR: --concept-cid, --verifier-key, --source, and --output required")
            sys.exit(1)
        
        success = export_verification_as_car(
            concept_cid=args.concept_cid,
            verifier_key=args.verifier_key,
            statement_type=args.statement_type,
            source=args.source,
            output_path=Path(args.output),
            metadata={"exported_via": "cli"}
        )
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
