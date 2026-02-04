#!/usr/bin/env python3
"""
Simple core functionality test for CADMIES IPLD system.

This test verifies the basic operations work correctly:
1. Can generate a CID from a concept
2. Can read a concept by CID
3. Schema compliance is checked

Note: This is a demonstration/test version only.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_cid_generation():
    """Test that we can generate a CID from a simple concept."""
    print("Testing CID generation...")
    
    try:
        from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
        
        # Create a simple test concept
        test_concept = {
            "schema_version": "1.0.0",
            "human_id": "test_functionality_concept",
            "title": "Test Concept for Core Functionality",
            "definition": "This is a test concept to verify the system works.",
            "type": "Test",
            "domain": "Testing",
            "metadata": {
                "created": "2026-01-11T12:00:00Z",
                "creator": "Test System",
                "certainty_score": 0.9,
                "version": 1,
                "purpose": "testing"
            }
        }
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_concept, f)
            temp_file = f.name
        
        try:
            # Generate CID
            generator = CIDGenerator_v1_1_0()
            result = generator.generate_cid_from_file(temp_file)
            
            if result and "cid" in result:
                print(f"  ✓ CID generated: {result['cid'][:20]}...")
                print(f"  ✓ Human ID: {result.get('human_id', 'N/A')}")
                print(f"  ✓ Block stored: {result.get('block_path', 'N/A')}")
                return True
            else:
                print("  ✗ CID generation failed")
                return False
                
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_cbor_reading():
    """Test that we can read a concept back."""
    print("\nTesting CBOR reading...")
    
    try:
        # First, we need a CID to read. Use the conservation of energy example if available.
        # Check if we have the example file
        example_file = Path("physics_conservation_of_energy.json")
        
        if example_file.exists():
            # Generate the CID first
            from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
            generator = CIDGenerator_v1_1_0()
            result = generator.generate_cid_from_file(str(example_file))
            
            if result and "cid" in result:
                cid = result["cid"]
                
                # Now try to read it back
                from cbor_reader import CBORReader
                reader = CBORReader()
                
                concept = reader.read_cbor_file(cid)
                if concept and "title" in concept:
                    print(f"  ✓ Concept read successfully: {concept['title']}")
                    print(f"  ✓ Definition: {concept['definition'][:50]}...")
                    return True
                else:
                    print("  ✗ Failed to read concept")
                    return False
            else:
                print("  ✗ Could not generate CID from example file")
                return False
        else:
            print("  ⚠ Example file not found, trying to read any existing block...")
            
            # Try to read any existing .cbor file
            blocks_dir = Path("./blocks")
            if blocks_dir.exists():
                cbor_files = list(blocks_dir.glob("*.cbor"))
                if cbor_files:
                    cid = cbor_files[0].stem  # Get CID from filename
                    from cbor_reader import CBORReader
                    reader = CBORReader()
                    
                    concept = reader.read_cbor_file(cid)
                    if concept and "title" in concept:
                        print(f"  ✓ Read existing block: {concept['title']}")
                        return True
                    else:
                        print("  ✗ Failed to read existing block")
                        return False
                else:
                    print("  ⚠ No blocks found. Run CID generator first.")
                    return None  # Not a failure, just nothing to test
            else:
                print("  ⚠ blocks directory not found")
                return None
                
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_schema_validation():
    """Test that schema validation works."""
    print("\nTesting schema validation...")
    
    try:
        # Try to import the schema validation if it exists in the generator
        from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
        
        # Create a concept missing required fields
        invalid_concept = {
            "title": "Invalid Concept",
            "definition": "This is missing required fields"
            # Missing: schema_version, human_id, type, domain, metadata
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_concept, f)
            temp_file = f.name
        
        try:
            generator = CIDGenerator_v1_1_0()
            
            # This should fail due to missing required fields
            result = generator.generate_cid_from_file(temp_file)
            
            if result is None or "error" in str(result).lower():
                print("  ✓ Schema validation caught missing fields")
                return True
            else:
                print("  ✗ Schema validation should have failed")
                return False
                
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except Exception as e:
        # If validation fails as expected, that's actually success
        if "validation" in str(e).lower() or "schema" in str(e).lower():
            print(f"  ✓ Schema validation working: {e}")
            return True
        else:
            print(f"  ✗ Unexpected error: {e}")
            return False

def main():
    """Run all core functionality tests."""
    print("=" * 60)
    print("CADMIES IPLD - Core Functionality Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("CID Generation", test_cid_generation()))
    results.append(("CBOR Reading", test_cbor_reading()))
    results.append(("Schema Validation", test_schema_validation()))
    
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
    
    if passed == total:
        print("\n✅ All core functionality tests passed!")
        return 0
    else:
        print("\n⚠ Some tests failed or were skipped")
        print("   This may be expected if no example data exists yet.")
        return 1

if __name__ == "__main__":
    sys.exit(main())