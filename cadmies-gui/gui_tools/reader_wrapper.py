import subprocess
import json
import re

class ConceptReader:
    def __init__(self, system):
        self.system = system
        self.script_path = system.get_cbor_reader()
    
    def read_concept(self, human_id_or_cid):
        """Read concept by human_id or CID"""
        try:
            result = subprocess.run([
                "python3",
                str(self.script_path),
                human_id_or_cid
            ], capture_output=True, text=True, check=True)
            
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            return f"Error reading concept: {e.stderr}"
    
    async def read_concept_async(self, human_id_or_cid):
        """Async version for UI"""
        import asyncio
        return await asyncio.to_thread(self.read_concept, human_id_or_cid)
    
    def list_all(self):
        """Get all concepts from index"""
        index_path = self.system.get_index_path()
        if not index_path.exists():
            return {}
        
        with open(index_path) as f:
            return json.load(f)
    
    def get_valid_concepts(self):
        """Return only valid concepts (not legacy/test)"""
        all_concepts = self.list_all()
        # Filter out legacy/test concepts
        return {
            k: v for k, v in all_concepts.items()
            if not k.startswith(("old_", "legacy_", "test_")) or k == "test_simple"
        }
    
    def search_concepts(self, query):
        """Search concepts by name"""
        all_concepts = self.get_valid_concepts()
        if not query:
            return all_concepts
        
        query = query.lower()
        return {
            k: v for k, v in all_concepts.items()
            if query in k.lower()
        }
