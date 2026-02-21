# Testing Guide - Verify Everything Works

## Why Test?
Content-addressed systems depend on **determinism** and **reliability**. These tests verify that:
- Same content → Same CID (determinism)
- CIDs can be reliably retrieved
- Schema validation works correctly
- Edge cases are handled properly

## Running Complete Test Suite
```bash
# Run all tests
python -m pytest tests/ -v

# Or run specific test modules
python tests/test_core_functionality.py
python tests/test_determinism.py
python tests/test_read_write_cycle.py

Test 1: Core Functionality
bash

python tests/test_core_functionality.py

Verifies:

    ✅ CID generation works

    ✅ CBOR reading works

    ✅ Schema validation functions

    ✅ File system operations work

Test 2: Determinism Verification
bash

python tests/test_determinism.py

Verifies:

    ✅ Same JSON → Same CID (critical for trust)

    ✅ Different JSON → Different CID

    ✅ Whitespace/formatting doesn't affect CID

    ✅ Field order doesn't affect CID

Test 3: Complete Read/Write Cycle
bash

python tests/test_read_write_cycle.py

Verifies:

    ✅ Write concept → Generate CID

    ✅ Save to blockstore

    ✅ Read back using CID

    ✅ Read back using human ID

    ✅ Retrieved content matches original

Test 4: Schema Validation
bash

python tests/test_schema_validation.py

Verifies:

    ✅ Valid concepts pass validation

    ✅ Invalid concepts are rejected

    ✅ Required fields are enforced

    ✅ Data types are correctly validated

Test 5: Example Validation
bash

python tests/test_example_concepts.py

Verifies:

    ✅ All examples in /examples/ are valid

    ✅ Examples generate CIDs correctly

    ✅ Examples can be retrieved

    ✅ Examples follow best practices

Manual Verification Steps
Step A: Create and Verify a Concept
bash

# 1. Create test concept
echo '{
  "schema_version": "1.0.0",
  "human_id": "test_concept",
  "title": "Test Concept",
  "definition": "A concept for testing",
  "type": "Test",
  "domain": "Testing",
  "metadata": {
    "created": "2026-01-07T12:00:00Z",
    "creator": "TestUser",
    "certainty_score": 0.9,
    "version": 1,
    "purpose": "testing"
  }
}' > test_concept.json

# 2. Generate CID
python cid_generator_v1.1.0.py --concept-file test_concept.json

# 3. Read back
python cbor_reader.py test_concept

# 4. Clean up
rm test_concept.json

Step B: Verify Blockstore Structure
bash

# Check what was created
ls -la blocks/
ls -la index/
ls -la logs/

# Verify index mapping
cat index/human_id_to_cid.json

Test Results Interpretation
All Tests Pass ✅

System is ready for production use. All core functionality verified.
Some Tests Fail ⚠️

Check:

    Dependencies: pip install dag-cbor multiformats

    Python version: python --version (needs 3.8+)

    File permissions in blocks/, index/, logs/ directories

    Schema file location: schemas/universal_scientific_concept_schema_v1.0.0.json

Critical Test Fails ❌

If determinism tests fail:

    System cannot be trusted for knowledge sharing

    Check for non-deterministic JSON serialization

    Verify DAG-CBOR encoding is consistent

Automated Testing (For Developers)
bash

# Add to your CI/CD pipeline
pytest tests/ --cov=. --cov-report=html

# Generate test coverage report
open htmlcov/index.html

Reporting Issues

If tests fail on your system:

    Run python --version

    Run pip list | grep -E "dag-cbor|multiformats"

    Check operating system details

    Email full output to: hieroscadmies@proton.me
