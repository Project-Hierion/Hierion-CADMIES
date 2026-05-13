---
File: scientific_documentation_creation_guide_20260121.md
Author: Digital Intelligence Research Division - Project Hieros
Created: 2026-01-21
Version: 1.1.0
System: CADMIES Documentation Framework
Document_ID: CA-2026-021-GUIDE
Classification: INTERNAL - DOCUMENTATION TEAM USE ONLY
Status: ACTIVE GUIDE
Reviewers: [Technical Lead, Quality Assurance]
Modified: 2026-05-12
Related_Docs: 
  - 2025-12-22_template_technical_audit_execution_v1.0.0.md
  - template_technical_audit_execution_v1.0.0.md
  - Technical_Audit_Execution_Template_v1.0.0.md
Consolidated_From:
  - 2025-12-22_guide-cadmies_scientific_documentation_creation_v1.1.0.md
  - 2025-12-22_guide-cadmies_scientific_documentation_creation_v1.0.0.md  
  - CADMIES - Scientific Documentation Creation Guide v1.0.0 Dec 2025
Processing_Notes: Consolidated three variant documents into single NASA-standard version on 2026-01-21
Scientific Rigor Note: Enhanced YAML frontmatter for improved metadata tracking
---

CADMIES - Scientific Documentation Creation Guide
Interactive, scientific-grade documentation system with LaTeX/PDF generation.
Create, edit, manage, and version-control technical documentation with NASA-level rigor.

NOW WITH: Template Library, Evidence Management, Metadata Standards, Version Control, Quality Checklists, Diagram Standards, and Scientific Workflow Automation

## Table of Contents

1.0 PURPOSE AND SCOPE
2.0 PREREQUISITES AND APPLICABLE SYSTEMS
3.0 PROCEDURE: STEP-BY-STEP WORKFLOW
4.0 DOCUMENT TYPES AND TEMPLATES
5.0 EVIDENCE MANAGEMENT PROTOCOL
6.0 QUALITY ASSURANCE CHECKLISTS
7.0 TROUBLESHOOTING (BATTLE-TESTED)
8.0 BEST PRACTICES AND STANDARDS
9.0 QUICK REFERENCE CARD
APPENDIX A: TEMPLATE LIBRARY
APPENDIX B: METADATA STANDARDS
APPENDIX C: VERSION HISTORY AND CONSOLIDATION NOTES

## 1.0 PURPOSE AND SCOPE

### 1.1 Purpose
This guide provides a complete, proven workflow for creating scientific-grade documentation from initial text entry to professional PDF output.

### 1.2 Scope
Based on battle-tested experience from the Cosmium Angelo ecosystem and enhanced with **CADMIES (Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem)** audit framework methodologies.

## 2.0 PREREQUISITES AND APPLICABLE SYSTEMS

### 2.1 Toolbox Environment

```text
documentation-tools container with:
- Pandoc 3.1.9+
- LaTeX (TeX Live)
- XeLaTeX engine
- Listings package support
```

### 2.2 Storage Structure
text

/var/mnt/la_mansion/documentation/
├── templates/              # Document templates
├── evidence/              # Audit/validation evidence
│   ├── commands/          # Command output captures
│   ├── screenshots/       # System state images
│   └── logs/             # Reference logs
├── drafts/               # Working documents
├── published/            # Final versions
└── archives/             # Version history

### 2.3 Text Editor Requirements

    VS Code, Notepad++, or any plain text editor

    UTF-8 encoding support

    Line ending: LF (Unix)

### 2.4 Silverblue Toolbox Setup (Fedora Silverblue Only)

If you're using Fedora Silverblue, all documentation tools must be installed in a toolbox:
2.4.1 Check for Existing Toolbox
bash

toolbox list | grep documentation-tools

#### 2.4.2 Create Toolbox (If Needed)
```bash

toolbox create --image fedora-toolbox:43 documentation-tools
toolbox enter documentation-tools
```

#### 2.4.3 Install Required Packages Inside Toolbox

Once inside the toolbox:
bash

