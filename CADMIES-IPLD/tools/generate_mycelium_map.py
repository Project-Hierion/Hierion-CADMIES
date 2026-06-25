#!/usr/bin/env python3
"""
File: generate_mycelium_map.py
Tool: CADMIES Mycelium Map Generator
Version: 3.0.0
System: CADMIES-IPLD / tools
Status: ACTIVE — Phase 66: Progressive loading, domain-ranked initial view, renderer-agnostic data

Purpose: Dynamically generates mycelium_map.html and concepts_ranked.json from the live blockstore.
         v3.0.0 introduces progressive loading: initial view shows top concepts per canonical domain
         with cross-domain connectors prioritized. Remaining concepts lazy-load as users explore.
         The ranked JSON file is renderer-agnostic — any future map renderer can consume it.

Usage:
    python tools/generate_mycelium_map.py

Output:
    mycelium_map.html (project root) — progressive-loading interactive map
    concepts_ranked.json (project root) — full ranked concept data for lazy loading

Version History:
  v3.0.0 (2026-06-24): Phase 66 — Progressive loading with domain-ranked initial view.
      Concepts scored by edge count + cross-domain bonus. Top 5-8 per canonical domain
      load initially (~100 nodes). Remaining concepts stream in on zoom/pan/click.
      Separate concepts_ranked.json for renderer-agnostic data consumption.
  v2.4.0 (2026-05-27): Map UX — node collision spacing, click-to-highlight, legend domain
      filter with cross-domain ghosting, gradient edge fade.
  v2.3.0: Canonical 15-domain legend, directional arrows, concept cards.
  v2.2.0: Interactive legend, keyboard shortcuts, responsive design.
  v2.1.0: Zoom buttons, concept search, hover tooltips.
  v2.0.0: Initial D3/Cytoscape map generator.
"""

import json, sys, webbrowser
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

# === CONFIG ===
OUTPUT_FILE = PROJECT_ROOT / "mycelium_map.html"
RANKED_DATA_FILE = PROJECT_ROOT / "concepts_ranked.json"

# How many concepts to load initially per domain (based on domain size)
INITIAL_PER_DOMAIN_LARGE = 8    # Domains with 30+ concepts
INITIAL_PER_DOMAIN_MEDIUM = 6   # Domains with 15-29 concepts
INITIAL_PER_DOMAIN_SMALL = 4    # Domains with <15 concepts
CROSS_DOMAIN_BONUS = 3          # Extra points per cross-domain edge

# === CANONICAL TOP-LEVEL DOMAINS (Phase 44) ===
CANONICAL_DOMAINS = [
    "Physics",
    "Philosophy",
    "Biology",
    "Mathematics",
    "Consciousness",
    "Chemistry",
    "Ethics",
    "Computer Science",
    "Psychology",
    "Spirituality",
    "Neuroscience",
    "Sociology",
    "Economics",
    "Ecology",
    "Medicine",
]

DOMAIN_COLORS = {
    "Physics": "#4F46E5",
    "Philosophy": "#6366F1",
    "Biology": "#10B981",
    "Mathematics": "#1E1B4B",
    "Consciousness": "#0F172A",
    "Chemistry": "#F59E0B",
    "Ethics": "#EC4899",
    "Computer Science": "#3B82F6",
    "Psychology": "#14B8A6",
    "Spirituality": "#A78BFA",
    "Neuroscience": "#14B8A6",
    "Sociology": "#EC4899",
    "Economics": "#F59E0B",
    "Ecology": "#10B981",
    "Medicine": "#10B981",
}
DEFAULT_COLOR = "#64748B"

