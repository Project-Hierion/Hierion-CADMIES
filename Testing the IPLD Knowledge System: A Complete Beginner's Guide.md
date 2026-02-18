# Testing the IPLD Knowledge System: A Complete Beginner's Guide

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

**Don't worry if these sound technical - we'll guide you through everything!**

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

What should happen:

Good outcome: You see something like:
```text
Python 3.8.10
```

or

```text
Python 3.10.0
```
If you see this, you have Python! Skip to Step 4.

Bad outcome: You see:
```text
    Python 2.7.18 (too old)
or
    'python' is not recognized...
or
    command not found
```

If you see this, you need to install Python. Go to Step 3.

### Step 3: Install Python (If Needed)

**For Windows:**

   - Open your web browser

   - Go to: https://www.python.org/downloads/

   - Click the big yellow "Download Python 3.12" button

   - Run the downloaded file

    **IMPORTANT:** Check the box that says "Add Python to PATH"

   - Click "Install Now"

   - Wait for installation to finish

   - Close and reopen your Command Prompt

**For Mac:**

   - Open your web browser

   - Go to: https://www.python.org/downloads/macos/

   - Download "Python 3.12" for macOS

   - Run the downloaded file

   - Follow the installation steps

   - Close and reopen your Terminal

**For Linux (Ubuntu/Debian):**

In your terminal, type:
```bash

sudo apt update
sudo apt install python3 python3-pip
```

After installing: Go back to Step 2 to verify Python is installed.

### Step 4: Install Required Packages

In your terminal/command line, type this exactly and press Enter:
```bash

pip install dag-cbor multiformats
```

What should happen:
You'll see text scrolling as packages download. It should end with:

"Successfully installed dag-cbor-X.X multiformats-X.X"

If you get an error:
Try this instead:
```bash

python -m pip install dag-cbor multiformats
```

## PART 2: Download and Test the Tools

### Step 5: Download the Tools

In your terminal/command line, type this exactly and press Enter:
```bash

git clone https://github.com/Hieros-CADMIES/CADMIES.git
```

What should happen:
You'll see something like:
```text

Cloning into 'CADMIES'...
remote: Enumerating objects: XX, done.
remote: Counting objects: 100% (XX/XX), done.
remote: Compressing objects: 100% (XX/XX), done.
remote: Total XX (delta XX), reused XX (delta XX), pack-reused XX
Receiving objects: 100% (XX/XX), XX KiB | XX KiB/s, done.
```

If you get an error about "git not found":

   - Download from: https://github.com/Hieros-CADMIES/CADMIES/archive/refs/heads/main.zip

   - Extract the ZIP file

   - Open the extracted folder

### Step 6: Enter the Tools Folder

In your terminal/command line, type this exactly and press Enter:
```bash

cd CADMIES
```

What should happen:
You're now inside the tools folder. You can type dir (Windows) or ls (Mac/Linux) to see the files.

## PART 3: Your First Test

### Step 7: Run the CID Generator

In your terminal/command line, type this exactly and press Enter:
```bash

python cid_generator_v1.1.0.py
```

What should happen:
You'll see a lot of text scrolling. Look for this line (it might be near the bottom):
```text

Generated CID: bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji
```

**IMPORTANT:** Your CID might be different! That's okay! Just look for a line starting with 🎯 Generated CID: followed by a long string of letters and numbers.

### Step 8: Copy Your CID

Find the line that says 🎯 Generated CID: and copy the long string after it.

Example of what to copy:
```text

bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji
```

**How to copy:**

   - Click and drag your mouse to select the entire CID string

   - Right-click and choose "Copy"

   - Or press Ctrl+C (Windows) or Command+C (Mac)

### Step 9: Test the CBOR Reader

In your terminal/command line, type this exactly:
```bash

python cbor_reader.py bafyreifh5f5i6elunhcqfuw7n2t3c2rl4jbrdkjlfh5lhlkjh3jkh6lkjsdf
```

***But wait! Replace the example CID with your actual CID that you copied.***

Example:
If your CID was bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji, type:
```bash

python cbor_reader.py bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji
```

What should happen:
You'll see a nicely formatted display showing information about the *"Law of Conservation of Energy."*

### Step 10: Test Again (Verify Determinism)

In your terminal/command line, type this exactly and press Enter:
```bash

python cid_generator_v1.1.0.py
```

Look for the CID line again:
```text

🎯 Generated CID: bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji
```

