#!/usr/bin/env python3
# orcid_stamper.py
# ORCID Public API integration - creates verification blocks
# Limitations: Public API cannot prove ownership (OAuth required for that)
# Badge shows 🟢 but indicates "claimed" not "owner-verified"

import sys
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime

# Add tools/core to path
sys.path.append(str(Path(__file__).parent))
from verification_manager import add_verification_statement

ORCID_API_URL = "https://pub.orcid.org/v3.0"

def fetch_orcid_profile(orcid_id):
    """
    Fetch public ORCID profile.
    Returns (name, record_hash, raw_data) or (None, None, None) if not found.
    """
    # Format ORCID ID with hyphens if not already
    if '-' not in orcid_id and len(orcid_id) == 16:
        orcid_id = f"{orcid_id[:4]}-{orcid_id[4:8]}-{orcid_id[8:12]}-{orcid_id[12:]}"
    
    url = f"{ORCID_API_URL}/{orcid_id}/record"
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract name from person record
            person_url = f"{ORCID_API_URL}/{orcid_id}/person"
            person_response = requests.get(person_url, headers=headers, timeout=10)
            
            name = orcid_id  # fallback
            if person_response.status_code == 200:
                person_data = person_response.json()
                name_parts = person_data.get('name', {})
                given = name_parts.get('given-names', {}).get('value', '')
                family = name_parts.get('family-name', {}).get('value', '')
                if given or family:
                    name = f"{given} {family}".strip()
            
            # Create hash of record for offline verification
            record_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
            
            return (name, record_hash, data)
        else:
            print(f"ORCID API error: {response.status_code}")
            return (None, None, None)
    except Exception as e:
        print(f"Error fetching ORCID profile: {e}")
        return (None, None, None)

def stamp_with_orcid(concept_cid, orcid_id, verifier_key="orcid-public-api"):
    """
    Create verification block using public ORCID data.
    Returns provenance_cid or None.
    """
    name, record_hash, raw_data = fetch_orcid_profile(orcid_id)
    
    if not name:
        print(f"ERROR: ORCID {orcid_id} not found or inaccessible")
        return None
    
    metadata = {
        "orcid_id": orcid_id,
        "orcid_name": name,
        "orcid_record_hash": record_hash,
        "verification_method": "public_api_claimed",
        "limitation_note": "Public API cannot prove ownership. Full verification requires OAuth.",
        "fetch_timestamp": datetime.now().isoformat() + "Z"
    }
    
    provenance_cid = add_verification_statement(
        verifier_key=verifier_key,
        concept_cid=concept_cid,
        statement_type="endorses",
        source="orcid",
        metadata=metadata
    )
    
    print(f"✅ ORCID stamp added for {name} ({orcid_id})")
    print(f"   Provenance CID: {provenance_cid}")
    print(f"   ⚠️ Note: This is claimed verification, not owner-verified")
    
    return provenance_cid

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Stamp concept with ORCID verification (public API)")
    parser.add_argument("concept_cid", help="CID of concept to verify")
    parser.add_argument("orcid_id", help="ORCID ID (e.g., 0000-0001-5000-0007)")
    parser.add_argument("--verifier-key", default="orcid-public-api", help="Key used for verification")
    
    args = parser.parse_args()
    
    stamp_with_orcid(args.concept_cid, args.orcid_id, args.verifier_key)