# === UPWARD MAPPING ===
DOMAIN_UPWARD_MAP = {
    "Theoretical Physics": "Physics",
    "Cosmology": "Physics",
    "Complexity_Science": "Physics",
    "Astrophysics": "Physics",
    "Physics (String Theory)": "Physics",
    "Physics, Quantum Field Theory": "Physics",
    "Quantum Mechanics, Philosophy": "Physics",
    "Quantum Physics and Philosophy": "Physics",
    "Quantum Physics, Consciousness Studies": "Physics",
    "Physics and Philosophy": "Physics",
    "Physics & Philosophy": "Physics",
    "Physics, Philosophy": "Physics",
    "Philosophy, Physics": "Philosophy",
    "Physics, Metaphysics": "Physics",
    "Metaphysics, Philosophy": "Philosophy",
    "Physics, Philosophy, Consciousness": "Physics",
    "Physics, Philosophy, Biology": "Physics",
    "Physics, Biology, Ecology": "Physics",
    "Physics, Biology, Computer Science": "Physics",
    "Neurology and Quantum Physics": "Neuroscience",
    "Epistemology": "Philosophy",
    "Metaphysics": "Philosophy",
    "Buddhist_Philosophy": "Philosophy",
    "Philosophy of Art": "Philosophy",
    "Art, Philosophy": "Philosophy",
    "Art & Philosophy": "Philosophy",
    "Philosophy of Daily Life": "Philosophy",
    "Philosophy of Technology": "Philosophy",
    "Technology, Philosophy": "Philosophy",
    "Technology & Philosophy": "Philosophy",
    "Philosophy of Science & Spirituality": "Philosophy",
    "Philosophy of Science": "Philosophy",
    "Philosophy of Science & Nature": "Philosophy",
    "Philosophy of Physics": "Philosophy",
    "Philosophy of Language": "Philosophy",
    "Philosophy of Mind": "Philosophy",
    "Philosophy of Religion": "Philosophy",
    "Philosophy of Law": "Philosophy",
    "Philosophy of Perception & Sound": "Philosophy",
    "Philosophy of Perception & Scent": "Philosophy",
    "Philosophy, Meditation": "Philosophy",
    "Philosophy & Neuroscience": "Philosophy",
    "Philosophy & Psychology": "Philosophy",
    "Metaphysics & Philosophy of Mind": "Philosophy",
    "Literature & Philosophy": "Philosophy",
    "Symbolism, Philosophy": "Philosophy",
    "Science & Philosophy": "Philosophy",
    "Science, Philosophy": "Philosophy",
    "MolecularBiology": "Biology",
    "Genomics": "Biology",
    "Biology, Philosophy": "Biology",
    "Evolutionary Biology": "Biology",
    "Botany": "Biology",
    "Biology & Marketing": "Biology",
    "Biology & Business": "Biology",
    "Biology and Philosophy of Mind": "Biology",
    "Computer Science, Biology": "Computer Science",
    "Cognitive_Science": "Psychology",
    "Cognitive Science": "Psychology",
    "Cognitive Processes": "Psychology",
    "ConsciousnessStudies": "Consciousness",
    "Psychology, Physics": "Psychology",
    "Psychology and Neuroscience": "Psychology",
    "Neuroscience & Philosophy": "Neuroscience",
    "Consciousness & Philosophy": "Consciousness",
    "Climate Ethics": "Ethics",
    "Ethics, Social Science": "Ethics",
    "Ethics & Philosophy of Mind": "Ethics",
    "Law and Business Ethics": "Ethics",
    "Law and Philosophy": "Philosophy",
    "Philanthropy": "Ethics",
    "Project Management, Ethics": "Ethics",
    "Project Management, Philosophy": "Philosophy",
    "Artificial Intelligence": "Computer Science",
    "AI": "Computer Science",
    "Computer Science, Philosophy": "Computer Science",
    "Science & Technology": "Computer Science",
    "Technology & Society": "Sociology",
    "Politics and Law": "Sociology",
    "Governance": "Sociology",
    "Communication": "Sociology",
    "Cultural Movement": "Sociology",
    "Creativity, Collaboration": "Sociology",
    "Food & Language": "Sociology",
    "Project Management": "Sociology",
    "Project Management, Governance": "Sociology",
    "Project Financing": "Economics",
    "Linguistics": "Philosophy",
    "Knowledge Management": "Sociology",
    "Buddhism": "Spirituality",
    "Biomysticism": "Philosophy",
    "Quantum Physics & Philosophy": "Physics",
    "Philosophy, Religion, Physics": "Philosophy",
    "Neuroscience & Quantum Physics": "Neuroscience",
    "Philosophy, Psychology": "Philosophy",
    "Philosophy, Consciousness": "Philosophy",
    "Astrobiology": "Biology",
    "Philosophy/Quantum Physics": "Physics",
    "Metaphysics & Philosophy": "Philosophy",
    "Neuroscience/Philosophy": "Neuroscience",
    "Genetics": "Biology",
    "Quantum Physics": "Physics",
    "Thermodynamics": "Physics",
    "Geology": "Physics",
    "Biochemistry": "Chemistry",
    "Environmental Science": "Ecology",
    "Microbiology": "Biology",
    "Earth Sciences": "Physics",
    "Cell Biology": "Biology",
    "Science": "Philosophy",
    "Cell Biology, Physiology": "Biology",
    "Chemistry & Biology": "Chemistry",
    "Molecular Biology, Genetics": "Biology",
    "Neuroscience, Chemistry, Psychology": "Neuroscience",
    "Physics & Atmospheric Science": "Physics",
}

def normalize_domain(domain):
    if domain in CANONICAL_DOMAINS:
        return domain
    if domain in DOMAIN_UPWARD_MAP:
        return DOMAIN_UPWARD_MAP[domain]
    print(f"  NOTE: Unmapped domain '{domain}' — using default color. Consider adding to DOMAIN_UPWARD_MAP.")
    return domain

EDGE_COLORS = {
    "builds_upon": "#10B981", "related_to": "#F59E0B",
    "specializes": "#8B5CF6", "contradicts": "#EF4444",
}

DEEPSEEK_INDIGO = "#4F46E5"
DEEPSEEK_NAVY = "#1E1B4B"

LEGACY_EDGES_FILE = TOOLS_DIR / "legacy_edges.json"

def load_legacy_edges():
    if not LEGACY_EDGES_FILE.exists():
        return []
    with open(LEGACY_EDGES_FILE, "r") as f:
        return json.load(f)

