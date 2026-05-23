## Phase 43/50C: Remint & CAR Resolution

Reminted 153 HOG-era blocks with proper CIDv1. Discovered persistent verification
mismatch between remint script's compute_current_cid() and car_utils calculate_cid() —
both use hashlib.sha256 + multihash.wrap but produce different CIDs. Code alignment
bug, not data corruption. Deferred to future session.

CAR pipeline proven: export, download, import, map generation all work for users.
Index conflicts are expected when updating — resolved via Option A (clean replace)
for public users, Option B (provenance preserved) for dev pipeline.

## Architecture Decisions

- Two branches: main (dev) + public (user)
- Hybrid CAR strategy: Option A for users (clean), Option B for dev (provenance)
- User publishing: delta CARs for sending updates back (future tool)
- incoming_cars/ replaces temp_tarz/ as the official CAR import directory
- All four nodes synced, all stray branches deleted