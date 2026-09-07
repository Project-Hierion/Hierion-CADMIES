---
phase: 73C
date: 2026-08-07
status: Complete
related: [[Phase-73A-Matadisco-Integration]], [[Session-044-2026-07-31-Matadisco-Integration-Foundation-and-Blueprint]], [[Session-044B-2026-08-05-Matadisco-Test-Publish-Success]], [[Phase-72A-LLMDataHub-Fork-Reorganization]]
---

# Phase 73C - Matadisco Reverse Domain Implementation and Bulk Readiness

## What Changed

We updated all Matadisco Lexicon IDs to follow AT Protocol's reverse domain naming convention, per feedback from vmx (Matadisco lead). This involved:

1. Changing Lexicon IDs from `project-hierion.llmdatahub` and `project-hierion.cadmies` to `org.project-hierion.llmdatahub` and `org.project-hierion.cadmies`
2. Updating the producer script, test records, and Lexicon JSON files
3. Deleting the old test records and re-publishing with the new IDs
4. Resolving the PDS HTTPS issues that were blocking authentication

## Why

vmx noted that reverse domain names are the standard in AT Protocol and improve uniqueness and discoverability. The change aligns our implementation with protocol conventions.

## Changes Made

### Lexicon ID Updates
```text
| File | Old Value | New Value |
|------|-----------|-----------|
| `scripts/matadisco_producer.py` | `project-hierion.llmdatahub` | `org.project-hierion.llmdatahub` |
| `scripts/matadisco_producer.py` | `project-hierion.cadmies` | `org.project-hierion.cadmies` |
| `docs/lexicon/llmdatahub.json` | `project-hierion.llmdatahub` | `org.project-hierion.llmdatahub` |
| `docs/lexicon/cadmies.json` | `project-hierion.cadmies` | `org.project-hierion.cadmies` |
| `docs/records/*.json` (dataset) | `"$type": "project-hierion.llmdatahub"` | `"$type": "org.project-hierion.llmdatahub"` |
| `docs/records/*.json` (concepts) | `"$type": "project-hierion.cadmies"` | `"$type": "org.project-hierion.cadmies"` |
```

### Infrastructure Changes

The PDS HTTPS issues were resolved by:
- Removing the Caddy container and installing Caddy on the host
- Consolidating all domains into a single host-level Caddyfile
- Fixing permissions on the Hierion site directory (`/home/Project/Hierion/CADMIES/docs`)
- Using `reverse_proxy localhost:3000` for the PDS (no container networking issues)

### Record Management

Old test records were deleted using `com.atproto.repo.deleteRecord` and replaced with new versions containing the updated Lexicon IDs.

## Testing

### Authentication Test
```
curl -X POST https://pds.project-hierion.org/xrpc/com.atproto.server.createSession \
  -H "Content-Type: application/json" \
  -d '{"identifier": "gardener.pds.project-hierion.org", "password": "..."}'
```

Result: 200 OK, access token received.

### Publish Test
```bash
python3 scripts/matadisco_producer.py --publish --file docs/records/test-dolphin-dataset.json
```

Result: ✅ Record published successfully.

## Results
```text
Record	Old AT-URI	New AT-URI
Dolphin	at://.../3msedzcgae22i	at://.../3mshwaxzdms2y
Anatta	at://.../3msee3nm6lk2i	at://.../3mshwbrqjgc2y
Interconnectedness	at://.../3msee3vo3jc2i	at://.../3mshwbsggls2y
```

All three records are live on Matadisco with the correct Lexicon IDs.

## Site Status
```text
Site	Status
PDS (pds.project-hierion.org)	✅ 200
Hierion (project-hierion.org)	✅ 200
```

## Analysis

## What Worked

- Reverse domain naming aligns with AT Protocol standards

- Host-level Caddy is simpler and more reliable than containerized Caddy

- Producer script handles authentication and publishing correctly

## What We Learned

- Caddy containers complicate networking. Moving Caddy to the host eliminated host.docker.internal issues and port conflicts.

- AT Protocol requires reverse domain names. Lexicon IDs should follow the org.project-hierion. pattern.

- File permissions matter. Caddy needs execute permissions on parent directories (/home/Project and /home/Project/Hierion) to serve files.

- Records are immutable. To update a record, you must delete it and re-publish.

## Challenges

- PDS HTTPS authentication failed due to Caddy container networking

- Caddy couldn't serve Hierion site files due to restrictive parent directory permissions

- Old records had to be deleted manually before re-publishing

## Conclusion

Phase 73C is complete. The Matadisco integration now uses reverse domain Lexicon IDs, the PDS is stable and accessible, and all test records are published. The infrastructure is ready for bulk publishing of CADMIES concepts and LLMDataHub datasets.

## Next Steps

- Complete the full license audit of LLMDataHub datasets

- Scale up to publish all 636 CADMIES concepts

- Automate publishing with GitHub Actions (optional)

## References

- Matadisco GitHub

- AT Protocol Lexicon Guide

- Project Hierion Matadisco Repo

*Let the mycelium grow!* 🌱
