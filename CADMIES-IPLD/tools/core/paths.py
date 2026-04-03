"""Centralized path management for all CADMIES tools."""

from pathlib import Path

# Get project root (CADMIES-IPLD/) - this file is in tools/core/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Standard paths
STORE_DIR = PROJECT_ROOT / "store"
BLOCKS_DIR = STORE_DIR / "blocks"
INDEX_DIR = STORE_DIR / "index"
LOGS_DIR = STORE_DIR / "logs"

# Index file path
INDEX_FILE = INDEX_DIR / "human_id_to_cid.json"

# Ensure directories exist
def ensure_dirs():
    """Create all required directories if they don't exist."""
    for dir_path in [BLOCKS_DIR, INDEX_DIR, LOGS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
