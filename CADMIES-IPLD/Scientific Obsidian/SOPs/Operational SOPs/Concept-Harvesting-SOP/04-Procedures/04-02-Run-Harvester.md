---
sop: Concept-Harvesting-SOP
section: Procedures
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-01-Prepare-Conversation]], [[05-01-CLI-Flags]]"
---

# 04-02 — Run Harvester

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
procedure documented here reflects the pipeline as of the August 2026
script audit.

## When to Use

After the conversation file is prepared. The harvester is the core
extraction engine.

## Procedure

### Step 1: Run the full pipeline

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
```

The --auto flag skips the review menu and approves all valid
concepts. The --with-relationships flag auto-runs the relationship
generator after minting.

### Step 2: Review mode (alternative)

To review each concept before minting:

```bash
python tools/harvest/harvest_full_pipeline.py --with-relationships
```

Without --auto, the pipeline pauses at the review menu.

### Step 3: Model selection

The harvester defaults to Mistral 7B. To use Codestral:

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships --model=codestral
```

To use TinyLlama (CPU-capable):

```bash
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships --model=tinyllama:1.1b
```

### Step 4: Batch mode

To process all JSON files in harvest/conversations/:

```bash
python tools/harvest/harvest_full_pipeline.py --batch
```

### Step 5: Custom conversation file

To specify a different conversation file:

```bash
python tools/harvest/harvest_full_pipeline.py --conv=path/to/file.json
```

## What the Pipeline Does

| Step | Action |
|---|---|
| Load | Reads the conversation JSON |
| Mycelium Context | Queries existing concepts via Willie's hybrid search |
| Chunk | Splits text into ~1000-word chunks |
| Extract | Sends chunks to Mistral with structured prompt |
| Transform | Maps output to UniversalScientificConcept schema |
| Save | Writes concepts to source_concepts/ |
| Merge | Deduplicates concepts across chunks |
| Review | Interactive menu (skipped with --auto) |
| Validate | Scientific validator checks schema |
| Mint | CID generation, blockstore save, provenance |

## Full CLI Flags

See [[05-01-CLI-Flags]] for the complete flag reference.

## Verification

- [ ] Harvester runs without errors
- [ ] Concepts written to source_concepts/
- [ ] Validation passes
- [ ] Blocks minted to blockstore
- [ ] Provenance records created

## Related

- [[04-03-Review-and-Mint]] — the review and minting detail
- [[05-01-CLI-Flags]] — all flags
- [[07-01-Harvester-Fails]] — troubleshooting
