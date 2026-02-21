# Quick Start Guide - 5 Minutes to Your First CID

## Prerequisites
- Python 3.8+ installed
- Basic command line familiarity

## Step 1: Clone Repository
```bash
git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES

Step 2: Install Dependencies
bash

pip install dag-cbor multiformats

Step 3: Run Built-in Example
bash

# This creates a sample concept and shows you the CID
python cid_generator_v1.1.0.py

Expected Output:
text

IPLD CID GENERATOR v1.1.0
==========================
📚 Sample Educational Concept:
   Title: Law of Conservation of Energy
...
🎯 Generated CID: bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji

Step 4: Read It Back
bash

# Use the CID from Step 3
python cbor_reader.py bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji

# Or use the human ID
python cbor_reader.py Physics:Law/ConservationOfEnergy

Step 5: Verify Determinism
bash

# Run the generator again - same CID should appear
python cid_generator_v1.1.0.py
# ✅ Same CID confirms deterministic system

🎉 Congratulations!

You've successfully:

    Generated a content-addressed identifier (CID)

    Stored knowledge in a local blockstore

    Retrieved it using the CID

    Verified the system works deterministically

Next Steps

    Detailed Installation - Custom setup options

    Use Cases - Practical applications

    Examples - More concept examples