sudo dnf install -y pandoc pandoc-citeproc
sudo dnf install -y texlive-scheme-medium texlive-listings texlive-geometry texlive-fontspec
sudo dnf install -y liberation-fonts liberation-mono-fonts

#### 2.4.4 Verify Installation
```bash

pandoc --version
xelatex --version
kpsewhich listings.sty
```
#### 2.4.5 Exit and Re-enter When Needed

To leave the toolbox:
```bash

exit
```

To re-enter later:
```bash

toolbox enter documentation-tools
```
## 3.0 PROCEDURE: STEP-BY-STEP WORKFLOW
### 3.1 Step 1: Document Type Selection

Consult Document Types Reference (Section 4.0)
Choose appropriate template from /templates/
Example: For audit reports → template_audit_report.md

IMPORTANT FOR SILVERBLUE USERS:
All commands in Sections 3.4 through 3.7 must be executed from within the documentation-tools toolbox. Begin with:
```bash

toolbox enter documentation-tools
cd /var/mnt/la_mansion/documentation/drafts/
```
Then proceed with the workflow steps.

### 3.2 Step 2: Create Source Content
Method A: Direct Text Entry (Recommended)

Open template and follow scientific formatting:
markdown

# Main Title
## Section Heading
### Subsection
- Bullet points with `code` examples
1. Numbered procedures

Formatting Standards:

    Use # for headings only (not in diagrams)

    Code blocks: triple backticks with language specifier

    Diagrams: ASCII only (+, |, -, >)

    No emojis, box characters, or smart quotes

Method B: LibreOffice Drafting
bash

toolbox enter documentation-tools
pandoc "draft.odt" -o "$(date +%Y-%m-%d)_project_name.md"

3.3 Step 3: Apply Metadata Header

Every document must include:
yaml

---
System: [System Name]
Document_ID: [CA-YYYY-NNN-TYPE]
Version: [X.Y.Z]
Classification: [INTERNAL|CONFIDENTIAL|PUBLIC]
Author: [Name/Role]
Reviewers: [Name1, Name2]
Status: [DRAFT|REVIEW|FINAL|ACTIVE]
Created: [YYYY-MM-DD]
Modified: [YYYY-MM-DD]
Related_Docs: [DOC-ID-1, DOC-ID-2]
---

### 3.4 Step 4: Pre-Conversion Quality Check
```bash

# Enter documentation environment
toolbox enter documentation-tools
cd /var/mnt/la_mansion/documentation/drafts/

# Check for problematic characters
grep -n "[����#]" "your_document.md"
grep -n "["""']" "your_document.md"  # Smart quotes

# Validate structure
head -20 "your_document.md" | grep -E "^#|^---"
```

### 3.5 Step 5: Generate Scientific PDF
```bash

pandoc "2025-12-22_cadmies_audit_report.md" -o "2025-12-22_cadmies_audit_report.pdf" \
  --table-of-contents \
  --number-sections \
  --pdf-engine=xelatex \
  --listings \
  -V geometry:margin=2.5cm \
  -V mainfont="Liberation Sans" \
  -V monofont="Liberation Mono" \
  -V linestretch=1.5 \
  -V papersize=a4 \
  -V documentclass=report
```
### 3.6 Step 6: Version Control
```bash

# Archive previous version
cp "2025-12-22_cadmies_audit_v1.0.md" "archives/v1.0/"
cp "2025-12-22_cadmies_audit_v1.0.pdf" "archives/v1.0/"

# Update working version
mv "2025-12-22_cadmies_audit_v1.1.md" "2025-12-22_cadmies_audit_v1.2.md"
```

### 3.7 Step 7: Final Verification
```bash

# Check PDF was created
ls -la "2025-12-22_cadmies_audit_report.pdf"

# Verify file integrity
file "2025-12-22_cadmies_audit_report.pdf"

# Check page count (if needed)
pdftk "2025-12-22_cadmies_audit_report.pdf" dump_data | grep NumberOfPages
```

