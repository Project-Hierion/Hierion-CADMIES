# Analysis Results

**Agent-generated insights from the CADMIES mycelium.**

## Overview

This directory contains JSON output files from the **Philosophical Analyzer Agent** and future agents. Each file represents a snapshot of agent analysis performed on a set of concepts.

## File Naming Convention
analysis_results_YYYYMMDD_HHMMSS.json
text


| Component | Example | Meaning |
|-----------|---------|---------|
| YYYYMMDD | 20260405 | Date of analysis (April 5, 2026) |
| HHMMSS | 022452 | Time of analysis (02:24:52 UTC) |

**Example:** `analysis_results_20260405_022452.json`

## File Contents

Each JSON file contains the complete output of an agent run:

```json
{
  "success": true,
  "concepts_analyzed": 22,
  "domain_distribution": {
    "Physics": 7,
    "Philosophy": 3,
    "Epistemology": 2
  },
  "type_distribution": {
    "ScientificLaw": 2,
    "PhilosophicalHypothesis": 2,
    "CognitiveAgent": 1
  },
  "common_terminology": {
    "system": 8,
    "physical": 6,
    "problem": 6
  },
  "connections": [
    {
      "source_title": "Concept A",
      "target_title": "Concept B",
      "connection_type": "shared_domain",
      "confidence": 0.8,
      "description": "Both belong to Epistemology"
    }
  ],
  "insights": [
    {
      "type": "domain_focus",
      "description": "Concepts span 9 different domains",
      "confidence": 0.7
    }
  ],
  "recommendations": [
    {
      "type": "further_exploration",
      "description": "Explore relationships between Concept A and Concept B",
      "priority": "high"
    }
  ],
  "metadata": {
    "analyzer_version": "1.0.0",
    "analysis_timestamp": "2026-04-05T02:24:52Z",
    "execution_time_seconds": 0.08,
    "focus_area": "general",
    "analysis_depth": "comprehensive"
  }
}

Viewing Results
Pretty-print a specific file
bash

cat analysis_results/analysis_results_20260405_022452.json | python -m json.tool

View the latest analysis
bash

cat $(ls -t analysis_results/*.json | head -1) | python -m json.tool

Extract specific fields
bash

# View only domain distribution
python -c "
import json
with open('analysis_results/analysis_results_20260405_022452.json') as f:
    data = json.load(f)
    print('Domain Distribution:')
    for domain, count in data.get('domain_distribution', {}).items():
        print(f'  {domain}: {count}')
"

Compare two analysis runs
bash

diff analysis_results/analysis_results_20260405_022223.json analysis_results/analysis_results_20260405_022452.json

Analysis Depth Levels
Depth	What's Included	File Size (typical)
basic	Domain, type, top terms	~1-2 KB
detailed	Basic + pairwise connections	~5-10 KB
comprehensive	Detailed + cluster analysis	~15-30 KB
Typical Results from Production
22-Concept Analysis (2026-04-05)
Metric	Value
Concepts analyzed	22
Connections found	118
Domains represented	9
Types represented	18
Execution time	0.08 seconds

Top domains: Physics (7), Mathematics (4), Philosophy (3)
Top terms: system, physical, problem, energy, effect
Key insight: Concepts span 9 different domains (interdisciplinary knowledge graph)
Regeneration

These files are regenerated on each agent run. They are not meant to be edited manually.

To regenerate the latest analysis:
bash

cd CADMIES-IPLD
python agents/code/philosophical_analyzer.py --cids $(python -c "import json; f=open('store/index/human_id_to_cid.json'); d=json.load(f); print(' '.join(d.values()))") --depth comprehensive

Archiving

Results are safe to delete if disk space is needed. They can always be regenerated from the current state of store/blocks/ and store/index/.

To archive old results:
bash

mkdir -p analysis_results/archive
mv analysis_results/analysis_results_2026* analysis_results/archive/

Git Tracking

Current policy: Analysis results are tracked in Git. This preserves the evolution of insights as the mycelium grows.

If results become too large, add to .gitignore:
bash

echo "analysis_results/*.json" >> .gitignore
git rm --cached analysis_results/*.json

Related Files
File	Purpose
agents/code/philosophical_analyzer.py	Agent that generates these results
store/index/human_id_to_cid.json	Source of concept CIDs
store/blocks/	Source of concept data

    "The mycelium doesn't just store knowledge — it analyzes it."

Let the mycelium grow! 🌱
