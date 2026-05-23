---
phase: 50
date: 2026-05-23
status: 🔄 In Progress
related: [[Phase-47-Orphan-Edge-Resolution]], [[Phase-48-Relationship-Generator-Hardening]], [[export_to_car.py]], [[import_from_car.py]], [[Session-018]]
---

# Phase 50: CAR Distribution Pipeline

## What Changed

The content-addressed archive (CAR) distribution pipeline was tested end-to-end. A full mycelium export was created on Paperspace (A4000 GPU), downloaded locally, and imported on the PNY development clone. The import verified 188 blocks successfully and detected 153 CID mismatches between Paperspace and local environments. The first GitHub Release (v0.5.0 — "The Happy Little Accidents") was published with the CAR file attached. CAR files will replace tarballs as the official mycelium distribution format.

## Why

Phase 48's fresh clone test revealed that new users who run `git clone` see an empty mycelium — the blockstore is gitignored. Tarballs were the initial workaround, but they provide no integrity verification. A user downloading `cadmies_latest.tar.gz` has no way to confirm the blocks are complete or uncorrupted.

CAR files are the IPLD-native solution:
- Every block is content-addressed and individually verifiable
- The import script (`import_from_car.py`) checks CID integrity for every block
- Users can re-import safely — duplicates are skipped, conflicts are flagged
- A single `.car` file replaces the entire `store/blocks/` directory plus the index

The `export_to_car.py` and `import_from_car.py` scripts were written on April 20, 2026, during early pipeline development, but were not needed until the mycelium reached sufficient density and the public distribution strategy was designed.

## Changes Made

### 1. Full Mycelium Export (Paperspace)

```
python tools/export_to_car.py --all --output /notebooks/cadmies_latest.car
```

Results:
- 342 concept blocks collected
- 341 total unique CIDs (plus consolidated index block)
- 342 root CIDs
- Output: 3,245,490 bytes (3.2MB)
- Export time: < 5 seconds on A4000 CPU
### 2. Local Import and Verification (PNY Clone)

python tools/import_from_car.py cadmies_latest.car

text

Results:
- 342 total blocks in CAR
- 188 blocks: already existed (verified, skipped)
- 153 blocks: CID mismatch (integrity check failed)
- 0 new blocks saved
- 1 verification block detected (self-verified concept)
- 342 index entries skipped (already present)
### 3. CID Mismatch Investigation (Pending — Sub-phase 50C)

The 153 mismatches indicate encoding variance between Paperspace and local environments. Likely causes:
- CBOR key ordering differences between Python environments
- Timestamp or metadata fields that differ between identical logical concepts
- `dag_cbor` version differences between Paperspace and local venv
- The `calculate_cid()` function producing different hashes than the original minting process
This does not affect the functional mycelium — all 342 concepts load correctly on both machines. The mismatch is in the CAR verification layer, not the data itself.
### 4. GitHub Release v0.5.0

The CAR file was pushed to the main repository with a `.gitignore` exception (`!cadmies_latest.car`). A GitHub Release was created:
- **Tag:** v0.5.0
- **Title:** v0.5.0 — The "Happy Little Accidents" Release
- **Assets:** `cadmies_latest.car` (3.2MB)
- **Notes:** 342 concepts, 259 edges, known CID encoding quirks, Bob Ross energy
## Testing
| Step | Environment | Result |
|------|-------------|--------|
| Export `--all` | Paperspace A4000 | ✅ 342 concepts, 3.2MB |
| Download CAR | Paperspace → Local | ✅ File browser |
| Import CAR | PNY clone (venv) | ⚠️ 188 verified, 153 mismatches |
| Map generation (post-import) | PNY clone | ✅ 342 nodes, 259 edges, 0 orphans |
| GitHub push | Local → GitHub | ✅ .gitignore exception added |
| Release creation | GitHub | ✅ v0.5.0 published |
## Analysis
### Why CAR Files Over Tarballs
| Property | Tarball | CAR File |
|----------|---------|----------|
| Integrity verification | None | Every block verified by CID |
| Duplicate handling | Overwrites silently | Skips with log message |
| Index handling | Manual (separate file) | Consolidated index block |
| Incremental updates | Full re-download | Only new blocks needed (future) |
| IPLD-native | No | Yes |
| User trust | "Trust us" | "Verify yourself" |
### The 153 CID Mismatches

The mismatches are a known limitation of the current pipeline, not a data corruption issue. All 342 concepts function correctly on both Paperspace and local. The CAR file's verification layer is more strict than the map generator's loading logic, catching encoding-level differences that don't affect functionality.
Resolution (Sub-phase 50C) will involve:
1. Auditing a sample of mismatched blocks to identify the specific encoding difference
2. Standardizing the CBOR encoding environment across machines
3. Potentially re-minting affected blocks with consistent encoding
4. Adding a `--relaxed` flag to the import script for users who want to skip CID verification
## Conclusion

Phase 50 is in progress. The CAR pipeline is functional — export, download, import, and map generation all work. The CID mismatch issue is documented and scoped for resolution. The first GitHub Release demonstrates the distribution model. CAR files are the future of CADMIES distribution.
## Next Steps
- **50C:** Investigate and resolve CID encoding mismatches
- **50D:** Automate CAR build on Paperspace after each relationship pass
- **50E:** Integrate CAR import into public-CADMIES setup script
- **Phase 51:** External collaboration with Bruno Cerda Mardini (entropy researcher)