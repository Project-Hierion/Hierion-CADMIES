# Testing the CADMIES-IPLD System: A Complete Beginner's Guide

## Who This Guide Is For
- **Students** learning about technology
- **Teachers** who want to demonstrate content addressing
- **Researchers** exploring knowledge systems
- **Anyone** with basic computer skills

**No programming experience needed!**

## What You'll Need

### Hardware Requirements:
- A computer (Windows, Mac, or Linux)
- Internet connection (to download tools)
- About 50MB of free space

### Software Requirements:
1. **Python** (we'll install it if you don't have it)
2. **Command Line/Terminal** (comes with your computer)

**Don't worry if this sounds technical - we'll guide you through everything!**

---

## PART 1: Setting Up Your Computer

### Step 1: Open Your Command Line/Terminal

#### On Windows:
1. Press the `Windows Key` (between Ctrl and Alt)
2. Type `cmd` and press Enter
3. A black window appears - this is your Command Prompt

#### On Mac:
1. Press `Command + Space` (hold both keys)
2. Type "Terminal" and press Enter
3. A white/gray window appears - this is your Terminal

#### On Linux:
1. Press `Ctrl + Alt + T` (all three together)
2. A terminal window appears

---

### Step 2: Check if Python is Installed

In your terminal/command line, type this **exactly** and press Enter:
```bash
python --version
```
#### What should happen:

**Good outcome:** You see something like:
```text
Python 3.8.10
```
or
```text
Python 3.10.0
```
If you see this, you have Python! Skip to Step 4.
#
#
**Bad outcome:** You see something like:
```text
Python 2.7.18 (too old)
```
or
```text
'python' is not recognized...
```
or
```text
command not found
```
If you see this, you need to install Python. Go to Step 3.
#
#
### Step 3: Install Python (If Needed)

#### For Windows:

    - Open your web browser

    - Go to: https://www.python.org/downloads/

    - Click the big yellow "Download Python 3.12" button

    - Run the downloaded file

    - IMPORTANT: Check the box that says "Add Python to PATH"

    - Click "Install Now"

    - Wait for installation to finish

    - Close and reopen your Command Prompt

#### For Mac:

    - Open your web browser

    - Go to: https://www.python.org/downloads/macos/

    - Download "Python 3.12" for macOS

    - Run the downloaded file

    - Follow the installation steps

    - Close and reopen your Terminal

#### For Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

After installing: Go back to Step 2 to verify Python is installed.

### Step 4: Install Required Packages

In your terminal/command line, type this exactly and press Enter:
```bash
pip install dag-cbor multiformats nicegui pydantic python-dotenv aiofiles
```

#### What should happen:
You'll see text scrolling as packages download. It should end with:

"Successfully installed dag-cbor-X.X multiformats-X.X nicegui-X.X..."

#### If you get an error:
Try this instead:
```bash
python -m pip install dag-cbor multiformats nicegui pydantic python-dotenv aiofiles
```

## PART 2: Download and Test the Tools
### Step 5: Download the Tools

In your terminal/command line, type this exactly and press Enter:
```bash
git clone https://github.com/Hieros-CADMIES/CADMIES.git
```

#### What should happen:
```text
Cloning into 'CADMIES'...
remote: Enumerating objects: XX, done.
remote: Counting objects: 100% (XX/XX), done.
...
```

#### If you get an error about "git not found":

    - Download from: https://github.com/Hieros-CADMIES/CADMIES/archive/refs/heads/main.zip

    - Extract the ZIP file

    - Open the extracted folder

### Step 6: Enter the CADMIES Folder

In your terminal/command line, type this exactly and press Enter:
``bash
cd CADMIES/CADMIES-IPLD
``

#### What should happen:
You're now inside the CADMIES-IPLD folder. Type dir (Windows) or ls -la (Mac/Linux) to see the files.

## PART 3: Your First Test (CLI)
### Step 7: Run the CID Generator

