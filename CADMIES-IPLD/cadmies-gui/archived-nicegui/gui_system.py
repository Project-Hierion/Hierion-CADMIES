import os
from pathlib import Path
from dotenv import load_dotenv
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "core"))
from paths import STORE_DIR, BLOCKS_DIR, INDEX_FILE, LOGS_DIR


class CadmiesSystem:
    def __init__(self, base_path=None):
        load_dotenv()
        # Allow custom base path or use current directory
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent
            
        # Expected structure - configurable via env or relative to base
        tools_path_env = os.getenv('CADMIES_TOOLS_PATH')
        if tools_path_env:
            self.tools_path = Path(tools_path_env)
        else:
            # Default: look for tools/core/ relative to base_path
            self.tools_path = self.base_path / "tools" / "core"
    
    def get_blocks_path(self):
        return BLOCKS_DIR

    def get_index_path(self):
        return INDEX_FILE

    def get_logs_path(self):
        return LOGS_DIR / "operations.jsonl"

    def get_cid_generator(self):
        return self.tools_path / "cid_generator_v1_1_0.py"

    def get_cbor_reader(self):
        return self.tools_path / "cbor_reader.py"
    
    def verify_system(self):
        """Check if all required components exist"""
        checks = {
            "blocks_dir": self.get_blocks_path().exists(),
            "index_file": self.get_index_path().exists(),
            "cid_generator": self.get_cid_generator().exists(),
            "cbor_reader": self.get_cbor_reader().exists(),
        }
        return all(checks.values()), checks
    
    @property
    def store_path(self):
        return STORE_DIR

    def get_system_info(self):
        """Return human-readable system info"""
        valid, checks = self.verify_system()
        blocks = list(self.get_blocks_path().glob("*.cbor")) if self.get_blocks_path().exists() else []
        return {
            "status": "✅ Operational" if valid else "❌ Incomplete",
            "path": str(self.base_path),
            "tools_path": str(self.tools_path),
            "store_path": str(self.store_path),
            "concepts_count": len(blocks),
            "checks": checks
        }
