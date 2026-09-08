---
sop: Concept-Harvesting-SOP
section: References
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-02-Run-Harvester]]"
---

# 05-01 — CLI Flags

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The flags
documented here reflect the pipeline as of the August 2026 script
audit.

## Harvester Flags

| Flag | Effect |
|---|---|
| `--auto` | Skip review menu, approve all valid concepts |
| `--batch` | Process all JSON files in harvest/conversations/ |
| `--with-relationships` | Auto-run relationship generator after minting |
| `--model=codestral` | Use Codestral 22B instead of Mistral 7B |
| `--model=tinyllama:1.1b` | Use TinyLlama (CPU-capable) |
| `--conv=path/to/file.json` | Specify a different conversation file |

## Usage Examples

### Full Auto Harvest

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
```

## Review Mode

```bash
python tools/harvest/harvest_full_pipeline.py --with-relationships
```

## Codestral Enrichment

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships --model=codestral
```

## Batch Processing

```bash
python tools/harvest/harvest_full_pipeline.py --batch
```

## Custom Conversation File

```bash
python tools/harvest/harvest_full_pipeline.py --conv=path/to/file.json
```

## Default Behavior

Without flags, the harvester:

- Uses Mistral 7B
- Reads tools/harvest/conversation.json
- Pauses at the review menu
- Does not run relationship generation

## Related
- [[04-02-Run-Harvester]] — how to use the flags
- [[05-02-Workflow-Commands]] — full workflow reference