## 4.0 DOCUMENT TYPES AND TEMPLATES
### 4.1 Document Type Reference Table
```yaml
Document Type	When to Use	Template	Example File Name
Audit Report	System assessment, compliance checks	template_audit_report.md	2025-12-22_cadmies_technical_audit.md
Architecture Spec	System design, component mapping	template_architecture_spec.md	2025-12-22_cadmies_architecture_v1.1.md
Runbook	Operational procedures, recovery steps	template_runbook.md	2025-12-22_backup_recovery_runbook.md
Postmortem	Incident analysis, root cause	template_postmortem.md	2025-12-22_ollama_service_outage.md
Research Note	Experimental findings, observations	template_research_note.md	2025-12-22_mistral_hog_integration.md
System Manual	User guides, administration	template_system_manual.md	2025-12-22_abigail_user_manual.md
```

### 4.2 Template Structure Example
```markdown

# TEMPLATE: Audit Report
# Location: /var/mnt/la_mansion/documentation/templates/template_audit_report.md

---
System: [System Name]
Document_ID: [CA-YYYY-NNN-AUDIT]
Version: [1.0.0]
Classification: INTERNAL
Author: [Auditor Name]
Reviewers: [Technical Lead, Security Officer]
Status: DRAFT
Created: [YYYY-MM-DD]
Modified: [YYYY-MM-DD]
Related_Docs: []
---

# [System Name] Technical Audit Report

## Executive Summary
[Brief overview of findings, risk level, recommendations]

## 1.0 Audit Scope
[Components in/out of scope, methodology]

## 2.0 Findings
### 2.1 Critical Findings
[Table format with Risk IDs]

## 3.0 Evidence
[Reference to evidence directory structure]

## 4.0 Recommendations
[Prioritized action items]

## 5.0 Appendices
[A. Command Outputs, B. Screenshots, C. Interview Notes]
```

## 5.0 EVIDENCE MANAGEMENT PROTOCOL
### 5.1 Evidence Directory Structure
```text

/var/mnt/la_mansion/documentation/evidence/
├── AUDIT-2025-001/                    # Audit-specific evidence
│   ├── commands/                      # Command outputs
│   │   ├── 2025-12-22_16-45_df-h.txt
│   │   ├── 2025-12-22_16-46_ollama-status.txt
│   │   └── command_index.csv          # Index of all commands run
│   ├── screenshots/
│   │   ├── 2025-12-22_16-47_ollama-dashboard.png
│   │   └── screenshot_metadata.csv    # Description, timestamp
│   ├── logs/
│   │   ├── system.log                 # Referenced log excerpts
│   │   └── journalctl-ollama.txt
│   └── interviews/
│       ├── 2025-12-22_tech-lead-notes.txt
│       └── interview_summary.csv
├── INCIDENT-2025-001/                 # Incident evidence
└── VALIDATION-2025-001/               # Validation test evidence
```

#### 5.2 Command Output Capture Standard
```bash

# Capture with timestamp and context
{
  echo "=== COMMAND: df -h"
  echo "=== TIMESTAMP: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "=== CONTEXT: Storage audit baseline"
  echo ""
  df -h
} > /var/mnt/la_mansion/documentation/evidence/AUDIT-2025-001/commands/2025-12-22_16-45_df-h.txt
```

#### 5.3 Evidence Reference in Documents

In your markdown, reference evidence like this:
```markdown

## 3.1 Storage Verification
Storage utilization was confirmed at 3% (see evidence: `AUDIT-2025-001/commands/2025-12-22_16-45_df-h.txt`).

## 3.2 Service Status  
Ollama service confirmed running (screenshot: `AUDIT-2025-001/screenshots/2025-12-22_16-47_ollama-dashboard.png`).
```

#### 5.4 Evidence Index File

Create evidence_index.csv in each evidence directory:
```csv
file_name,timestamp,command_context,reference_in_doc,hash_sha256
2025-12-22_16-45_df-h.txt,2025-12-22 16:45:23,"Storage audit baseline","Section 3.1",a1b2c3...
2025-12-22_16-46_ollama-status.txt,2025-12-22 16:46:05,"Service status check","Section 3.2",d4e5f6...
```