In your terminal/command line, type this exactly and press Enter:
```bash
python tools/core/cid_generator_v1_1_0.py
```

#### What should happen:
You'll see a lot of text scrolling. Look for this line:
```text
🎯 Generated CID: bafyreib3eztwxtsbq66e6sihfkresdy4sqezvefytqnqzp22hlwvqppatu
```

**IMPORTANT**: Your CID might be different! That's okay! Just look for a line starting with 🎯 Generated CID: followed by a long string of letters and numbers.

### Step 8: Copy Your CID

Find the line that says 🎯 Generated CID: and copy the long string after it.

#### Example of what to copy:
```text
bafyreib3eztwxtsbq66e6sihfkresdy4sqezvefytqnqzp22hlwvqppatu
```

#### How to copy:

    - Click and drag your mouse to select the entire CID string

    - Right-click and choose "Copy"

    - Or press Ctrl+C (Windows) or Command+C (Mac)

### Step 9: Test the CBOR Reader

In your terminal/command line, type:
```bash
python tools/core/cbor_reader.py [YOUR_CID]
```

#### Example:
```bash
python tools/core/cbor_reader.py bafyreib3eztwxtsbq66e6sihfkresdy4sqezvefytqnqzp22hlwvqppatu
```

#### What should happen:
You'll see a nicely formatted display showing information about the "Law of Conservation of Energy" including:

    - The concept definition

    - Provenance sticky notes (who created it and when)

    - Relationships to other concepts

    - Difficulty levels (beginner/intermediate/expert)

### Step 10: Test by Human ID

Try looking up the concept by its human-readable name:
```bash
python tools/core/cbor_reader.py conservation_of_energy
```

#### What should happen:
The exact same information appears! The human ID is just an easier way to remember the concept.

### Step 11: Verify Determinism

Run the CID generator again:
```bash
python tools/core/cid_generator_v1_1_0.py
```

Look for the CID line again:
```text
🎯 Generated CID: bafyreib3eztwxtsbq66e6sihfkresdy4sqezvefytqnqzp22hlwvqppatu
```

#### IMPORTANT CHECK:
Is this CID ***exactly*** the same as the first one?

**YES - Same CID:** Perfect! The system works correctly.

**NO - Different CID:** Something is wrong. See troubleshooting below.

## PART 4: Your First Test (GUI)

CADMIES also includes a graphical interface for those who prefer clicking over typing.

### Step 12: Launch the GUI

In your terminal/command line:
```bash
cd cadmies-gui
python gui_main.py
```

#### What should happen:
```text
NiceGUI ready to go on http://localhost:8081
```

### Step 13: Open the GUI

- Open your web browser

- Go to: http://localhost:8081

You'll see the CADMIES Dashboard with:

- System status

- Concept count (should be 20+ concepts)

- Recent activity

- A sidebar with navigation links

### Step 14: Explore the GUI

#### Browse Concepts:

- Click "Browse Library" in the sidebar

- See all 20+ concepts in grid or list view

- Click "View" on any concept to see details including provenance sticky notes

#### View the Mycelium Map:

- Click "Mycelium Map" in the sidebar

- See the interactive knowledge graph (173+ nodes, 160+ edges)

- Click any node to see concept names

- Type cadmies anywhere on the map for a surprise 🎸

#### Add a Concept:

- Click "Add Concept" in the sidebar

- Fill in the form (name, type, domain, description)

- Click out of each field to see the live preview update

- Click "Generate CID & Store"

- Your new concept gets a deterministic CID and auto-provenance

## PART 5: What Was Created

The system created these folders on your computer:
```text

CADMIES-IPLD/
├── store/
│   ├── blocks/           # IPLD blocks (named by CID)
│   ├── index/            # human_id → CID mappings
│   └── logs/             # Operation history (audit trail)
├── tools/core/           # CLI tools
└── cadmies-gui/          # Web interface
```

**🎉 CONGRATULATIONS!**

You've successfully:

