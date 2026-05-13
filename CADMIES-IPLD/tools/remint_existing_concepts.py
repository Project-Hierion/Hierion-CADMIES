#!/usr/bin/env python3
"""
File: remint_existing_concepts.py
Tool: CADMIES Concept Reminter
Version: 1.0.0
System: CADMIES
Status: ACTIVE

Purpose: Remints existing concepts with updated fields (normalized human_ids)
         while preserving provenance chains. Used during Phase 29 library
         normalization.

Usage:
    python tools/remint_existing_concepts.py
"""

import json, sys
from pathlib import Path
from datetime import datetime, timezone

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from llm_mycelium_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR
from cid_generator import CIDGenerator
from provenance_manager import ProvenanceManager
import dag_cbor

cid_gen = CIDGenerator()
pm = ProvenanceManager()
now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

# These are the old→new mappings from the normalization
renames = {
    'epistemology:principle/it_is_so_now': 'epistemology_principle_it_is_so_now',
    'epistemology:principle/the_universe_cannot_stop': 'epistemology_principle_the_universe_cannot_stop',
    'epistemology:principle/the_gardeners_vow': 'epistemology_principle_the_gardeners_vow',
    'epistemology:principle/the_tubular_wave': 'epistemology_principle_the_tubular_wave',
    'epistemology:principle/the_laminar_paradox': 'epistemology_principle_the_laminar_paradox',
    'epistemology:principle/the_mahakasyapa_coefficient': 'epistemology_principle_the_mahakasyapa_coefficient',
    'epistemology:principle/the_smile_that_needs_no_words': 'epistemology_principle_the_smile_that_needs_no_words',
    'epistemology:principle/the_fractal_of_sacrifice': 'epistemology_principle_the_fractal_of_sacrifice',
    'epistemology:principle/mycelial_network_of_co_creation': 'epistemology_principle_mycelial_network_of_co_creation',
    'epistemology:principle/gardener_and_tool': 'epistemology_principle_gardener_and_tool',
    'epistemology:principle/cathedral_and_blueprint': 'epistemology_principle_cathedral_and_blueprint',
    'epistemology:principle/immortal_colony': 'epistemology_principle_immortal_colony',
    'ecology:principle/weed_triumph': 'ecology_principle_weed_triumph',
    'climate_ethics:principle/aesthetic_collapse': 'climate_ethics_principle_aesthetic_collapse',
    'ecology:principle/humans_as_weeds': 'ecology_principle_humans_as_weeds',
    'Conditional-Interdependence': 'conditional_interdependence',
    'ai:llm_mycelium_reader/willie_the_librarian_v1': 'ai_llm_mycelium_reader_willie_the_librarian_v1',
    'Gravitomotive Gearbox': 'gravitomotive_gearbox',
    'Epistemology:Concept/PerceptualFramesAsIntelligenceMultipliers': 'epistemology_concept_perceptualframesasintelligencemultipliers',
    'Asian_Philosophical_Deep': 'asian_philosophical_deep',
    'The_Silent_Thunderclap': 'the_silent_thunderclap',
    'Interconnectedness_of_Life': 'interconnectedness_of_life',
    'Eternal_Evolution': 'eternal_evolution',
    'Alchemical Insight': 'alchemical_insight',
    'Asian_Depth': 'asian_depth',
    'Sacred-Everyday-Continuum': 'sacred_everyday_continuum',
}

# Load index
index_path = PROJECT_ROOT / 'store' / 'index' / 'human_id_to_cid.json'
with open(index_path, 'r') as f:
    index = json.load(f)

reminted = 0
for old_id, new_id in renames.items():
    old_cid = index.get(old_id)
    if not old_cid:
        print(f"  SKIP: {old_id} not in index")
        continue
    
    # Load old concept
    concept = load_concept(old_cid)
    if 'error' in concept:
        print(f"  ERROR loading {old_id}: {concept['error']}")
        continue
    
    # Update human_id (content was already changed by normalization script)
    concept['human_id'] = new_id
    if concept.get('title') == old_id:
        concept['title'] = new_id.replace('_', ' ').title()
    
    # Add supersedes metadata
    concept['metadata']['supersedes'] = old_cid
    concept['metadata']['version'] = concept['metadata'].get('version', 1) + 1
    
    # Generate new CID
    result = cid_gen.generate_cid(concept)
    if not result['success']:
        print(f"  CID generation failed for {new_id}")
        continue
    
    new_cid = result['cid']
    
    # Save new CBOR
    new_path = BLOCKS_DIR / f"{new_cid}.cbor"
    with open(new_path, 'wb') as f:
        f.write(dag_cbor.encode(concept))
    
    # Create provenance record
    try:
        pm.create_provenance_record(
            concept_cid=new_cid,
            author="CADMIES Normalization Script",
            record_type="supersedes",
            comment=f"Normalized human_id: {old_id} → {new_id}"
        )
    except Exception as e:
        print(f"  WARNING: Provenance failed for {new_id}: {e}")
    
    # Remove old CBOR
    old_path = BLOCKS_DIR / f"{old_cid}.cbor"
    if not old_path.exists():
        old_path = BLOCKS_DIR / old_cid
    if old_path.exists():
        old_path.unlink()
    
    # Update index
    del index[old_id]
    index[new_id] = new_cid
    
    print(f"  ✅ {old_id} → {new_id}  (CID: {new_cid[:16]}...)")
    reminted += 1

# Save updated index
with open(index_path, 'w') as f:
    json.dump(index, f, indent=2)

print(f"\nReminted {reminted} concepts. Index now has {len(index)} entries.")