## 6.0 QUALITY ASSURANCE CHECKLISTS
#### 6.1 Pre-Submission Checklist

    Metadata Complete: All header fields populated

    Version Number: X.Y.Z format, incremented appropriately

    References Valid: All evidence files exist and are accessible

    Acronyms Defined: Each acronym defined on first use (e.g., CADMIES: Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem)

    Code Examples Tested: All commands/scripts verified functional

    Diagrams Described: ASCII diagrams explained in captions

    Assumptions Documented: All assumptions explicitly stated

    Limitations Acknowledged: System constraints documented

    Units Included: All measurements have appropriate units

    Cross-References: Internal document links work correctly

    Spell Check: Technical terms correct, no typos

#### 6.2 Scientific Rigor Checklist

    Repeatable: Another team could reproduce findings

    Verifiable: All claims supported by evidence

    Objective: Language is neutral and factual

    Structured: Logical flow from problem to solution

    Complete: No unanswered questions or gaps

#### 6.3 PDF Generation Checklist

    Table of Contents: Generated and accurate

    Page Numbers: Consistent throughout

    Code Formatting: Syntax highlighting preserved

    Font Consistency: No font substitution warnings

    Image Placement: Diagrams correctly positioned

    Hyperlinks: Clickable references work

## 7.0 TROUBLESHOOTING (BATTLE-TESTED)
#### 7.1 Common Issues & Solutions

Issue: "pandoc: command not found"

Solution: You're not in the toolbox
```bash

toolbox enter documentation-tools
```
Issue: "Error producing PDF" with # character

Solution: Replace # in diagrams with //
```bash

sed -i 's/^\(.*\)# \(.*\)$/\1\/\/ \2/' "your_document.md"
```
Issue: Unicode characters causing failures

Solution: Clean problematic characters
```bash

# Box characters
sed -i 's/[����]//g' "your_document.md"

# Emojis  
sed -i 's/[����]//g' "your_document.md"

# Smart quotes (curly to straight)
sed -i "s/[」「]/\"'/g" "your_document.md"
```
Issue: File not found

Solution: Verify location and spelling
```bash

pwd  # Check current directory
ls -la *.md  # List markdown files
find /var/mnt/ -name "*.md" 2>/dev/null  # Search system

Issue: LaTeX missing packages

Solution: Install in toolbox
bash

toolbox enter documentation-tools
tlmgr install listings geometry fontspec
```
Issue: "toolbox: command not found" on Silverblue
Solution: Toolbox isn't installed on host. Install it first:
```bash

rpm-ostree install toolbox
sudo systemctl reboot
```
Issue: "Package not found" when trying to install in toolbox
Solution: Make sure you're INSIDE the toolbox when installing:
```bash

toolbox enter documentation-tools # Enter first
sudo dnf install [package] # Then install
```
Issue: "Permission denied" accessing /var/mnt from toolbox
Solution: The toolbox user may not have access. Check permissions:

On host (outside toolbox):
```bash

ls -la /var/mnt/
```
If needed, adjust permissions:
```bash

sudo chmod -R 755 /var/mnt/la_mansion
```
Issue: "Toolbox 'documentation-tools' already exists" when creating
Solution: You already have it! Just enter it:
```bash

toolbox enter documentation-tools
```
Issue: Changes in toolbox don't persist after exit/enter
Solution: All package installations DO persist. User files in /home and /var/mnt persist. Only temporary runtime state is lost.

#### 7.2 Evidence Management Issues

Issue: Command output too large

Solution: Capture essential parts only
```bash

{
  echo "=== ESSENTIAL OUTPUT ONLY ==="
  df -h | grep -E "(Filesystem|/var/mnt/)"
  echo "... [truncated for brevity]"
} > evidence_file.txt
```
Issue: Screenshot organization

Solution: Use consistent naming
```text
YYYY-MM-DD_HH-MM_context_description.png
Example: 2025-12-22_16-47_ollama-dashboard-models-empty.png
```