**IMPORTANT CHECK:**
Is this CID ***exactly*** the same as the first one?

YES - Same CID: Perfect! The system works correctly.
NO - Different CID: Something is wrong. Try the troubleshooting steps below.

**🎉 CONGRATULATIONS!**

You've successfully:

    ✅ Set up Python on your computer

    ✅ Installed the required packages

    ✅ Downloaded the IPLD knowledge tools

    ✅ Created your first content-addressed identifier (CID)

    ✅ Retrieved knowledge using that CID

    ✅ Verified the system is deterministic (same content → same CID)

**You now have a working content-addressed knowledge system!**

**What Was Created?**

The system created three folders on your computer:
Check what was created:

In your terminal/command line, type:

On Windows:
```bash

dir
```

On Mac/Linux:
```bash

ls -la
```

You should see:
```text

blocks/    (Contains the encoded knowledge)
index/     (Contains the human-readable index)
logs/      (Contains operation history)
```

**Additional Tests You Can Try**

Test A: List All Stored Concepts
```bash

python cbor_reader.py --list
```

Test B: Try the Human-Readable ID
```bash

python cbor_reader.py Physics:Law/ConservationOfEnergy
```

Test C: Create Your Own Concept

   - Open Notepad (Windows) or TextEdit (Mac)

   - Copy this text:
```json

{
  "schema_version": "1.0.0",
  "human_id": "my_test_concept",
  "title": "My First Test",
  "definition": "This is my first knowledge concept",
  "type": "Test",
  "domain": "Testing",
  "metadata": {
    "created": "2026-01-08T10:00:00Z",
    "creator": "Me",
    "certainty_score": 0.8,
    "version": 1,
    "purpose": "testing"
  }
}
```

   - Save it as my_test.json in the CADMIES folder

   - In your terminal:
```bash

python cid_generator_v1.1.0.py --concept-file my_test.json

python cbor_reader.py my_test_concept
```

**Troubleshooting Guide**

- **Problem 1:** "python not found"

--**Solution:** Python isn't in your PATH. Try:
```bash

python3 --version
```

If that works, use python3 instead of python in all commands.

-**Problem 2:** "pip not found"

--**Solution:** Try:
```bash

python -m pip install dag-cbor multiformats
```

-**Problem 3:** Different CIDs each time

--**Solution:** **This is serious!** **The system must be deterministic.**
``text
Check:

    Are you running the exact same command?

    Did any files change?

    Try restarting and running just the basic test again.
``

-**Problem 4:** "Module not found: dag_cbor"

--**Solution:** The installation failed. Try:
```bash

pip uninstall dag-cbor multiformats

pip install dag-cbor multiformats --upgrade
```

-**Problem 5:** Permission errors

--**Solution:** On Mac/Linux, try:
```bash

sudo pip install dag-cbor multiformats
```

**Next Steps**
```text
If You Want to Learn More:

    Read the README.md file in the CADMIES folder

    Look at the examples/ folder for more concepts

    Read docs/USER_MANUAL.md for complete documentation
```
```text
If You're a Teacher:

    Have students run through this guide

    Compare CIDs - everyone should get the same result!

    Discuss why determinism is important for knowledge systems
```
```text
If You're a Researcher:

    Study the schemas/ folder for the data structure

    Examine the test files in tests/

    Create concepts for your research domain
```

**Need Help?**
```text
If you get stuck:

    Check the error message - copy it exactly

    Note what step you were on

    Email: hieroscadmies@proton.me

Include:

    Your operating system (Windows/Mac/Linux)

    Python version (from Step 2)

    The exact error message

    What you were trying to do
```

**Success Checklist**
```text
    Opened terminal/command line

    Verified Python 3.8+ is installed

    Installed dag-cbor and multiformats

    Downloaded the CADMIES tools

    Ran python cid_generator_v1.1.0.py

    Found and copied the CID

    Ran python cbor_reader.py [YOUR_CID]

    Saw the knowledge display

    Verified same CID on second run
```
If you checked all boxes, you've successfully tested the system!


**What You Just Demonstrated**

    Content Addressing: Knowledge gets a permanent address based on its content

    Determinism: Same content → Same address every time

    Verifiability: Anyone with the CID can verify they have the exact same content

    Local Storage: Everything stays on your computer - no cloud needed

This is how trustworthy knowledge systems work!

***"The same understanding should always have the same address."***

***Let the mycelium grow!*** 🌱