- ✅ Set up Python and installed packages

- ✅ Downloaded the CADMIES-IPLD system

- ✅ Created your first CID (deterministic content address)

- ✅ Retrieved knowledge using CID and human ID

- ✅ Verified determinism (same content → same CID)

- ✅ Launched and explored the GUI

- ✅ Viewed the Mycelium Map knowledge graph

**You now have a working content-addressed knowledge system with provenance tracking!**

### Additional Tests You Can Try

#### Test A: List All Stored Concepts
```bash
python tools/core/cbor_reader.py --list
```

#### Test B: View Provenance History
```bash
python tools/core/cbor_reader.py conservation_of_energy
# Look for the "📜 PROVENANCE STICKY NOTES" section
```

#### Test C: Check the Audit Trail
```bash
cat store/logs/operations.jsonl | tail -10
```

#### Test D: Create Your Own Concept

- Create a file called my_concept.json:

```json

{
  "schema_version": "1.0.0",
  "human_id": "my_test_concept",
  "title": "My First Test",
  "definition": "This is my first knowledge concept",
  "type": "TestConcept",
  "domain": "Testing",
  "subdomain": "Beginner",
  "metadata": {
    "creator": "Me",
    "certainty_score": 0.8,
    "version": 1,
    "license": "CC BY-SA 4.0",
    "purpose": "educational"
  }
}
```

- Generate its CID:

```bash
python tools/core/cid_generator_v1_1_0.py --concept-file my_concept.json
```

- Retrieve it:

```bash
python tools/core/cbor_reader.py my_test_concept
```

## Troubleshooting Guide
Problem	Solution
#
"python not found"	Try python3 instead of python in all commands
#
"pip not found"	Try python -m pip install instead
#
Different CIDs each time	This is serious! The system must be deterministic. Check if any files changed or if you're running different commands.
#
"Module not found: dag_cbor"	Run pip uninstall dag-cbor multiformats then pip install dag-cbor multiformats --upgrade
#
"CADMIES System Not Found" in GUI	Make sure you're running the GUI from cadmies-gui/ folder
#
Permission errors (Mac/Linux)	Try sudo pip install dag-cbor multiformats
#
#
## Success Checklist

- Opened terminal/command line

- Verified Python 3.8+ is installed

- Installed required packages

- Downloaded CADMIES via git clone

- Ran cid_generator_v1_1_0.py

- Found and copied the CID

- Ran cbor_reader.py with your CID

- Saw the knowledge display with provenance

- Verified same CID on second run

- Launched the GUI

- Explored the Mycelium Map

If you checked all boxes, you've successfully tested the CADMIES-IPLD system!

## What You Just Demonstrated

Concept	What It Means
#
Content Addressing	Knowledge gets a permanent address based on its content
#
Determinism	Same content → Same address every time
#
Provenance	Every concept has a sticky note showing who created it and when
#
Verifiability	Anyone with the CID can verify they have the exact same content
#
Local Storage	Everything stays on your computer - no cloud needed
#
Mycelial Growth	Concepts connect to form a knowledge graph

This is how trustworthy knowledge systems work!


## Next Steps

### If You Want to Learn More:

- Read the README.md

- Explore the CID Structure Specification

- Browse the source_concepts/ folder for PhD-level examples

### If You're a Teacher:

- Have students run through this guide

- Compare CIDs - everyone should get the same result!

- Discuss why determinism and provenance matter for knowledge systems

### If You're a Researcher:

- Study the schemas/ folder for data structures

- Create concepts for your research domain

- Use the Mycelium Map to discover connections

## Need Help?

### If you get stuck:

- Check the error message - copy it exactly

- Note what step you were on

- Email: hieroscadmies@proton.me

### Include:

- Your operating system (Windows/Mac/Linux)

- Python version (from Step 2)

- The exact error message

- What you were trying to do

**"The same understanding should always have the same address."**

**Let the mycelium grow! 🌱**
