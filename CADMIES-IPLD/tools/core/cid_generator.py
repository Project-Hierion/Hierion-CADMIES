#!/usr/bin/env python3
"""
File: cid_generator.py
Tool: CADMIES CID Generator
Version: 1.1.0
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Generates CIDs from structured knowledge concepts using IPLD/DAG-CBOR.
         Provides deterministic content addressing for shared understanding.
         Content-addressed, immutable, verifiable.

Usage:
    python tools/core/cid_generator.py
    python tools/core/cid_generator.py --concept-file concept.json

Version History:
  v1.1.0 (2026-06-24): Project renamed from Hieros to Hierion. Updated author,
      copyright, and contact information.
  v1.0.0: Initial release — CIDv1, dag-cbor, SHA2-256.
"""

import json
import dag_cbor
from multiformats import multihash, CID
from typing import Dict, Any
import hashlib
from provenance_manager import ProvenanceManager
from datetime import datetime
import argparse
import sys
import os
from paths import BLOCKS_DIR, INDEX_DIR, INDEX_FILE, LOGS_DIR, ensure_dirs

class CIDGenerator:
    """
    CID Generator for UniversalScientificConcept format
    
    Generates CIDs from structured knowledge concepts using IPLD/DAG-CBOR.
    Provides deterministic content addressing for shared understanding.
    
    Philosophy: Knowledge should be freely accessible, not commercially exploited.
    """
    
    def __init__(self):
        self.version = "1.1.0"
        self.codec = "dag-cbor"
        self.hash_algo = "sha2-256"
        self.encoding = "base32"
    
    def validate_concept(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate concept structure against knowledge schema
        """
        errors = []
        warnings = []
    
        required_fields = [
            "schema_version", "human_id", "title", "definition",
            "type", "domain", "metadata"
        ]
    
        for field in required_fields:
            if field not in concept:
                errors.append(f"Missing required field: {field}")
    
        if "metadata" in concept:
            metadata = concept["metadata"]
            meta_required = ["creator", "certainty_score", "version"]
            for field in meta_required:
                if field not in metadata:
                    errors.append(f"Missing metadata field: {field}")
        
            if "created" not in metadata:
                warnings.append("No creation timestamp - provenance will be stored separately")
    
        if errors:
            return {"success": False, "errors": errors, "warnings": warnings}
    
        return {"success": True, "errors": [], "warnings": warnings}

    def generate_cid(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate CID from validated knowledge concept
        
        Returns content-addressed identifier with metadata
        """
        try:
            validation = self.validate_concept(concept)
            if not validation["success"]:
                return {
                    "success": False,
                    "errors": validation["errors"],
                    "cid": None,
                    "hash": None,
                    "bytes_size": 0
                }
            
            serialized = dag_cbor.encode(concept)
            bytes_size = len(serialized)
            
            hash_obj = hashlib.sha256(serialized)
            hash_bytes = hash_obj.digest()
            hash_preview = hash_bytes[:8].hex() + "..."
            
            mh = multihash.wrap(hash_bytes, "sha2-256")
            cid = CID("base32", 1, "dag-cbor", mh)
            cid_str = str(cid)
            
            cid_parts = {
                "version": "CIDv1",
                "codec": "dag-cbor",
                "hash": "sha2-256",
                "encoding": "base32"
            }
            
            return {
                "success": True,
                "cid": cid_str,
                "hash": hash_bytes.hex(),
                "hash_preview": hash_preview,
                "bytes_size": bytes_size,
                "cid_parts": cid_parts,
                "serialized": serialized,
                "errors": []
            }
            
        except Exception as e:
            return {
                "success": False,
                "errors": [f"CID generation failed: {str(e)}"],
                "cid": None,
                "hash": None,
                "bytes_size": 0
            }
    
    def save_to_blockstore(self, cid_result: Dict[str, Any], concept: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save generated block to IPLD blockstore
        
        Creates local blockstore with index and audit trail
        """
        try:
            cid = cid_result["cid"]
            serialized = cid_result["serialized"]
            human_id = concept.get("human_id", "unknown")
            
            block_path = BLOCKS_DIR / f"{cid}.cbor"
            block_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(block_path, "wb") as f:
                f.write(serialized)
            
            index_path = INDEX_DIR / "human_id_to_cid.json"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            index = {}
            if os.path.exists(index_path):
                with open(index_path, "r") as f:
                    index = json.load(f)
            
            index[human_id] = cid
            
            if os.path.exists(index_path):
                backup_dir = os.path.join(os.path.dirname(index_path), "backups")
                os.makedirs(backup_dir, exist_ok=True)
                backup_filename = os.path.basename(index_path) + ".backup." + datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = os.path.join(backup_dir, backup_filename)
                import shutil
                shutil.copy2(index_path, backup_path)
            
            with open(index_path, "w") as f:
                json.dump(index, f, indent=2)
            
            log_path = LOGS_DIR / "operations.jsonl"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            log_entry = {
                "timestamp": datetime.now().isoformat() + "Z",
                "operation": "cid_generation",
                "tool_version": self.version,
                "human_id": human_id,
                "cid": cid,
                "bytes_size": cid_result["bytes_size"],
                "purpose": "knowledge_sharing",
                "source": "external_file" if hasattr(self, 'external_file_path') else "sample_concept"
            }
            
            with open(log_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            try:
                pm = ProvenanceManager()
                provenance_result = pm.create_provenance_record(
                    concept_cid=cid,
                    author="CID_Generator",
                    record_type="creation",
                    comment="Auto-generated from CID generator"
                )
                if provenance_result.get('stored'):
                    print(f"   📝 Provenance record: {provenance_result['provenance_cid'][:20]}...")
            except Exception as e:
                print(f"   ⚠️  Provenance creation failed: {e}")

            return {
                "success": True,
                "block_path": block_path,
                "index_updated": True,
                "log_updated": True,
                "human_id": human_id,
                "cid": cid
            }
            
        except Exception as e:
            return {
                "success": False,
                "errors": [f"Blockstore save failed: {str(e)}"],
                "block_path": None,
                "index_updated": False,
                "log_updated": False
            }
    
    def test_determinism(self, concept: Dict[str, Any]) -> bool:
        """
        Test CID determinism by generating twice and comparing
        
        Critical for trustworthy knowledge systems
        """
        print(f"\n🔬 Testing CID determinism (trust through consistency)...")
        
        result1 = self.generate_cid(concept)
        if not result1["success"]:
            print(f"   ❌ First generation failed: {result1['errors']}")
            return False
        
        cid1 = result1["cid"]
        
        result2 = self.generate_cid(concept)
        if not result2["success"]:
            print(f"   ❌ Second generation failed: {result2['errors']}")
            return False
        
        cid2 = result2["cid"]
        
        if cid1 == cid2:
            print(f"   ✅ Determinism confirmed: same knowledge → same address")
            print(f"   📍 CID: {cid1}")
            return True
        else:
            print(f"   ❌ Determinism FAILED: inconsistency detected")
            print(f"      First:  {cid1}")
            print(f"      Second: {cid2}")
            return False


def create_sample_concept() -> Dict[str, Any]:
    """Create a sample knowledge concept for testing and education"""
    return {
        "schema_version": "1.0.0",
        "human_id": "conservation_of_energy",
        "title": "Law of Conservation of Energy",
        "definition": "Energy cannot be created or destroyed, only transformed from one form to another. This fundamental principle enables understanding of physical systems across scales.",
        "type": "ScientificLaw",
        "domain": "Physics",
        "subdomain": "Classical Mechanics",
        "formula": "ΔE_system = Q - W",
        "proofs": [
            {
                "type": "experimental",
                "description": "Verified through countless experiments including Joule's paddle wheel experiment",
                "confidence": 0.99,
                "date": "1847-01-01",
                "reference": "Joule, J. P. (1847). On the Mechanical Equivalent of Heat"
            },
            {
                "type": "theoretical",
                "description": "Noether's theorem links energy conservation to time translation symmetry",
                "confidence": 0.99,
                "date": "1918-01-01",
                "reference": "Noether, E. (1918). Invariante Variationsprobleme"
            }
        ],
        "cross_references": {
            "wikipedia": "https://en.wikipedia.org/wiki/Conservation_of_energy",
            "doi": "10.1098/rstl.1850.0016",
            "textbook": "Halliday & Resnick, Physics, 10th ed., p.345"
        },
        "metadata": {
            "created": datetime.now().isoformat() + "Z",
            "creator": "IPLD_Knowledge_Generator",
            "certainty_score": 0.99,
            "version": 1,
            "license": "CC BY-SA 4.0",
            "purpose": "educational",
            "supersedes": None,
            "superseded_by": None
        },
        "relationships": {
            "builds_upon": ["NewtonianMechanics", "Thermodynamics"],
            "contradicts": [],
            "related_to": ["ConservationOfMomentum", "ConservationOfMass"],
            "specializes": ["FirstLawOfThermodynamics"]
        },
        "difficulty_levels": {
            "beginner": "Energy doesn't disappear, it just changes form",
            "intermediate": "The total energy in an isolated system remains constant",
            "expert": "Energy conservation emerges from time translation symmetry via Noether's theorem"
        },
        "learning_path": {
            "prerequisites": ["BasicPhysics", "Algebra"],
            "next_steps": ["Thermodynamics", "QuantumMechanics", "FieldTheory"]
        },
        "extra_fields": {
            "units": "Joules",
            "discovery_year": 1847,
            "discoverer": "Julius Robert von Mayer, James Prescott Joule, Hermann von Helmholtz",
            "significance": "Fundamental constraint on all physical processes"
        }
    }


def read_concept_file(file_path: str) -> Dict[str, Any]:
    """
    Read and validate knowledge concept JSON file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Knowledge file not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if not content:
        raise ValueError(f"File is empty: {file_path}")
    
    concept = json.loads(content)
    
    if not isinstance(concept, dict):
        raise ValueError(f"Concept must be a JSON object, got {type(concept)}")
    
    if "human_id" not in concept:
        raise ValueError("Knowledge concept missing required field: human_id")
    
    if "title" not in concept:
        raise ValueError("Knowledge concept missing required field: title")
    
    if "metadata" in concept and "purpose" in concept["metadata"]:
        purpose = concept["metadata"]["purpose"]
        if purpose not in ["educational", "research", "personal_knowledge"]:
            print(f"⚠️  Note: Concept purpose is '{purpose}' - ensure it aligns with knowledge sharing ethics")
    
    return concept


def main():
    """Main function with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="CID Generator - Generate CIDs for knowledge concepts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                         # Process sample concept
  %(prog)s --concept-file knowledge.json  # Process external knowledge file

Requirements: dag-cbor, multiformats packages
Install: pip install dag-cbor multiformats
        """
    )
    
    parser.add_argument(
        "--concept-file",
        type=str,
        help="Path to JSON file containing knowledge concept",
        metavar="FILE"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"CID Generator v1.1.0"
    )
    
    parser.add_argument(
        "--educational-only",
        action="store_true",
        help="Validate that concept is for educational purposes"
    )
    
    args = parser.parse_args()
    
    generator = CIDGenerator()
    
    print("=" * 60)
    print("CADMIES CID GENERATOR v1.1.0")
    print(f"License: AGPLv3 with Commons Clause")
    print("=" * 60)
    
    concept = None
    source = "sample_concept"
    
    if args.concept_file:
        try:
            concept = read_concept_file(args.concept_file)
            source = f"external_file: {args.concept_file}"
            generator.external_file_path = args.concept_file
            
            print(f"\n📚 Processing knowledge file:")
            print(f"   Path: {args.concept_file}")
            
            if "title" in concept:
                print(f"   Title: {concept['title']}")
            if "human_id" in concept:
                print(f"   Human ID: {concept['human_id']}")
            
            if args.educational_only:
                metadata = concept.get("metadata", {})
                purpose = metadata.get("purpose", "")
                if purpose not in ["educational", "research", "personal_knowledge"]:
                    print(f"\n⚠️  ETHICAL NOTE: Concept purpose is '{purpose}'")
                    print("   Consider adding 'purpose': 'educational' to metadata")
                
        except FileNotFoundError as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"\n❌ Invalid JSON: {str(e)}")
            sys.exit(2)
        except ValueError as e:
            print(f"\n❌ Validation error: {str(e)}")
            sys.exit(3)
        except Exception as e:
            print(f"\n❌ Unexpected error reading file: {str(e)}")
            sys.exit(4)
    else:
        concept = create_sample_concept()
        source = "sample_concept (educational)"
        
        print(f"\n📚 Sample Educational Concept:")
        print(f"   Title: {concept['title']}")
        print(f"   Purpose: {concept['metadata'].get('purpose', 'educational')}")
        print(f"   License: {concept['metadata'].get('license', 'CC BY-SA 4.0')}")
    
    result = generator.generate_cid(concept)
    
    print(f"\n🧪 Processing: '{concept.get('title', 'Knowledge Concept')}'")
    
    if result["success"]:
        print(f"   📦 Serialized to {result['bytes_size']} bytes of DAG-CBOR")
        print(f"   🔐 Computed SHA2-256 hash: {result['hash_preview']}")
        print(f"   🎯 Generated CID: {result['cid']}")
        print(f"   📊 CID breakdown:")
        for key, value in result["cid_parts"].items():
            print(f"      - {key}: {value}")
    else:
        print(f"\n❌ CID generation failed:")
        for error in result["errors"]:
            print(f"   • {error}")
        sys.exit(5)
    
    if result["success"]:
        save_result = generator.save_to_blockstore(result, concept)
        
        if save_result["success"]:
            print(f"\n💾 Saved to knowledge store:")
            print(f"   Block: {save_result['block_path']}")
            print(f"   Index: Updated with '{save_result['human_id']}' → '{save_result['cid']}'")
            print(f"   Log: Operation recorded")
        else:
            print(f"\n⚠️  Knowledge store save failed (CID still generated):")
            for error in save_result.get("errors", ["Unknown error"]):
                print(f"   • {error}")
    
    print(f"\n📋 RESULT:")
    print(f"   Success: {result['success']}")
    if result["success"]:
        print(f"   CID: {result['cid']}")
        print(f"   Size: {result['bytes_size']} bytes")
        print(f"   Source: {source}")
    
    if result["success"]:
        deterministic = generator.test_determinism(concept)
        if not deterministic:
            print(f"\n⚠️  WARNING: Non-deterministic CIDs undermine trust in knowledge systems")
    
    print(f"\n✅ Knowledge address generated successfully!")
    print("   This CID will always point to this exact understanding.")
    print("   Shared knowledge → shared understanding → diminished ignorance")

if __name__ == "__main__":
    main()
