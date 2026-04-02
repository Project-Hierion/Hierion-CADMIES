# paths.py - Centralized Path Management

## Purpose
Single source of truth for all file paths in CADMIES-IPLD.

## Why It Exists
- Scripts were using different paths (`./blocks`, `./store/blocks`, etc.)
- This caused "file not found" errors when running from different directories
- Now every script imports paths from here

## What It Provides
```text
| Variable | Path |
|----------|------|
| `PROJECT_ROOT` | `/.../CADMIES-IPLD/` |
| `STORE_DIR` | `PROJECT_ROOT/store/` |
| `BLOCKS_DIR` | `STORE_DIR/blocks/` |
| `INDEX_DIR` | `STORE_DIR/index/` |
| `LOGS_DIR` | `STORE_DIR/logs/` |
| `INDEX_FILE` | `INDEX_DIR/human_id_to_cid.json` |
```

## How to Use in Other Scripts

```python
from paths import BLOCKS_DIR, INDEX_FILE, LOGS_DIR, ensure_dirs
```

# Ensure directories exist
```python
ensure_dirs()
```
# Use paths
```python
block_path = BLOCKS_DIR / f"{cid}.cbor"
```

## Scripts Currently Using paths.py

    cbor_reader.py

    cid_generator_v1_1_0.py

    provenance_manager.py

## Maintenance

If the project structure changes, update ONLY this file. All scripts will automatically use the new paths.
