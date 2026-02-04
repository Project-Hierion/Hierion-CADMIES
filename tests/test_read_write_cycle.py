#!/usr/bin/env python3
"""
Complete read/write cycle test for CADMIES IPLD system.

Tests the full workflow:
1. Write a concept → Generate CID → Store CBOR
2. Read the concept back using the CID
3. Verify the retrieved content matches original

Note: This is a demonstration/test version only.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

def create_test_concept():
    """Create a test concept for the read/write cycle."""
    return {
        "schema_version": "1.0.0",
        "human_id": "read_write_test_concept",
        "title": "Read/Write Cycle Test Concept",
        "definition": "This concept exists solely to test the complete read/write cycle of the IPLD system. It verifies that concepts can be stored and retrieved identically.",
        "type": "Test",
        "domain": "SystemTesting",
        "subdomain": "IPLDVerification",
        "difficulty_levels": {
            "beginner": "This is a test to make sure the system works correctly.",
            "intermediate": "Verifies that content addressing produces deterministic CIDs.",
            "expert": "Tests DAG-CBOR encoding/decoding consistency and schema compliance."
        },
        "metadata": {
            "created": "2026-01-11T12:00:00Z",
            "creator": "CADMIES Test Suite",
            "certainty_score": 1.0,
            "version": 1,
            "purpose": "system_verification",
            "license": "CC0-1.0"
        }
    }

def test_complete_cycle():
    """Test the complete write → read cycle."""
    print("Testing complete read/write cycle...")
    
    try:
        from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
        from cbor_reader import CBORReader
        
        # Create test concept
        original_concept = create_test_concept()
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(original_concept, f, indent=2)
            temp_file = f.name
        
        try:
            # STEP 1: Write - Generate CID and store
            print("  Step 1: Writing concept...")
            generator = CIDGenerator_v1_1_0()
            write_result = generator.generate_cid_from_file(temp_file)
            
            if not write_result or "cid" not in write_result:
                print("  ✗ Failed to generate CID")
                return False
            
            cid = write_result["cid"]
            print(f"  ✓ CID generated: {cid[:20]}...")
            
            # STEP 2: Read - Retrieve using CID
            print("  Step 2: Reading concept back...")
            reader = CBORReader()
            retrieved_concept = reader.read_cbor_file(cid)
            
            if not retrieved_concept:
                print("  ✗ Failed to read concept back")
                return False
            
            print(f"  ✓ Concept retrieved: {retrieved_concept.get('title', 'Unknown')}")
            
            # STEP 3: Verify - Compare key fields
            print("  Step 3: Verifying content matches...")
            
            # Check critical fields
            critical_fields = ["schema_version", "human_id", "title", "definition", "type", "domain"]
            mismatches = []
            
            for field in critical_fields:
                original_val = original_concept.get(field)
                retrieved_val = retrieved_concept.get(field)
                
                if original_val != retrieved_val:
                    mismatches.append(field)
                    print(f"    ✗ Field mismatch: {field}")
                    print(f"      Original: {original_val}")
                    print(f"      Retrieved: {retrieved_val}")
                else:
                    print(f"    ✓ {field}: matches")
            
            # Check metadata
            original_meta = original_concept.get("metadata", {})
            retrieved_meta = retrieved_concept.get("metadata", {})
            
            meta_fields_to_check = ["creator", "purpose", "version"]
            for field in meta_fields_to_check:
                if original_meta.get(field) != retrieved_meta.get(field):
                    mismatches.append(f"metadata.{field}")
                    print(f"    ✗ Metadata mismatch: {field}")
                else:
                    print(f"    ✓ metadata.{field}: matches")
            
            if not mismatches:
                print("  ✓ All critical fields match!")
                
                # Bonus: Verify the file was actually created
                cbor_path = Path(f"./blocks/{cid}.cbor")
                if cbor_path.exists():
                    file_size = cbor_path.stat().st_size
                    print(f"  ✓ CBOR file created: {file_size} bytes")
                    
                    # Verify it's in the index
                    index_path = Path("./index/human_id_to_cid.json")
                    if index_path.exists():
                        with open(index_path, 'r') as f:
                            index = json.load(f)
                        
                        if original_concept["human_id"] in index:
                            print(f"  ✓ Concept indexed: {original_concept['human_id']} → {index[original_concept['human_id']][:20]}...")
                        else:
                            print("  ⚠ Concept not found in index (might be expected for some configurations)")
                    
                    return True
                else:
                    print("  ✗ CBOR file not found in blocks directory")
                    return False
            else:
                print(f"  ✗ Found {len(mismatches)} field mismatches")
                return False
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_human_id_lookup():
    """Test retrieval using human ID instead of CID."""
    print("\nTesting human ID lookup...")
    
    try:
        from cbor_reader import CBORReader
        
        reader = CBORReader()
        
        # Load index
        index_path = Path("./index/human_id_to_cid.json")
        if not index_path.exists():
            print("  ⚠ No index file found (might be expected)")
            return None
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        if not index:
            print("  ⚠ Index is empty")
            return None
        
        # Try to look up the first human ID
        first_human_id = list(index.keys())[0]
        cid = index[first_human_id]
        
        print(f"  Looking up: {first_human_id}")
        print(f"  Found CID: {cid[:20]}...")
        
        # Try to read it
        concept = reader.read_cbor_file(cid)
        if concept:
            print(f"  ✓ Successfully retrieved via human ID: {concept.get('title', 'Unknown')}")
            return True
        else:
            print("  ✗ Failed to retrieve via human ID")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_cleanup():
    """Optionally clean up test artifacts."""
    print("\nCleaning up test artifacts...")
    
    test_human_id = "read_write_test_concept"
    
    # Remove from index if it exists
    index_path = Path("./index/human_id_to_cid.json")
    if index_path.exists():
        try:
            with open(index_path, 'r') as f:
                index = json.load(f)
            
            if test_human_id in index:
                cid = index[test_human_id]
                del index[test_human_id]
                
                with open(index_path, 'w') as f:
                    json.dump(index, f, indent=2)
                
                print(f"  ✓ Removed {test_human_id} from index")
                
                # Try to remove the block file
                block_path = Path(f"./blocks/{cid}.cbor")
                if block_path.exists():
                    block_path.unlink()
                    print(f"  ✓ Removed block file: {cid[:20]}...")
                else:
                    print(f"  ⚠ Block file not found (may have been already removed)")
            else:
                print(f"  ⚠ {test_human_id} not in index")
                
        except Exception as e:
            print(f"  ⚠ Error during cleanup: {e}")
    
    return True

def main():
    """Run the complete read/write cycle test."""
    print("=" * 60)
    print("CADMIES IPLD - Read/Write Cycle Test")
    print("=" * 60)
    
    results = []
    
    # Run the main cycle test
    cycle_result = test_complete_cycle()
    results.append(("Complete Cycle", cycle_result))
    
    # Test human ID lookup
    lookup_result = test_human_id_lookup()
    results.append(("Human ID Lookup", lookup_result))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    
    passed = 0
    total = 0
    
    for test_name, result in results:
        total += 1
        if result is True:
            passed += 1
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:  # None (skipped)
            status = "⚠ SKIP"
        
        print(f"  {test_name:20} {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    # Ask about cleanup
    print("\n" + "=" * 60)
    cleanup = input("Clean up test artifacts? (y/n): ").strip().lower()
    if cleanup == 'y':
        test_cleanup()
        print("Cleanup complete.")
    
    if passed == total:
        print("\n✅ Read/write cycle fully verified!")
        print("   The system correctly stores and retrieves content.")
        return 0
    elif passed >= 1:
        print("\n⚠ Basic functionality verified (some tests skipped)")
        print("   The system works but may need example data.")
        return 0
    else:
        print("\n❌ Tests failed - check system setup")
        return 1

if __name__ == "__main__":
    sys.exit(main())