## 8.0 BEST PRACTICES AND STANDARDS
#### 8.1 File Management

    Source Files are Sacred: Keep .md files forever as single source of truth

    PDFs are Ephemeral: Regenerate as needed from source

    Dated Filenames: Always use YYYY-MM-DD_topic_version.md format

    Project Organization: Group documents by system/component

    Regular Backups: Include documentation in 3-tier backup system

#### 8.2 Content Standards

    Scientific Purity: Facts over decoration, evidence over opinion

    ASCII Diagrams Only: Use +, -, |, > for all diagrams

    Descriptive Text: No emojis, use words for emphasis

    Standard Fonts: Liberation Sans for body, Liberation Mono for code

    Code Formatting: Always use --listings option with pandoc

#### 8.3 Version Control Standards

Version numbering:
```text

MAJOR (X): Breaking changes, new structure

MINOR (Y): New sections, significant additions

PATCH (Z): Corrections, typo fixes, minor updates
```
Archive structure:
```text

archives/
├── v1.0.0/              # Complete version
├── v1.1.0/
└── latest -> v1.1.0/    # Symlink to current
```

#### 8.4 Diagram Standards
```text

// Network Diagram Example
        ┌─────────────────┐
        │  Core Service   │
        └─────────┬───────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼──┐     ┌───▼──┐     ┌───▼──┐
│Node A│─────│Node B│─────│Node C│
└──────┘     └──────┘     └──────┘

// Flow Chart Example
Start → [Process Step] → Decision → Yes → [Action]
                              ↓
                              No → [Alternative] → End
```

## 9.0 QUICK REFERENCE CARD
#### 9.1 Essential Commands

Enter documentation environment
```bash

toolbox enter documentation-tools
```
Generate PDF (standard)
```bash

pandoc "doc.md" -o "doc.pdf" --toc --number-sections --pdf-engine=xelatex --listings
```
Generate PDF (full scientific)
```bash

pandoc "doc.md" -o "doc.pdf" --toc --number-sections --pdf-engine=xelatex --listings -V geometry:margin=2.5cm -V mainfont="Liberation Sans" -V monofont="Liberation Mono" -V linestretch=1.5
```
Check document structure
```bash

head -20 doc.md | grep -E "^#|^---"
```
Clean problematic characters
```bash

sed -i 's/[����]//g' doc.md
```

#### 9.2 File Naming Examples
```text

2025-12-22_cadmies_audit_v1.0.md
2025-12-22_ollama_config_spec_v2.1.md
2025-12-22_backup_recovery_runbook.md
```

#### 9.3 Quality Checklist (Abbreviated)

    Metadata complete

    Evidence referenced

    Code tested

    No Unicode issues

    PDF generates cleanly

#### 9.4 Template Locations
```text

/var/mnt/la_mansion/documentation/templates/
├── template_audit_report.md
├── template_architecture_spec.md
├── template_runbook.md
├── template_postmortem.md
├── template_research_note.md
└── template_system_manual.md
```

## APPENDIX A: TEMPLATE LIBRARY
### A.1 Audit Report Template

