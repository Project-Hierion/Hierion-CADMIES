# verification_manager.py
# Depends on: provenance_manager.py, paths.py

from provenance_manager import ProvenanceManager
from paths import BLOCKS_DIR

VERIFICATION_LEVELS = {
    0: {"badge": "🔴", "label": "Unverified"},
    1: {"badge": "🟡", "label": "Self-verified"},
    2: {"badge": "🟢", "label": "Verified"},
    3: {"badge": "💎", "label": "Highly Verified"}
}

def get_verification_status(concept_cid):
    """Returns (level, badge, label, verification_chain)"""
    verification_chain = get_verification_chain(concept_cid)
    level = calculate_verification_level(verification_chain)
    badge = VERIFICATION_LEVELS[level]["badge"]
    label = VERIFICATION_LEVELS[level]["label"]
    return (level, badge, label, verification_chain)

def get_verification_chain(concept_cid):
    """Returns all verification provenance blocks for a concept"""
    try:
        pm = ProvenanceManager()
        all_provenance = pm.query_provenance(concept_cid)
        # Filter for verification records
        verification_records = [p for p in all_provenance if p.get('record_type') == 'verification']
        return verification_records
    except Exception:
        return []

def calculate_verification_level(chain):
    """Calculate verification level based on chain contents"""
    if not chain:
        return 0
    
    sources = [p.get('metadata', {}).get('source', 'self') for p in chain]
    
    # Check for highly verified (level 3)
    orcid_count = sources.count('orcid')
    institution_count = sources.count('institution')
    
    if orcid_count >= 2 or (orcid_count >= 1 and institution_count >= 1):
        return 3
    
    # Check for verified (level 2)
    if 'orcid' in sources or 'institution' in sources:
        return 2
    
    # Check for self-verified (level 1)
    if 'self' in sources:
        return 1
    
    return 0

def add_verification_statement(verifier_key, concept_cid, statement_type, source="self", metadata=None):
    """
    Creates provenance block with type="verification"
    source: "self", "orcid", "institution"
    """
    from provenance_manager import ProvenanceManager
    import json
    from datetime import datetime
    
    pm = ProvenanceManager()
    
    verification_data = {
        "record_type": "verification",
        "verifier_key": verifier_key,
        "concept_cid": concept_cid,
        "statement_type": statement_type,  # "endorses", "questions", "refutes"
        "source": source,
        "timestamp": datetime.now().isoformat() + "Z"
    }
    
    if metadata:
        verification_data["metadata"] = metadata
    
    # Create provenance block
    provenance_cid = pm.create_provenance_record(
        concept_cid=concept_cid,
        author=verifier_key,
        record_type="verification",
        comment=f"Verification statement: {statement_type}",
        metadata=verification_data
)
    
    return provenance_cid