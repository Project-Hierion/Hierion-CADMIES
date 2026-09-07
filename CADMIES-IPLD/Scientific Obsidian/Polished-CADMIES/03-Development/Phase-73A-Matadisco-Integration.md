---
phase: 73
date: 2026-07-30
status: Complete
related: [[Phase-72A-LLMDataHub-Fork-Reorganization]], [[growth_roadmap]]
---

# Phase 73A: Matadisco Integration

## What Changed

Phase 73 was planned as the next phase following the LLMDataHub fork reorganization. It extends the "mycelium reclaims nutrients from fallen logs" philosophy by publishing LLMDataHub dataset metadata and CADMIES concept metadata to Matadisco — the IPFS Foundation's decentralized data discovery network built on AT Protocol. This phase was planned during Session 042, following the completion of Phase 72.

## Why

LLMDataHub is an abandoned repository (5+ years unmaintained) containing curated LLM training dataset references. Phase 72 reorganized the fork for maintainability. Phase 73 completes the mission by making those datasets discoverable again through a decentralized network — turning a dead, siloed repo into findable, open knowledge.

Matadisco aligns with CADMIES architecture: content-addressed, decentralized, open, interoperable. Publishing to Matadisco serves double duty: training material discovery for Dr. Mistral and a real-world test of Matadisco as a data discovery network. CADMIES would be among the first non-geospatial publishers on the network.

Additionally, publishing CADMIES concept metadata to Matadisco extends the mycelium's reach — our 636 concepts become discoverable through an open protocol alongside satellite imagery, geodata, and cultural heritage collections.

## Changes Made

*This section will be populated as implementation progresses.*

### Planned Workstreams

**Workstream A: LLMDataHub → Matadisco**

| Step | Description | Status |
|------|-------------|--------|
| A1 | License audit — parse DATASETS.md, verify explicit licenses, build allowlist | Planned |
| A2 | Attribution mapping — per allowed dataset: author, source, license, link | Planned |
| A3 | Outreach — contact Matadisco/IPFS Foundation for green light | Planned |
| A4 | Record generation script — transform allowlist → Matadisco records | Planned |
| A5 | Publishing pipeline — GitHub Actions workflow to push records to ATProto | Planned |
| A6 | Validation — spot-check live records, verify attribution, confirm visibility | Planned |

**Workstream B: CADMIES Concepts → Matadisco**

| Step | Description | Status |
|------|-------------|--------|
| B1 | Concept metadata mapping — each concept → Matadisco record (resource = public gateway URL) | Planned |
| B2 | Record generation — extend producer script for concept JSON | Planned |
| B3 | Publishing — same GitHub Actions pipeline, separate record batch | Planned |
| B4 | Validation — confirm CADMIES concepts discoverable on the network | Planned |

### Constraints & Principles

- **License-first.** No license or ambiguous license = dataset is skipped. Only datasets with explicit, verifiable open licenses (MIT, Apache 2.0, CC-BY, CC0, etc.) are published.
- **Attribution always.** Every record credits original authors, links to source repositories, and cites license type. The mycelium shares knowledge, not identities. Credit where credit is due.
- **Privacy-respecting infrastructure.** Publishing via GitHub Actions (free tier). No personal data in records. No tracking. No data harvesting. If GitHub Actions is unsuitable, a free third-party alternative with strong privacy practices will be evaluated.
- **Validate everything.** Run `validate_vault.py` before committing. Keep the badge green.

### Infrastructure Plan

| Component | Plan |
|-----------|------|
| Publishing method | GitHub Actions (scheduled/manual), modeled after `gdi-de-csw-to-atproto` |
| PDS/relay target | Existing ATProto relay or free PDS — to be determined during implementation |
| Fallback | Fly.io free tier or equivalent privacy-respecting alternative |
| Record schema | `cx.vmx.matadisco` Lexicon: `resource` (URI), `publishedAt` (datetime), optional `preview` and `tags` |


### Deliverables

- `scripts/matadisco_producer.py` — generates Matadisco records from dataset index and concept JSON
- `.github/workflows/matadisco_publish.yml` — scheduled publishing pipeline
- `Phase-73-Matadisco-Integration.md` — this polished phase note (updated as work progresses)
- Raw session note for implementation session(s)
- Live Matadisco records, confirmed visible in matadisco-viewer

## Testing

*This section will be populated as implementation progresses.*

- License audit: all published datasets have verified open licenses
- Attribution: all records include author, source, and license
- Record validity: generated records conform to `cx.vmx.matadisco` schema
- Pipeline: GitHub Actions workflow runs successfully
- Visibility: published records appear in matadisco-viewer
- Vault health: `validate_vault.py` passes with green badge

## Results

*This section will be populated after implementation.*

## Analysis

*This section will be populated after implementation.*

## Conclusion

Phase 73 is planned and ready for execution. The license audit (Step A1) is the gate — no work on record generation or publishing begins until dataset licenses are verified. The Matadisco outreach (Step A3) runs in parallel. Once both clear, implementation proceeds through Workstream A (LLMDataHub datasets) then Workstream B (CADMIES concepts).

The mycelium extends its reach. Fallen logs become fertile ground.
