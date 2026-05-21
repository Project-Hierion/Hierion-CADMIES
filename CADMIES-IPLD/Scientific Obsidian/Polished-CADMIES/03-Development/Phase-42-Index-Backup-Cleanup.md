---
phase: 42
date: 2026-05-21
status: ✅ Complete
related: [[Phase-46-Unmapped-Domain-Mapping]], [[Session-015]]
---

# Phase 42: Index Backup Cleanup

## What Changed

The index backup mechanism in `tools/core/cid_generator.py` was updated to write backups to a `store/index/backups/` subdirectory instead of the active `store/index/` directory. The `.gitignore` file was updated to exclude the backups directory from version control. Six pre-existing backup files from Phase 46's remint cascade were moved to the new subdirectory.

## Why

Harvest, enrichment, and relationship generation scripts all call `cid_generator.py` to update `store/index/human_id_to_cid.json`. Before writing, the generator creates a timestamped backup of the existing index. Prior to Phase 42, these backups were written directly to `store/index/` with filenames like `human_id_to_cid.json.backup.20260521_170502`. Over multiple sessions, the index directory accumulated backup files alongside the active index, creating clutter and making it difficult to identify the live file.

Phase 42 was necessary because:
1. Backup files in the active directory obscure the real index file
2. The `.gitignore` could not distinguish backups from the active index
3. A dedicated subdirectory enables future auto-cleanup logic

## Changes Made

### 1. Backup Path Update (`tools/core/cid_generator.py`)

Lines 203-207 were changed from:

```python
# Backup existing index
if os.path.exists(index_path):
    backup_path = f"{index_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    import shutil
    shutil.copy2(index_path, backup_path)
```

To:

```python
# Backup existing index to backups subdirectory
if os.path.exists(index_path):
    backup_dir = os.path.join(os.path.dirname(index_path), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    backup_filename = os.path.basename(index_path) + ".backup." + datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, backup_filename)
    import shutil
    shutil.copy2(index_path, backup_path)
```

Key changes:
- `backup_dir` constructed using `os.path.join` and `os.path.dirname(index_path)` → `store/index/backups/`
- `os.makedirs(backup_dir, exist_ok=True)` ensures the subdirectory exists
- `backup_filename` uses `os.path.basename(index_path)` for clean filename construction
- `backup_path` uses `os.path.join(backup_dir, backup_filename)` for cross-platform compatibility

### 2. `.gitignore` Update

Added `store/index/backups/` to `.gitignore`. The active index (`store/index/human_id_to_cid.json`) remains tracked. Backup files are now excluded from version control entirely.

### 3. Existing Backup Migration

Six backup files from Phase 46's remint cascade were moved from `store/index/` to `store/index/backups/`:

```
human_id_to_cid.json.backup.20260521_170502
human_id_to_cid.json.backup.20260521_170503
human_id_to_cid.json.backup.20260521_170504
human_id_to_cid.json.backup.20260521_170505
human_id_to_cid.json.backup.20260521_170506
human_id_to_cid.json.backup.20260521_170507
```

## Testing

### Pre-Phase State

```
ls store/index/ | grep backup
# 6 backup files interleaved with active index
```

### Post-Phase State

```
ls store/index/
# human_id_to_cid.json (only the active file)

ls store/index/backups/
# 6 backup files in dedicated subdirectory
```

### Map Generator Verification

The map generator (`generate_mycelium_map.py`) was run after the change. It does not modify the index and therefore does not trigger the backup logic, but its successful execution (342 nodes, 165 edges, 0 skipped) confirmed no regressions in the `cid_generator.py` module.

## Analysis

This is a minimal, targeted fix. The change affects one file (`cid_generator.py`) and touches exactly the path construction logic. All three scripts that modify the index (harvester, enrichment, relationship generator) share this code path, so the fix applies universally. No script-specific changes were needed.

The `os.makedirs(backup_dir, exist_ok=True)` line ensures the subdirectory is created automatically on first use, requiring no manual setup on new machines or fresh clones.

The `.gitignore` entry prevents backup files from ever being committed, regardless of where the backups subdirectory is located.

## Conclusion

Phase 42 is complete. The `store/index/` directory now contains only the active `human_id_to_cid.json` file. Backup files are stored in `store/index/backups/` and excluded from version control. The fix applies to all current and future scripts that use `cid_generator.py` for index updates.

## Next Steps

- Future phase: Add auto-cleanup on success (delete backups created during a run that completed without errors)
- Future phase: Keep backups on failure (preserve for recovery if a script errors out)