def gather_concepts():
    """Load all concepts from blockstore and return (nodes, edges, domain_counts, ranked_data).
    
    The ranked_data dict is renderer-agnostic — any future map renderer can consume it.
    It contains every concept with its score, domain, edges, and whether it's in the initial load set.
    """
    all_cids = load_all_concept_cids()
    print(f"Loading {len(all_cids)} concepts from blockstore...")
    
    # First pass: load all concepts into memory
    concepts = {}
    skipped = 0
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            skipped += 1
            continue
        hid = concept.get('human_id', '')
        concepts[hid] = concept
    
    # Build node list, edge list, and domain tracking
    nodes, node_ids = [], set()
    domain_counts = Counter()
    canonical_domain_concepts = defaultdict(list)
    
    # Build full edge list from blockstore relationships
    all_edges = []
    for hid, concept in concepts.items():
        rels = concept.get('relationships', {})
        for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
            for target in rels.get(rel_type, []):
                if isinstance(target, str):
                    all_edges.append({
                        "source": hid, "target": target, "type": rel_type,
                    })
    
    # Merge with legacy edges
    legacy_edges = load_legacy_edges()
    merged = {}
    for e in all_edges:
        merged[(e["source"], e["target"], e["type"])] = e
    for e in legacy_edges:
        merged[(e["source"], e["target"], e["type"])] = e
    all_edges = list(merged.values())
    
    # Build edge lookup: for each concept, what does it connect to?
    outgoing_edges = defaultdict(list)
    incoming_edges = defaultdict(list)
    for e in all_edges:
        outgoing_edges[e["source"]].append(e)
        incoming_edges[e["target"]].append(e)
    
    # Compute edge counts and cross-domain status for every concept
    concept_scores = {}
    for hid, concept in concepts.items():
        raw_domain = concept.get('domain', 'Unknown')
        display_domain = normalize_domain(raw_domain)
        
        out_edges = outgoing_edges.get(hid, [])
        in_edges = incoming_edges.get(hid, [])
        total_edges = len(out_edges) + len(in_edges)
        
        # Count cross-domain edges
        cross_domain_count = 0
        connected_domains = set()
        for e in out_edges + in_edges:
            other = e["target"] if e["source"] == hid else e["source"]
            if other in concepts:
                other_domain = normalize_domain(concepts[other].get('domain', 'Unknown'))
                if other_domain != display_domain:
                    cross_domain_count += 1
                    connected_domains.add(other_domain)
        
        # Score: edge count + cross-domain bonus
        score = total_edges + (cross_domain_count * CROSS_DOMAIN_BONUS)
        
        concept_scores[hid] = {
            "human_id": hid,
            "title": concept.get('title', hid.replace('_', ' ').title()),
            "domain": display_domain,
            "raw_domain": raw_domain,
            "definition": concept.get('definition', '')[:200],
            "edge_count": total_edges,
            "cross_domain_edges": cross_domain_count,
            "connected_domains": list(connected_domains),
            "score": score,
        }
        
        canonical_domain_concepts[display_domain].append(hid)
        domain_counts[display_domain] += 1
    
    # Determine initial load set: top N per canonical domain by score
    initial_hids = set()
    for domain in CANONICAL_DOMAINS:
        domain_hids = canonical_domain_concepts.get(domain, [])
        domain_size = len(domain_hids)
        
        if domain_size >= 30:
            take = INITIAL_PER_DOMAIN_LARGE
        elif domain_size >= 15:
            take = INITIAL_PER_DOMAIN_MEDIUM
        elif domain_size > 0:
            take = INITIAL_PER_DOMAIN_SMALL
        else:
            continue
        
        # Sort by score descending, take top N
        ranked = sorted(domain_hids, key=lambda h: concept_scores[h]["score"], reverse=True)
        initial_hids.update(ranked[:take])
    
    # Ensure cross-domain connectors get priority — if a concept connects 3+ domains, always include it
    for hid, score_data in concept_scores.items():
        if len(score_data["connected_domains"]) >= 3:
            initial_hids.add(hid)
    
    # Build node objects for ALL concepts (for the ranked JSON)
    all_nodes_data = []
    for hid, score_data in concept_scores.items():
        all_nodes_data.append({
            "id": hid,
            "label": score_data["title"],
            "color": DOMAIN_COLORS.get(score_data["domain"], DEFAULT_COLOR),
            "domain": score_data["domain"],
            "definition": score_data["definition"],
            "score": score_data["score"],
            "edge_count": score_data["edge_count"],
            "cross_domain_edges": score_data["cross_domain_edges"],
            "initial": hid in initial_hids,
        })
        node_ids.add(hid)
    
    # Filter edges: only edges where both ends exist as concepts
    valid_edges = [e for e in all_edges if e["source"] in node_ids and e["target"] in node_ids]
    orphan = len(all_edges) - len(valid_edges)
    if orphan:
        print(f"  Filtered {orphan} orphan edge(s)")
    
    print(f"  {len(all_nodes_data)} nodes, {len(valid_edges)} edges, {skipped} skipped")
    print(f"  Domains in data: {len(domain_counts)} (canonical with concepts: {len([d for d in CANONICAL_DOMAINS if d in domain_counts])})")
    print(f"  Initial load: {len(initial_hids)} concepts (of {len(all_nodes_data)} total)")
    
    # Build ranked data for export (renderer-agnostic)
    ranked_data = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "total_concepts": len(all_nodes_data),
        "total_edges": len(valid_edges),
        "canonical_domains": CANONICAL_DOMAINS,
        "initial_load_count": len(initial_hids),
        "concepts": all_nodes_data,
        "edges": valid_edges,
    }
    
    return all_nodes_data, valid_edges, domain_counts, ranked_data, initial_hids

