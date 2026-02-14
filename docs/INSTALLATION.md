# Detailed Installation Guide
## System Requirements
### Minimum Requirements

    Operating System: Linux, macOS, or Windows with WSL2
    Python: 3.8 or higher
    Storage: 50MB free space
    Memory: 512MB RAM

### Recommended Requirements

    Python: 3.10 or higher
    Storage: 500MB for extensive knowledge bases
    Memory: 2GB+ RAM for large operations

## Installation Methods

### Method 1: Basic Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package in development mode
pip install -e .

# 5. Verify installation
python -c "from cadmies_demo import CIDGenerator_v1_1_0; print('✅ Package installed successfully')"

Method 2: Development Installation
bash

# Clone with all branches
git clone --recursive https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run test suite to verify
python -m pytest tests/ -v

Method 3: Docker Installation (Advanced)
dockerfile

# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt && pip install -e .
CMD ["python", "-c", "from cadmies_demo import CIDGenerator_v1_1_0; print('✅ Ready')"]

Configuration
Directory Structure

After first run, the system creates:
text

./
├── blocks/          # CBOR-encoded knowledge blocks
├── index/           # Human ID to CID mapping
├── logs/            # Operation logs
└── schemas/         # Schema definitions

Environment Variables (Optional)
bash

# Custom storage paths
export IPLD_BLOCKS_DIR="/path/to/blocks"
export IPLD_INDEX_DIR="/path/to/index"
export IPLD_LOGS_DIR="/path/to/logs"

# Verbose logging
export IPLD_VERBOSE="true"

Verification
Test 1: Basic Functionality
bash

# Generate a sample concept using the installed package
python -c "
from cadmies_demo import CIDGenerator_v1_1_0
generator = CIDGenerator_v1_1_0()
print('✅ Generator created successfully')
"

# Check directories were created
ls -la blocks/ index/ logs/

Test 2: Read/Write Cycle
bash

# Create a simple test concept
cat > test_concept.json << 'EOF'
{
  "schema_version": "1.0.0",
  "human_id": "test_installation",
  "title": "Installation Test",
  "definition": "Testing the installation",
  "type": "Test",
  "domain": "Testing",
  "metadata": {
    "created": "2026-01-07T12:00:00Z",
    "creator": "TestUser",
    "certainty_score": 0.9,
    "version": 1,
    "purpose": "testing"
  }
}
EOF

# Generate CID using the package
python -c "
from cadmies_demo import CIDGenerator_v1_1_0
import json

with open('test_concept.json') as f:
    concept = json.load(f)
    
generator = CIDGenerator_v1_1_0()
result = generator.generate_cid(concept)
print(f'CID: {result[\"cid\"]}')
"

# Read it back
python -c "
from cadmies_demo import CBORReader
reader = CBORReader()
concept = reader.read_cbor_file('test_installation')
print(f'Retrieved: {concept[\"title\"]}')
"

# Clean up
rm test_concept.json

Test 3: Schema Validation
bash

# Verify schema file exists
ls -la schemas/universal_scientific_concept_schema_v1.0.0.json

# Check schema is valid JSON
python -m json.tool schemas/universal_scientific_concept_schema_v1.0.0.json > /dev/null && echo "✅ Schema is valid JSON"

Platform-Specific Notes
Linux/Mac
bash

# Ensure Python is installed
python3 --version

# Install pip if missing
sudo apt-get install python3-pip  # Debian/Ubuntu
brew install python3              # macOS

Windows (WSL2 Recommended)
bash

# Enable WSL2
wsl --install

# Install Python in WSL
sudo apt update
sudo apt install python3 python3-pip

# Continue with Method 1 above

Windows Native (Not Recommended)
powershell

# Install Python from python.org
# Add Python to PATH during installation

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Note: Some features may require WSL2 for full compatibility

Troubleshooting Installation
Common Issues

Issue: "Command not found: python"
bash

# Try python3 instead
python3 --version
python3 -c "from cadmies_demo import CIDGenerator_v1_1_0"

Issue: "Module not found: dag_cbor"
bash

# Reinstall with pip
pip uninstall dag-cbor multiformats -y
pip install -r requirements.txt --upgrade

Issue: Permission denied creating directories
bash

# Check current directory permissions
ls -la .

# Create directories manually if needed
mkdir -p blocks index logs

Issue: Python version too old
bash

# Check Python version
python --version

# Install Python 3.8+ if needed
# Ubuntu/Debian: sudo apt install python3.10
# macOS: brew install python@3.10
# Windows: Download from python.org

Next Steps

After successful installation:
text

Run the test suite to verify everything works:
```bash
python -m pytest tests/ -v
```

Explore examples in the `examples/` directory

Read the user manual for complete documentation

For additional help: hieroscadmies@proton.me
