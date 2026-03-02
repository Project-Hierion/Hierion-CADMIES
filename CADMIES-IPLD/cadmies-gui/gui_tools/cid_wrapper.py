import subprocess
import json
import tempfile
import os
import re
from pathlib import Path

class CIDGenerator:
    def __init__(self, system):
        self.system = system
        self.script_path = system.get_cid_generator()
    
    def generate(self, concept):
        """Generate CID from Concept object"""
        # Create temp JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(concept.to_json(), f, indent=2)
            temp_path = f.name
        
        try:
            # Run cid_generator
            result = subprocess.run([
                "python3",
                str(self.script_path),
                "--concept-file", temp_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"CID generator failed: {result.stderr}")
            
            # Parse CID from output
            output = result.stdout + result.stderr
            cid_match = re.search(r'bafy[a-zA-Z0-9]{50,}', output)
            
            if cid_match:
                return cid_match.group(0)
            else:
                raise Exception("No CID found in output")
            
        except Exception as e:
            raise Exception(f"CID generator error: {str(e)}")
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    async def generate_async(self, concept):
        """Async version for UI"""
        import asyncio
        return await asyncio.to_thread(self.generate, concept)
