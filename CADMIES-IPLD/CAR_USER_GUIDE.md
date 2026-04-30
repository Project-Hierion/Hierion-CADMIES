# CADMIES CAR System User Guide

## What is a CAR file?

CAR (Content Addressable Archive) is a standardized format for bundling content-addressed data. In CADMIES, a CAR file packages one or more concept blocks with their provenance records into a single shareable file. Same content = same CID, always — even inside a CAR.

## Why CAR?

- **Offline sharing** — Send concepts to collaborators without network access
- **Air-gap compatible** — Move verified knowledge across isolated systems
- **Backup** — Export your full mycelium as a single file
- **Verification exchange** — Scientists export verified concepts, recipients import and validate

## Exporting Concepts

### Export a single concept

```
python tools/export_to_car.py natural_selection --output natural_selection.car
```

This bundles the concept block and all its provenance records into one CAR file.

### Export all concepts (full backup)

```
python tools/export_to_car.py --all --output full_mycelium_backup.car
```

This exports every block in `store/blocks/` along with their provenance. Use this to create a complete snapshot of your mycelium.

### Export with CID

```
python tools/export_to_car.py --cid bafyreib... --output concept.car
```

Use the full CID when you don't have a human-readable ID mapped.

## Importing Concepts

### Import from local CAR file

```
python tools/import_from_car.py natural_selection.car
```

This reads the CAR, validates the CIDs (content hasn't been tampered with), and writes the blocks into your `store/blocks/` directory. The human_id index updates automatically.

### Import and verify without writing

```
python tools/import_from_car.py natural_selection.car --verify-only
```

Preview what's in the CAR — checks CIDs match their content, shows concept metadata, but doesn't import. Useful when receiving CAR files from unknown sources.

### Import from GitHub release

```
python tools/import_from_github.py --url https://github.com/Hieros-CADMIES/CADMIES/releases/download/v0.2.0-reader-capability/full_mycelium_v0.2.0.car
```

Downloads the CAR from a URL (GitHub release, IPFS gateway, or any HTTPS endpoint) and imports it. The `--url` flag accepts any direct download link.

## Verification Workflow with CAR

This is the scientist verification handshake:

### Step 1: Scientist exports a verified concept

```
python tools/core/verification_manager.py --export-verification \
  --concept-cid bafyreib... \
  --verifier-key "scientist@example.com" \
  --source orcid \
  --output verified_concept.car
```

This creates a CAR containing the original concept plus the scientist's verification provenance block.

### Step 2: Scientist sends the CAR file

Email, shared drive, IPFS — any transport works. The CAR is self-verifying.

### Step 3: Recipient previews before importing

```
python tools/import_from_car.py verified_concept.car --verify-only
```

Shows who verified it, what level, and confirms the CIDs are intact.

### Step 4: Recipient imports

```
python tools/import_from_car.py verified_concept.car
```

The verification block joins your mycelium. The concept's validation status updates accordingly.

## Verification Badges

| Badge | Level | Meaning |
|-------|-------|---------|
| 🔴 | 0 | Unverified |
| 🟡 | 1 | Self-verified |
| 🟢 | 2 | Verified (ORCID or institution) |
| 💎 | 3 | Highly verified (2+ ORCID or ORCID+institution) |

## Understanding CAR Files

### What's inside?

A CADMIES CAR file contains:
1. **Header** — CAR version and root CIDs
2. **Concept blocks** — The actual CBOR-encoded concepts
3. **Provenance blocks** — Creation records, verification statements, supersedence chains
4. **Index metadata** — Internal mapping for human-readable lookups

### How CIDs work in CAR files

Every block's CID is calculated from its content using SHA2-256 with dag-cbor encoding. If a single byte changes, the CID changes completely. This means:
- You can't forge a concept — the CID won't match
- You can't tamper with provenance — verification breaks
- You can always verify a CAR hasn't been corrupted in transit

### Multiple concepts in one CAR

A CAR can hold any number of concepts. The full mycelium release CAR contains 50+ interconnected concepts. When importing large CARs:
- Expect 30-60 seconds for full validation (CID recalculation on every block)
- Blocks are written atomically — failed import doesn't leave partial state
- Duplicate blocks (same CID already in your store) are skipped

## Troubleshooting

### "CID mismatch" error

The CAR file has been corrupted or tampered with. The calculated CID doesn't match the one in the CAR header. **Do not import.** Request a fresh export from the source.

### "No provenance found" warning

The concept imports fine, but it has no provenance records. This means either:
- It was exported without provenance (unusual)
- The concept is brand new (normal for seed concepts)

### "Block already exists"

Safe to ignore. Your mycelium already has this block. The importer skips duplicates automatically.

### "Unsupported multihash"

You're missing `pycryptodome` or `pysha3`. Install with:

```
pip install pycryptodome pysha3
```

## Advanced: Creating Release CARs

For maintainers publishing official mycelium releases:

```
python tools/export_to_car.py --all --output full_mycelium_vX.Y.Z.car
```

Then upload to GitHub Releases alongside the source code assets. Tag format: `vX.Y.Z-brief-description` (e.g., `v0.3.0-reader-fixes`).

Users import the release CAR with:

```
python tools/import_from_github.py --url https://github.com/Hieros-CADMIES/CADMIES/releases/download/v0.3.0-reader-fixes/full_mycelium_v0.3.0.car
```

The mycelium grows independently of code — concept releases and code releases can (and should) diverge over time.
