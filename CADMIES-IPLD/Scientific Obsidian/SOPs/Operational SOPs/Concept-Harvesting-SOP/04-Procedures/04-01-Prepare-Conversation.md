---
sop: Concept-Harvesting-SOP
section: Procedures
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-02-Run-Harvester]], [[05-02-Workflow-Commands]]"
---

# 04-01 — Prepare Conversation

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
procedure documented here reflects the pipeline as of the August 2026
script audit.

## When to Use

Before running the harvester. The conversation file is the input that
everything downstream flows from.

## Procedure

### Step 1: Edit the conversation file

Edit `tools/harvest/conversation.json`. This is the template:

```json
{
  "metadata": {
    "_citation_guidance": "For scientific provenance and proper attribution, complete the fields below. They are optional but we highly advise they be filled in — omitted fields default to internal CADMIES system standards. All entries may be amended later as new source information becomes available.",
    "source_description": "YOUR TEXT HERE",
    "source_url": "YOUR TEXT HERE",
    "author": "YOUR TEXT HERE",
    "license": "YOUR TEXT HERE"
  },
  "content": "YOUR TEXT HERE"
}
```

### Step 2: Fill in the content field

Paste the full conversation or source text into the content field.

The loader handles unescaped newlines, apostrophes, and malformed
conversation files. Do not worry about line breaks or formatting.

### Step 3: Fill in the metadata fields

For external sources — published work, blogs, papers, articles —
complete the metadata fields for proper attribution:

| Field | Purpose |
|---|---|
| source_description | What the source is |
| source_url | Where it came from |
| author | Who wrote it |
| license | Licensing information |

The metadata is optional but advised. Omitted fields default to
internal CADMIES system standards.

### Step 4: Verify the file

Confirm the JSON is valid:

```bash
python3 -c "import json; json.load(open('tools/harvest/conversation.json'))"
```
No output means the JSON is valid.

External Source Example
From the Rebentisch Harvest:

```json
{
  "metadata": {
    "_citation_guidance": "For scientific provenance and proper attribution, complete the fields below. Optional — defaults to internal CADMIES standards. May be amended later.",
    "source_description": "Dr. Rupert Rebentisch's blog 'Mycelium of Knowledge' — article: 'When AI Becomes Your Zettelkasten's Co-Pilot'",
    "source_url": "https://www.mycelium-of-knowledge.org/when-ai-becomes-your-zettelkastens-co-pilot/",
    "author": "Dr. Rupert Rebentisch",
    "license": "MIT"
  },
  "content": "[Full article text here]"
}
```

## How Metadata Is Used

The harvester injects the metadata into the proofs array of each
concept:

```json
"proofs": [{
  "type": "conversation_extraction",
  "description": "Extracted from conversation via mistral:7b",
  "reference": "https://...",
  "author": "...",
  "license": "..."
}]
```

This ensures every concept minted from an external source carries its
provenance.

## Verification

- [ ] conversation.json edited with content
- [ ] Metadata fields filled for external sources
- [ ] JSON validates without errors

## Related
- [[04-02-Run-Harvester]] — next step
- [[05-02-Workflow-Commands]] — full workflow reference
