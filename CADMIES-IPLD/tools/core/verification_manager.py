# verification_manager.py
# Depends on: provenance_manager.py, paths.py

VERIFICATION_LEVELS = {
    0: {"badge": "🔴", "label": "Unverified"},
    1: {"badge": "🟡", "label": "Self-verified"},
    2: {"badge": "🟢", "label": "Verified"},
    3: {"badge": "💎", "label": "Highly Verified"}
}

def get_verification_status(concept_cid):
    # Returns (level, badge, label, verification_chain)
    pass

def add_verification_statement(verifier_key, concept_cid, statement_type, source="self", metadata=None):
    # Creates provenance block with type="verification"
    # source: "self", "orcid", "institution"
    pass

def get_verification_chain(concept_cid):
    # Returns list of all verification provenance blocks
    pass

def calculate_verification_level(chain):
    # Logic: 
    # - empty = level 0
    # - only self = level 1  
    # - any orcid/institution = level 2
    # - 2+ orcid OR 1 orcid+1 institution = level 3
    pass
