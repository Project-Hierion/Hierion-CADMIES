phase: 57
date: 2026-05-28
status: Complete
related: [[Session-023-The Terminator, Infrastructure Consolidation & Map UX Planning]], [[Session-025A — 2026-05-28 — Index Recovery, Codestral Breakthrough]], [[Phase-48-Relationship-Generator-Hardening]], , [[problem_solving_guide]]

Phase 57: Index Integrity & Disaster Recovery
What Changed
Recovered the CADMIES mycelium from a critical index/blockstore mismatch caused by the Session 023 Paperspace workspace consolidation. Established clear backup protocols distinguishing CAR files (concept exchange) from tarballs (disaster recovery). Cleaned 180 orphan blocks and 26 bad-format index entries. Created permanent documentation in the problem solving guide and GitHub Issue #274.

Why
During the Session 023 consolidation, three separate Paperspace projects were merged into a single CADMIES-Gradient structure. The git clone brought code but not blocks (gitignored). The index survived or was restored from backup, but pointed to CIDs whose .cbor files no longer existed on disk. The map and relationship generators loaded only 115 of 661 concepts.

A contributing factor: CAR files had been used as complete backups under the assumption they included the index. CAR exports only package blocks from store/blocks/. The human_id_to_cid.json index lives outside the blockstore and is never included. When restoring from CAR alone, blocks land on disk but the index must be rebuilt separately — and if rebuilt from a contaminated source, the mismatch persists.

Changes Made
1. Three-Step Index Cleanup
Step 1: Rebuild blockstore from source concepts. Source JSONs in source_concepts/ are the ground truth. A loop through cid_generator.py rebuilt all 652 concepts into fresh .cbor blocks with correct CIDs matching actual content.

Step 2: Purge orphan blocks. Compared every .cbor file against the clean index. Deleted 180 blocks whose CIDs had no matching index entry — HOG-era ghosts, duplicate formats, and stale mints.

Step 3: Remove bad-format index entries. Stripped 26 entries with colons (Epistemology:Concept/...), uppercase first letters (Alchemical Insight), and legacy HOG-era formats. Index went from 700 → 674 clean lowercase_snake_case entries.

2. Backup Protocol Established
Use Case	Tool	What It Captures
Share concepts between machines	CAR	Blocks only (store/blocks/)
Full disaster recovery	Tarball	Blocks + index + index backups + source concepts
Pre-migration safety snapshot	Tarball	Everything needed for complete restore
Creating a full tarball backup:

bash
cd /notebooks/CADMIES/CADMIES-IPLD
tar -czf /notebooks/cadmies_sessionXXX.tar.gz store/blocks/ store/index/human_id_to_cid.json store/index/backups/ source_concepts/
3. Documentation Created
Scientific Obsidian/00-Meta/CADMIES Problem Solving Guide/Problem: Map Generator Only Loads a Fraction of Indexed Concepts.md

Scientific Obsidian/00-Meta/CADMIES Problem Solving Guide/CAR vs Tarball — When to Use Each for Backup and Transfer.md

GitHub Issue #274: "Index/blockstore mismatch after workspace consolidation"

4. Backup Hygiene
Deleted over 100 auto-generated index backup files from store/index/backups/ — all snapshots of progressively broken states taken during failed recovery attempts. The 23:48 backup files were confirmed as post-migration artifacts, not healthy snapshots. Only the current clean tarball (index_backup_5_28_26.tar.gz) is considered a valid restore point.

Testing
Map generator loads 636 concepts (up from 115)

Index entries: 674 clean lowercase_snake_case, zero bad formats

Block count aligns with index entries

Tarball created and verified

GitHub issue filed and documented

Problem solving guide entries saved to Scientific Obsidian

Results
Metric	Before Recovery	After Recovery
Map nodes loaded	115	636
Index entries	700 (26 bad)	674 (0 bad)
Orphan blocks	180	0
Index backups	100+ (all broken)	0 (clean tarball only)
Analysis
The root cause was a process failure, not a code failure. CAR files were treated as complete backups when they only capture blocks. The consolidation was performed without a pre-migration tarball. When the blockstore was lost, the index survived but had no matching blocks, and every subsequent recovery attempt compounded the problem by creating backups of already-corrupted state.

The fix was returning to the only reliable ground truth: the source concept JSONs. Every other artifact (blocks, index, backups) can be regenerated from those files. The source concepts are the mycelium's DNA.

Conclusion
CAR files are for concept exchange between machines. Tarballs are for disaster recovery. This distinction is now permanently documented in the problem solving guide, the GitHub issue tracker, and the pipeline workflows. No future consolidation or migration should occur without a tarball backup first.

Next Steps
Apply same backup discipline to Buttercup and Narrative notebooks

Add pre-migration tarball step to pipeline workflow documentation

Consider adding index to CAR export format or creating a companion index file

Phase 58: Codestral relationship enrichment (the breakthrough that followed this recovery)

Group public gateway concept cards under 15 canonical domain headers (bookstore layout)