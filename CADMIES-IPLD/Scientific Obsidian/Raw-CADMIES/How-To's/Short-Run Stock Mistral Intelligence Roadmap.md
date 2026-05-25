**Short-Run Stock Mistral Intelligence Roadmap**

1. **Continue STEM Harvesting**
    
    - Process: Write conversation.json with new STEM topics → `python tools/harvest_full_pipeline.py --auto --with-relationships`
        
    - Target domains: Neuroscience, Chemistry, Economics, Medicine, Mathematics (per Codestral audit)
        
    - Files: `tools/conversation.json`, `tools/harvest_full_pipeline.py`
        
2. **Fix Unmapped Domains**
    
    - Process: Add unmapped domains to `DOMAIN_UPWARD_MAP` in `tools/generate_mycelium_map.py`
        
    - Current unmapped: Genetics → Biology, Quantum Physics → Physics, Thermodynamics → Physics, Geology → Earth Sciences/Physics, Biochemistry → Chemistry/Biology, Environmental Science → Ecology, Microbiology → Biology, Earth Sciences → Physics/Ecology
        
    - File: `tools/generate_mycelium_map.py`
        
3. **Phase 52: llama.cpp Integration**
    
    - Process: Scout Snagnar's llama.cpp fork → benchmark vs Ollama → implement persistent prompt caching
        
    - Goal: Faster inference, session-to-session memory for Mistral
        
    - Files: New tool in `tools/`, modify relationship generator to use llama.cpp backend
        
4. **Targeted Domain Relationship Passes**
    
    - Process: Modify `tools/generate_relationships.py` to accept `--domain` filter → run focused passes on STEM-sparse domains
        
    - Goal: Deeper connections within underrepresented domains instead of spraying the full graph
        
    - File: `tools/generate_relationships.py` (modification)
        
5. **Regular Codestral Audits**
    
    - Process: After major harvest runs → `ollama run codestral:22b` with structured audit prompt → document findings → adjust harvesting targets
        
    - Goal: Multi-model quality control, catch gaps Mistral misses
        
    - Output: Audit notes saved to Scientific Obsidian
        
6. **Fix Near-Duplicate Concepts**
    
    - Process: Identify case variants (`eternal_evolution` / `Eternal_Evolution`) → deduplicate → remint
        
    - Tool: `tools/remint_existing_concepts.py`
        
    - Part of: Phase 43 (Concept Editing & Reminting)
        
7. **Continue Incremental Relationship Passes**
    
    - Process: `python tools/generate_relationships.py --write` (can chain multiple)
        
    - Current: 452 edges from 374 nodes. Target: 500+ edges
        
    - File: `tools/generate_relationships.py`
        
8. **Sync & Commit Regularly**
    
    - Process: Tar Paperspace results → download to PNY → `git add -A && git commit && git push`
        
    - Keeps all four nodes aligned (PNY, SanDisk, Paperspace, GitHub)