---
sop: Concept-Harvesting-SOP
section: Procedures
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-02-Run-Harvester]], [[07-02-Validation-Errors]]"
---

# 04-03 — Review and Mint

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
procedure documented here reflects the pipeline as of the August 2026
script audit.

## When to Use

- After the harvester extracts concepts
- When running in review mode without `--auto`
- When manually importing concepts

## Procedure

### Step 1: Review the extracted concepts

The review menu presents each concept. Options:

| Action | Effect |
|---|---|
| View | Display the concept details |
| Approve | Accept the concept for minting |
| Skip | Reject the concept |
| Quit | Exit the review |

When running with `--auto`, this menu is skipped and all valid
concepts are approved.

### Step 2: Human enrichment

For each concept, add the human layer:

- Deeper definitions
- Better insights
- The poetic version
- The mantra

Mistral provides the skeleton. The human adds the flesh. This is the
co-gardener step.

### Step 3: Validation

The scientific validator checks schema compliance before minting.
Validation levels:

| Level | Description |
|---|---|
| BASIC | Minimal schema checks |
| STANDARD | Standard concept requirements |
| RIGOROUS | Strict scientific requirements |
| STRICT | Full compliance |

If validation fails, see [[07-02-Validation-Errors]].

### Step 4: Minting

The CID generator:

1. Generates the content-addressed identifier
2. Saves the block to the blockstore
3. Updates the index
4. Logs the operation
5. Creates the provenance record

Each minted concept receives a permanent CID and becomes part of the
living mycelium.

## Manual Import Mode

When no LLM is available, concepts can be imported directly:

The pipeline loads unminted concept JSONs from `source_concepts/` for
review. The review and minting steps function identically.

## Verification

- [ ] Every concept reviewed or auto-approved
- [ ] Human enrichment completed for approved concepts
- [ ] Validation passed
- [ ] CIDs generated
- [ ] Blocks in blockstore
- [ ] Index updated
- [ ] Provenance records created

## Related

- [[04-02-Run-Harvester]] — the extraction step
- [[07-02-Validation-Errors]] — validation troubleshooting
- [[05-04-Script-Inventory]] — cid_generator and validator details
