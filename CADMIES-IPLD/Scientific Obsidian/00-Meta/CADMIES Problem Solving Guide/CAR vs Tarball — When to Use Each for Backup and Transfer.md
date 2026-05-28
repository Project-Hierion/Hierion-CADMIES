CAR vs Tarball — When to Use Each for Backup and Transfer

Date encountered: 2026-05-27 through 2026-05-28 (post-Session-023 work)
Severity: Critical — misunderstanding this distinction contributed to index/blockstore mismatch
Status: Resolved (process documented)
See also: Problem: Map Generator Only Loads a Fraction of Indexed Concepts


Why This Document Exists
During post-Session-023 recovery work, we attempted to back up the index using a CAR file. We believed the CAR contained the index — it did not. CAR files export blocks from store/blocks/ only. The human_id_to_cid.json index is a separate file that lives outside the blockstore and is never included in a CAR export. When we needed to restore, we had blocks but no reliable index to map human-readable IDs to those blocks. This directly contributed to the index/blockstore mismatch that required a full rebuild.

The lesson: CAR files are for concept exchange between machines. Tarballs are for backing up the index, blocks, and source concept JSONs so we can restore the library if something breaks.

The Distinction
CAR files and tarballs serve different purposes. Using the wrong one for the wrong job leads to incomplete backups and difficult recoveries.

Use Case	Tool	What It Captures
Share concepts between machines	CAR	Blocks only (store/blocks/)
Full disaster recovery backup	Tarball	Blocks + index + index backups + source concepts
Pre-migration safety snapshot	Tarball	Everything needed for a complete restore
Portable concept archive	CAR	IPLD-native, can be imported by any IPLD tool
Why CAR Files Are Not Complete Backups
CAR (Content Addressable Archive) files export .cbor blocks from store/blocks/. The human_id_to_cid.json index lives at store/index/ — outside the blockstore — and is never included in a CAR. This is by design: CAR is an IPLD-native format for exchanging content-addressed data between systems. But it means a CAR file alone cannot restore the library.

When importing a CAR, the blocks land in store/blocks/ but the index must be rebuilt separately. If the index rebuild uses a stale or contaminated source, the mapping between human-readable IDs and CIDs drifts. Concepts appear to be missing even though their blocks exist on disk.

Creating a Full Tarball Backup
bash
cd /notebooks/CADMIES/CADMIES-IPLD
tar -czf /notebooks/cadmies_sessionXXX.tar.gz store/blocks/ store/index/human_id_to_cid.json store/index/backups/ source_concepts/
This captures the blocks, the live index, all index backup snapshots, and the source concept JSONs — everything required to restore the library to its exact state on any machine.

Restoring from a Tarball
bash
cd /notebooks/CADMIES/CADMIES-IPLD
tar -xzf /notebooks/cadmies_sessionXXX.tar.gz
Rules of Thumb
Tarball before risky operations. Consolidation, restructuring, mass deletes — tarball first.

CAR for exchange, tarball for safety. Use CAR to move concepts between machines. Use tarball to protect against data loss.

Never rely on a CAR alone for disaster recovery. If you only have a CAR, you will need to rebuild the index from the blocks on import — and that rebuild may not be clean.

Store tarballs in /notebooks/ on Paperspace — the file browser shows that directory and it persists across notebook restarts. Never store them in /root/.