(Full template as shown in Section 4.2)
### A.2 Runbook Template
```markdown

# TEMPLATE: Operational Runbook

---
System: [System Name]
Document_ID: [CA-YYYY-NNN-RUNBOOK]
Version: [1.0.0]
Classification: INTERNAL
Author: [Operations Lead]
Reviewers: [Technical Lead, Backup Operator]
Status: ACTIVE
Created: [YYYY-MM-DD]
Modified: [YYYY-MM-DD]
Related_Docs: [ARCH-DOC-ID, AUDIT-DOC-ID]
---

# [System/Procedure] Runbook

## Purpose
[What this runbook accomplishes]

## Prerequisites
[Required access, tools, knowledge]

## Procedure
### Step 1: [Action]

command --with options

### Step 2: [Verification]

check --command here

## Troubleshooting
| Symptom | Cause | Resolution |
|---------|-------|------------|
| [Issue] | [Root cause] | [Fix steps] |

## Rollback Procedure
[How to undo changes if procedure fails]

## Success Verification
[How to confirm procedure succeeded]

### A.3 Research Note Template
markdown

# TEMPLATE: Research Note

---
System: [System/Experiment Name]
Document_ID: [CA-YYYY-NNN-RESEARCH]
Version: [1.0.0]
Classification: INTERNAL
Author: [Researcher Name]
Reviewers: [Peer Reviewer]
Status: PRELIMINARY
Created: [YYYY-MM-DD]
Modified: [YYYY-MM-DD]
Related_Docs: []
---

# Research Note: [Topic]

## Hypothesis
[What you expect to find]

## Experiment Design
[Methodology, controls, variables]

## Data Collected
[Tables, measurements, observations]

## Analysis
[Interpretation of results]

## Conclusions
[What was learned, next steps]

## Raw Data References
[Location of raw data files]

## APPENDIX B: METADATA STANDARDS

### B.1 Classification Levels

    INTERNAL: Team use only, contains operational details

    CONFIDENTIAL: Restricted distribution, sensitive information

    PUBLIC: Safe for external sharing, no sensitive data

### B.2 Status Definitions

    DRAFT: Under active development, not for operational use

    REVIEW: Ready for peer review, content complete

    FINAL: Reviewed and approved, ready for use

    ACTIVE: Currently in use for operations (equivalent to FINAL)

    DEPRECATED: Replaced by newer version, historical only

    ARCHIVED: Retained for reference, not current

### B.3 Document ID Format
```text

CA-YYYY-NNN-TYPE
│   │    │   └── Document type (AUDIT, SPEC, RUNBOOK, etc.)
│   │    └────── Sequential number (001, 002, 003...)
│   └─────────── Year (2025, 2026...)
└─────────────── Cosmium Angelo prefix
```

### B.4 Version Numbering Rules

    Major (X): Breaking changes, new document structure

    Minor (Y): Significant additions, new sections

    Patch (Z): Corrections, typo fixes, minor updates

Example evolution: 1.0.0 → 1.0.1 → 1.1.0 → 2.0.0

## APPENDIX C: VERSION HISTORY AND CONSOLIDATION NOTES
### C.1 Current Version (v1.0.0 - 2026-01-21)

    Consolidated three variant documents into single NASA-standard version

    Standardized all date formats to YYYY-MM-DD throughout

    Preserved all original content from source documents

    Resolved formatting inconsistencies between variants

    Added comprehensive metadata tracking consolidation history

### C.2 Source Documents Consolidated

    2025-12-22_guide-cadmies_scientific_documentation_creation_v1.1.0.md

        Version: 1.1.0

        Date format: YYYY-MM-DD

        Most recent variant before consolidation

    2025-12-22_guide-cadmies_scientific_documentation_creation_v1.0.0.md

        Version: 1.0.0

        Date format: YYYY-MM-DD

        Earlier variant with YYYY-MM-DD format

    CADMIES - Scientific Documentation Creation Guide v1.0.0 Dec 2025

        Version: 1.0.0

        Date format: MM-DD-YYYY and MM-DD-YY variants

        Earlier variant with different date formatting

### C.3 Key Changes from Consolidation

    Metadata standardization: All headers now use YYYY-MM-DD format

    Date consistency: Examples in content remain as 2025-12-22 (historical)

    File naming: NASA-compliant: hieros_guide_scientific_documentation_creation_20260121_v1.0.0_released.md

    Document ID: Updated to reflect creation date: CA-2026-021-GUIDE

    Version reset: New consolidated document starts at v1.0.0

    NASA compliance: Added document type "guide" to classification

### C.4 Historical Version Chain
```text

2025-12-22: v1.0.0 (MM-DD variant) created
2025-12-22: v1.0.0 (YYYY-MM-DD variant) created  
2025-12-22: v1.1.0 released with updates
2026-01-21: All variants consolidated into new v1.0.0 (NASA-standard with "guide" type)
```

End of Scientific Documentation Creation Guide v1.0.0
CADMIES Framework - Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem
NASA Document Type: GUIDE
*Consolidated on: 2026-01-21*