def generate_html(nodes, edges, domain_counts, initial_hids):
    """Generate the HTML map with progressive loading support."""
    
    # Separate initial and lazy nodes
    initial_nodes = [n for n in nodes if n["id"] in initial_hids]
    
    # Build inline JSON for initial load
    nodes_json = []
    for n in initial_nodes:
        escaped_id = n["id"].replace('"', '\\"')
        escaped_label = n["label"].replace('"', '\\"')
        escaped_def = n.get("definition", "").replace('"', '\\"')
        escaped_domain = n.get("domain", "").replace('"', '\\"')
        nodes_json.append(
            '{{ data: {{ id: "{}", label: "{}", definition: "{}", domain: "{}", background_color: "{}" }} }}'.format(
                escaped_id, escaped_label, escaped_def, escaped_domain, n["color"]
            )
        )
    
    # Initial edges: only edges where both ends are in the initial set
    initial_edges = [e for e in edges if e["source"] in initial_hids and e["target"] in initial_hids]
    edges_json = []
    for e in initial_edges:
        escaped_source = e["source"].replace('"', '\\"')
        escaped_target = e["target"].replace('"', '\\"')
        edges_json.append(
            '{{ data: {{ source: "{}", target: "{}", label: "{}" }} }}'.format(
                escaped_source, escaped_target, e["type"]
            )
        )
    
    # Legend items
    legend_items = []
    for domain in CANONICAL_DOMAINS:
        if domain in domain_counts:
            color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
            legend_items.append(
                '<div class="legend-item"><div class="color-box" style="background:{}"></div><span>{}</span></div>'.format(
                    color, domain.replace('_', ' ')
                )
            )
    
    edge_legend = '''
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px solid #10B981"></div><span>→ builds_upon</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px solid #F59E0B"></div><span>— related_to</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px dashed #8B5CF6"></div><span>→ specializes</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:3px solid #EF4444"></div><span>→ contradicts</span></div>'''
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    info_text = 'CADMIES Mycelium Map | {} nodes ({} initial) | {} edges | {} | Click node for details | / to search | Esc to reset | Scroll to load more'.format(
        len(nodes), len(initial_nodes), len(edges), timestamp
    )
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>CADMIES Mycelium Map</title>
    <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #FFFFFF; overflow: hidden; }
        #cy { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; }
        #loading { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #0F172A; color: #FFFFFF; padding: 12px 24px; border-radius: 8px; font-size: 13px; z-index: 5000; display: none; font-family: monospace; }
        #info { position: absolute; bottom: 12px; left: 12px; background: #0F172A; color: #FFFFFF; padding: 8px 14px; border-radius: 8px; font-size: 11px; z-index: 100; pointer-events: none; font-family: monospace; }
        #searchBox { position: absolute; top: 20px; left: 20px; z-index: 1000; }
        #searchInput { padding: 10px 14px; font-size: 13px; border: 1px solid #E2E8F0; border-radius: 8px; width: 220px; font-family: sans-serif; outline: none; }
        #searchInput:focus { border-color: #4F46E5; box-shadow: 0 0 0 2px rgba(79,70,229,0.2); }
        .zoom-controls { position: absolute; bottom: 20px; right: 20px; display: flex; flex-direction: column; z-index: 1000; }
        .zoom-btn { font-size: 20px; cursor: pointer; margin: 2px; padding: 8px 14px; border: 1px solid #E2E8F0; background: #0F172A; color: #FFFFFF; border-radius: 8px; font-family: monospace; transition: background 0.2s; }
        .zoom-btn:hover { background: #1E1B4B; }
        .legend-toggle { position: absolute; top: 20px; right: 20px; background: #0F172A; color: #FFFFFF; border-radius: 30px; padding: 10px 16px; font-family: monospace; font-size: 14px; cursor: pointer; z-index: 1000; border: 1px solid #E2E8F0; transition: all 0.2s ease; }
        .legend-toggle:hover { background: #1E1B4B; transform: scale(1.02); }
        .legend-panel { position: absolute; top: 70px; right: 20px; background: #0F172A; color: #FFFFFF; border-radius: 12px; padding: 15px; font-family: monospace; font-size: 11px; border: 1px solid #E2E8F0; z-index: 999; min-width: 180px; transition: all 0.3s ease; opacity: 1; pointer-events: auto; }
        .legend-panel.collapsed { opacity: 0; pointer-events: none; transform: translateX(20px); }
        .legend-panel h4 { margin: 0 0 10px 0; color: #FFFFFF; font-size: 13px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
        .color-box { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; cursor: pointer; }
        .color-box:hover { transform: scale(1.3); }
        .line-sample { width: 20px; height: 2px; flex-shrink: 0; }
        hr { margin: 8px 0; border-color: #475569; border-width: 0.5px; }
        .close-legend { float: right; cursor: pointer; color: #475569; margin-left: 10px; font-size: 14px; }
        .close-legend:hover { color: #FFFFFF; }
        .node-tooltip { position: absolute; background: #0F172A; color: #FFFFFF; padding: 8px 12px; border-radius: 6px; font-size: 11px; z-index: 2000; pointer-events: none; max-width: 280px; display: none; border: 1px solid #475569; }
        .concept-card { position: absolute; background: #0F172A; color: #FFFFFF; border-radius: 12px; padding: 18px 22px; z-index: 3000; max-width: 360px; min-width: 260px; max-height: 80vh; overflow-y: auto; border: 1px solid #475569; box-shadow: 0 8px 32px rgba(0,0,0,0.5); display: none; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; pointer-events: auto; }
        .concept-card h3 { margin: 0 0 4px 0; font-size: 16px; color: #FFFFFF; }
        .concept-card .card-domain { font-size: 11px; color: #94A3B8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .concept-card .card-definition { font-size: 13px; line-height: 1.5; color: #CBD5E1; margin-bottom: 10px; }
        .concept-card .card-relationships { font-size: 11px; color: #94A3B8; border-top: 1px solid #334155; padding-top: 8px; margin-top: 4px; }
        .concept-card .card-relationships span { display: inline-block; margin-right: 8px; margin-bottom: 4px; }
        .concept-card .card-close { position: absolute; top: 8px; right: 12px; cursor: pointer; color: #64748B; font-size: 16px; }
        .concept-card .card-close:hover { color: #FFFFFF; }
        .reset-btn { position: absolute; bottom: 55px; left: 20px; z-index: 1000; cursor: pointer; padding: 6px 12px; font-size: 11px; background: #0F172A; color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; font-family: monospace; }
        .reset-btn:hover { background: #1E1B4B; }
        .load-more-btn { position: absolute; bottom: 55px; left: 140px; z-index: 1000; cursor: pointer; padding: 6px 12px; font-size: 11px; background: #10B981; color: #FFFFFF; border: 1px solid #10B981; border-radius: 6px; font-family: monospace; }
        .load-more-btn:hover { background: #059669; }
    </style>
</head>
<body>
    <div id="cy"></div>
    <div id="loading">Loading concepts...</div>
    <div id="info">''' + info_text + '''</div>
    <div class="node-tooltip" id="nodeTooltip"></div>
    <div class="concept-card" id="conceptCard">
        <span class="card-close" id="cardClose">x</span>
        <h3 id="cardTitle"></h3>
        <div class="card-domain" id="cardDomain"></div>
        <div class="card-definition" id="cardDefinition"></div>
        <div class="card-relationships" id="cardRelationships"></div>
    </div>
    <div id="searchBox"><input id="searchInput" type="text" placeholder="Search concepts..." /></div>
    <div class="zoom-controls">
        <button class="zoom-btn" title="Zoom in" onclick="cy.zoom(cy.zoom() * 1.3); cy.center()">+</button>
        <button class="zoom-btn" title="Zoom out" onclick="cy.zoom(cy.zoom() * 0.7); cy.center()">−</button>
    </div>
    <button class="reset-btn" onclick="resetView()">Reset View</button>
    <button class="load-more-btn" id="loadMoreBtn" onclick="loadMoreConcepts()">Load More</button>
    <div class="legend-toggle" id="legendToggle">Legend</div>
    <div class="legend-panel collapsed" id="legendPanel">
        <span class="close-legend" id="closeLegend">x</span>
        <h4>Mycelium Legend</h4>
        ''' + '\n'.join(legend_items) + '''
        <hr>
        ''' + edge_legend + '''
        <hr>
        <div class="legend-item"><span>Type 'cadmies' for easter egg</span></div>
    </div>
    <script>
        // === INITIAL DATA ===
        var elements = { nodes: [''' + ',\n'.join(nodes_json) + '''], edges: [''' + ',\n'.join(edges_json) + '''] };
        
        // === LAZY DATA STORE ===
        var allRankedConcepts = null;
        var loadedHids = new Set();
        var batchSize = 30;
        var currentBatchIndex = 0;
        var rankedList = [];
        
        // Track which HIDs are initially loaded
        var initialNodeIds = new Set(elements.nodes.map(function(n) { return n.data.id; }));
        initialNodeIds.forEach(function(id) { loadedHids.add(id); });
        
        // === CYTOSCAPE INIT ===
        var cy = cytoscape({
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                { selector: 'node', style: {
                    'label': 'data(label)', 'background-color': 'data(background_color)',
                    'width': 60, 'height': 60, 'font-size': '11px',
                    'text-valign': 'center', 'text-halign': 'center',
                    'color': '#FFFFFF', 'text-wrap': 'wrap',
                    'text-max-width': '54px', 'text-overflow-wrap': 'anywhere',
                    'border-width': 2, 'border-color': '#E2E8F0'
                }},
                { selector: 'edge', style: {
                    'width': 2, 'line-color': '#475569',
                    'curve-style': 'bezier', 'label': 'data(label)',
                    'font-size': '8px', 'text-rotation': 'autorotate',
                    'color': '#475569', 'text-background-color': '#FFFFFF',
                    'text-background-opacity': 0.8, 'text-background-padding': '2px'
                }},
                { selector: 'edge[label = "builds_upon"]', style: { 'line-color': '#10B981', 'width': 2, 'target-arrow-color': '#10B981', 'target-arrow-shape': 'triangle' }},
                { selector: 'edge[label = "related_to"]', style: { 'line-color': '#F59E0B', 'width': 2 }},
                { selector: 'edge[label = "specializes"]', style: { 'line-color': '#8B5CF6', 'line-style': 'dashed', 'width': 2, 'target-arrow-color': '#8B5CF6', 'target-arrow-shape': 'triangle' }},
                { selector: 'edge[label = "contradicts"]', style: { 'line-color': '#EF4444', 'width': 3, 'target-arrow-color': '#EF4444', 'target-arrow-shape': 'triangle' }}
            ],
            layout: {
                name: 'cose',
                idealEdgeLength: 120,
                nodeRepulsion: 6000,
                gravity: 0.15,
                numIter: 2000,
                animate: true,
                animationDuration: 1500,
                nodeOverlap: 20,
                nodeDimensionsIncludeLabels: false
            }
        });

        // === LOAD RANKED DATA FROM JSON ===
        function fetchRankedData() {
            if (allRankedConcepts) return Promise.resolve(allRankedConcepts);
            document.getElementById('loading').style.display = 'block';
            return fetch('concepts_ranked.json')
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    allRankedConcepts = data;
                    // Build ranked list of not-yet-loaded concepts, sorted by score
                    rankedList = data.concepts
                        .filter(function(c) { return !loadedHids.has(c.id); })
                        .sort(function(a, b) { return b.score - a.score; });
                    document.getElementById('loading').style.display = 'none';
                    console.log('Ranked data loaded: ' + data.total_concepts + ' concepts, ' + data.total_edges + ' edges');
                    console.log('Initial load: ' + loadedHids.size + ' concepts, ' + rankedList.length + ' remaining');
                    return data;
                })
                .catch(function(err) {
                    document.getElementById('loading').style.display = 'none';
                    console.error('Failed to load ranked data:', err);
                });
        }

        // === PROGRESSIVE LOADING ===
        function loadMoreConcepts() {
            if (!allRankedConcepts) {
                fetchRankedData().then(function() { loadMoreConcepts(); });
                return;
            }
            
            if (currentBatchIndex >= rankedList.length) {
                document.getElementById('loadMoreBtn').textContent = 'All Loaded';
                document.getElementById('loadMoreBtn').style.opacity = '0.5';
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            
            var batch = rankedList.slice(currentBatchIndex, currentBatchIndex + batchSize);
            currentBatchIndex += batchSize;
            
            // Add new nodes
            var newNodes = batch.map(function(c) {
                return {
                    group: 'nodes',
                    data: {
                        id: c.id,
                        label: c.label,
                        definition: c.definition,
                        domain: c.domain,
                        background_color: c.color
                    }
                };
            });
            
            // Find edges for these new nodes from the ranked data
            var newEdges = [];
            if (allRankedConcepts.edges) {
                var newNodeIds = new Set(batch.map(function(c) { return c.id; }));
                allRankedConcepts.edges.forEach(function(e) {
                    if (newNodeIds.has(e.source) || newNodeIds.has(e.target)) {
                        // Only add if target node exists (initial or already loaded)
                        if (loadedHids.has(e.source) || loadedHids.has(e.target) || newNodeIds.has(e.source) && newNodeIds.has(e.target)) {
                            newEdges.push({
                                group: 'edges',
                                data: {
                                    source: e.source,
                                    target: e.target,
                                    label: e.type
                                }
                            });
                        }
                    }
                });
            }
            
            batch.forEach(function(c) { loadedHids.add(c.id); });
            
            cy.add(newNodes.concat(newEdges));
            
            // Run a quick layout to position new nodes
            cy.layout({
                name: 'cose',
                idealEdgeLength: 120,
                nodeRepulsion: 6000,
                gravity: 0.15,
                numIter: 500,
                animate: true,
                animationDuration: 800,
                nodeOverlap: 20,
                fit: false,
                randomize: false
            }).run();
            
            document.getElementById('loading').style.display = 'none';
            
            var remaining = rankedList.length - currentBatchIndex;
            document.getElementById('loadMoreBtn').textContent = 'Load More (' + remaining + ' left)';
            
            if (remaining <= 0) {
                document.getElementById('loadMoreBtn').textContent = 'All Loaded';
                document.getElementById('loadMoreBtn').style.opacity = '0.5';
            }
            
            // Update info bar
            document.getElementById('info').textContent = 'CADMIES Mycelium Map | ' + allRankedConcepts.total_concepts + ' nodes | ' + loadedHids.size + ' loaded | ' + allRankedConcepts.total_edges + ' edges | / to search | Esc to reset | Scroll to load more';
        }

        // Auto-load on zoom/pan (loads more when user explores)
        var lastAutoLoad = 0;
        cy.on('viewport', function() {
            var now = Date.now();
            if (now - lastAutoLoad > 3000 && currentBatchIndex < rankedList.length && allRankedConcepts) {
                lastAutoLoad = now;
                // Load a smaller batch on auto
                var origBatch = batchSize;
                batchSize = 10;
                loadMoreConcepts();
                batchSize = origBatch;
            }
        });

        // Fetch ranked data in background after initial render
        cy.ready(function() {
            setTimeout(fetchRankedData, 500);
        });

        // Auto-size on zoom
        cy.on('zoom', function() {
            var zoom = cy.zoom();
            var base = Math.max(40, 60 / Math.sqrt(zoom));
            cy.style().selector('node').style({
                'width': base, 'height': base,
                'font-size': Math.max(7, base * 0.18) + 'px',
                'text-max-width': (base * 0.85) + 'px'
            }).update();
        });

        // Search
        var searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', function() {
            var q = this.value.toLowerCase();
            cy.nodes().forEach(function(n) {
                n.style({
                    'opacity': (q === '' || n.data('label').toLowerCase().includes(q)) ? 1 : 0.15,
                    'border-width': (q !== '' && n.data('label').toLowerCase().includes(q)) ? 3 : 2
                });
            });
            if (q === '') { cy.elements().style('opacity', 1); }
        });

        // Click node -> highlight neighborhood + show card
        cy.on('tap', 'node', function(evt) {
            var node = evt.target;
            var card = document.getElementById('conceptCard');
            document.getElementById('cardTitle').textContent = node.data('label');
            document.getElementById('cardDomain').textContent = node.data('domain').replace(/_/g, ' ');
            document.getElementById('cardDefinition').textContent = node.data('definition') || 'No definition available.';

            var rels = [];
            node.connectedEdges().forEach(function(edge) {
                var other = edge.source().id() === node.id() ? edge.target() : edge.source();
                var dir = edge.source().id() === node.id() ? '→' : '←';
                rels.push('<span>' + dir + ' <b>' + edge.data('label') + '</b> ' + other.data('label') + '</span>');
            });
            document.getElementById('cardRelationships').innerHTML = rels.length > 0
                ? rels.join('') : '<span>No relationships yet.</span>';

            card.style.display = 'block';
            card.style.left = Math.min(evt.originalEvent.clientX + 20, window.innerWidth - 360) + 'px';
            card.style.top = Math.min(evt.originalEvent.clientY - 30, window.innerHeight - 300) + 'px';

            // Fade non-connected, highlight neighborhood
            cy.elements().style('opacity', 0.1);
            node.style('opacity', 1);
            var connectedEdges = node.connectedEdges();
            var connectedNodes = connectedEdges.connectedNodes();
            connectedEdges.style('opacity', 0.8);
            connectedNodes.style('opacity', 1);

            // Gradient fade on edges: closer to clicked node = brighter
            connectedEdges.forEach(function(edge) {
                var sourceDist = edge.source().id() === node.id() ? 0 : 1;
                edge.style('opacity', sourceDist === 0 ? 0.9 : 0.5);
            });
        });

        // Click background -> reset
        cy.on('tap', function(evt) {
            if (evt.target === cy) {
                resetView();
            }
        });

        document.getElementById('cardClose').addEventListener('click', function() {
            document.getElementById('conceptCard').style.display = 'none';
        });

        function resetView() {
            cy.elements().style('opacity', 1);
            document.getElementById('conceptCard').style.display = 'none';
            cy.fit();
            cy.center();
        }

        // Tooltip
        var tooltip = document.getElementById('nodeTooltip');
        cy.on('mouseover', 'node', function(evt) {
            var n = evt.target;
            tooltip.innerHTML = '<strong>' + n.data('label') + '</strong><br><small>' + (n.data('definition') || '') + '</small>';
            tooltip.style.display = 'block';
            tooltip.style.left = (evt.originalEvent.clientX + 15) + 'px';
            tooltip.style.top = (evt.originalEvent.clientY + 15) + 'px';
        });
        cy.on('mousemove', 'node', function(evt) {
            tooltip.style.left = (evt.originalEvent.clientX + 15) + 'px';
            tooltip.style.top = (evt.originalEvent.clientY + 15) + 'px';
        });
        cy.on('mouseout', 'node', function() {
            tooltip.style.display = 'none';
        });

        // Legend domain filter
        document.querySelectorAll('.legend-item .color-box').forEach(function(box) {
            box.addEventListener('click', function() {
                var domainText = this.nextElementSibling.textContent.trim();
                cy.nodes().forEach(function(n) {
                    if (n.data('domain') === domainText) {
                        n.style({ 'opacity': 1, 'border-width': 3 });
                    } else {
                        n.style({ 'opacity': 0.08, 'border-width': 1 });
                    }
                });
                cy.edges().forEach(function(e) {
                    var srcVisible = e.source().data('domain') === domainText;
                    var tgtVisible = e.target().data('domain') === domainText;
                    if (srcVisible || tgtVisible) {
                        e.style('opacity', 0.4);
                    } else {
                        e.style('opacity', 0.04);
                    }
                });
            });
        });

        // Legend toggle
        document.getElementById('legendToggle').addEventListener('click', function() {
            document.getElementById('legendPanel').classList.toggle('collapsed');
        });
        document.getElementById('closeLegend').addEventListener('click', function() {
            document.getElementById('legendPanel').classList.add('collapsed');
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.key === '/' && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
            if (e.key === 'Escape') {
                resetView();
                searchInput.value = '';
                cy.elements().style('opacity', 1);
            }
        });

        // Easter egg
        var keyBuffer = [];
        document.addEventListener('keydown', function(e) {
            if (e.key.length === 1 && /[a-zA-Z]/.test(e.key)) {
                keyBuffer.push(e.key.toLowerCase());
                if (keyBuffer.length > 7) keyBuffer.shift();
                if (keyBuffer.join('') === 'cadmies') {
                    cy.style().selector('node').style({
                        'background-color': '#ffd700', 'border-color': '#ff6600',
                        'border-width': '3px', 'shape': 'ellipse'
                    }).update();
                    var msg = document.createElement('div');
                    msg.innerHTML = '<div style="text-align:center"><div style="font-size:20px;font-weight:bold">LET THE GOOD TIMES ROLL WITH CADMIES!</div><div style="font-size:12px;font-style:italic;color:#ffd700;margin-top:5px">homage to The Cars</div></div>';
                    msg.style.cssText = 'position:fixed;bottom:50px;left:50%;transform:translateX(-50%);background:linear-gradient(90deg,#ff6600,#ffd700);color:black;padding:12px 24px;border-radius:50px;z-index:9999;font-family:monospace;box-shadow:0 0 20px rgba(255,102,0,0.5);animation:fadeInOut 3s ease-in-out';
                    document.body.appendChild(msg);
                    var style = document.createElement('style');
                    style.textContent = '@keyframes fadeInOut { 0% { opacity:0; transform:translateX(-50%) scale(0.8); } 20% { opacity:1; transform:translateX(-50%) scale(1); } 80% { opacity:1; transform:translateX(-50%) scale(1); } 100% { opacity:0; transform:translateX(-50%) scale(0.8); } }';
                    document.head.appendChild(style);
                    setTimeout(function() { msg.remove(); }, 4000);
                    keyBuffer = [];
                }
            }
        });
    </script>
</body>
</html>'''
    return html

def main():
    print("=" * 60)
    print("CADMIES MYCELIUM MAP GENERATOR v3.0.0")
    print(f"Blockstore: {BLOCKS_DIR}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Ranked data: {RANKED_DATA_FILE}")
    print(f"Canonical domains: {len(CANONICAL_DOMAINS)}")
    print("=" * 60)
    
    nodes, edges, domain_counts, ranked_data, initial_hids = gather_concepts()
    
    if not nodes:
        print("\nERROR: No concepts loaded.")
        sys.exit(1)
    
    # Write ranked data JSON (renderer-agnostic)
    with open(RANKED_DATA_FILE, "w") as f:
        json.dump(ranked_data, f, indent=2)
    print(f"\nRanked data saved: {RANKED_DATA_FILE}")
    print(f"   {ranked_data['total_concepts']} concepts, {ranked_data['total_edges']} edges")
    print(f"   Initial load: {ranked_data['initial_load_count']} concepts")
    
    # Generate HTML
    html = generate_html(nodes, edges, domain_counts, initial_hids)
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    print(f"\nMap generated: {OUTPUT_FILE}")
    print(f"   {len(nodes)} total nodes, {len(edges)} total edges, {len(domain_counts)} domains in data")
    legend_domains = [d for d in CANONICAL_DOMAINS if d in domain_counts]
    print(f"   Legend: {len(legend_domains)} canonical domains shown")
    print(f"   Phase 66: Progressive loading — {len(initial_hids)} concepts initial, {len(nodes) - len(initial_hids)} lazy-loaded")
    print(f"   Features: zoom, search, tooltips, concept cards, directional arrows, interactive legend, keyboard shortcuts, node collision spacing, click-to-highlight, legend domain filter, progressive loading via 'Load More' button + auto-load on pan/zoom")
    print(f"   Data layer: concepts_ranked.json — renderer-agnostic, consumable by any future map renderer")
    
    # Update Tkinter page count
    tkinter_page = PROJECT_ROOT / "cadmies-gui" / "pages" / "tkinter_mycelium_map.py"
    if tkinter_page.exists():
        with open(tkinter_page, "r") as f:
            content = f.read()
        content = content.replace('all 119 concepts', f'all {len(nodes)} concepts').replace('all 116 concepts', f'all {len(nodes)} concepts')
        with open(tkinter_page, "w") as f:
            f.write(content)
        print(f"   Updated Tkinter page count to {len(nodes)} concepts.")
    
    try:
        webbrowser.open(f"file://{OUTPUT_FILE}")
        print(f"   Opened map in browser.")
    except:
        pass

if __name__ == "__main__":
    main()