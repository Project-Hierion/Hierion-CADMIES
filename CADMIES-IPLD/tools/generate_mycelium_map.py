#!/usr/bin/env python3
"""
File: generate_mycelium_map.py
Tool: CADMIES Mycelium Map Generator
Version: 2.3.0
System: CADMIES-IPLD / tools
Status: ACTIVE — Phase 44: canonical 15-domain legend, directional arrows, concept cards

Purpose: Dynamically generates mycelium_map.html from the live blockstore.
         Enhanced features: zoom buttons, concept search, hover tooltips,
         click-to-highlight connections, interactive domain legend,
         keyboard shortcuts, responsive design, directional edge arrows,
         concept info cards on click.

Usage:
    python tools/generate_mycelium_map.py

Output:
    mycelium_map.html (project root) — open in any modern browser
"""

import json, sys, webbrowser
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

# === CONFIG ===
OUTPUT_FILE = PROJECT_ROOT / "mycelium_map.html"

# === CANONICAL TOP-LEVEL DOMAINS (Phase 44) ===
# Only these 15 domains appear in the map legend.
# All other domains map upward to the closest canonical parent.
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

# DeepSeek-themed colors for canonical domains
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
# Every non-canonical domain maps to its closest canonical parent.
# Subdomains, compound domains, and specialty fields all resolve here.
DOMAIN_UPWARD_MAP = {
    # === Physics subdomains & compounds ===
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

    # === Philosophy subdomains & compounds ===
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
    "Philosophy & Psychology": "Philosophy",
    "Metaphysics & Philosophy of Mind": "Philosophy",
    "Literature & Philosophy": "Philosophy",
    "Symbolism, Philosophy": "Philosophy",
    "Science & Philosophy": "Philosophy",
    "Science, Philosophy": "Philosophy",
    "Science & Philosophy": "Philosophy",

    # === Biology subdomains & compounds ===
    "MolecularBiology": "Biology",
    "Genomics": "Biology",
    "Biology, Philosophy": "Biology",
    "Evolutionary Biology": "Biology",
    "Botany": "Biology",
    "Biology & Marketing": "Biology",
    "Biology & Business": "Biology",
    "Biology and Philosophy of Mind": "Biology",
    "Computer Science, Biology": "Computer Science",

    # === Psychology / Cognitive Science ===
    "Cognitive_Science": "Psychology",
    "Cognitive Science": "Psychology",
    "Cognitive Processes": "Psychology",
    "ConsciousnessStudies": "Consciousness",
    "Psychology, Physics": "Psychology",
    "Psychology and Neuroscience": "Psychology",
    "Neuroscience & Philosophy": "Neuroscience",
    "Consciousness & Philosophy": "Consciousness",

    # === Ethics subdomains & compounds ===
    "Climate Ethics": "Ethics",
    "Ethics, Social Science": "Ethics",
    "Ethics & Philosophy of Mind": "Ethics",
    "Law and Business Ethics": "Ethics",
    "Law and Philosophy": "Philosophy",
    "Philanthropy": "Ethics",
    "Project Management, Ethics": "Ethics",
    "Project Management, Philosophy": "Philosophy",

    # === Computer Science subdomains & compounds ===
    "Artificial Intelligence": "Computer Science",
    "AI": "Computer Science",
    "Computer Science, Philosophy": "Computer Science",
    "Science & Technology": "Computer Science",
    "Technology & Society": "Sociology",

    # === Sociology (social structures, governance, culture, communication) ===
    "Politics and Law": "Sociology",
    "Governance": "Sociology",
    "Communication": "Sociology",
    "Cultural Movement": "Sociology",
    "Creativity, Collaboration": "Sociology",
    "Food & Language": "Sociology",
    "Project Management": "Sociology",
    "Project Management, Governance": "Sociology",

    # === Economics ===
    "Project Financing": "Economics",

    # === Linguistics (philosophy of language) ===
    "Linguistics": "Philosophy",

    # === Knowledge Management (social knowledge systems) ===
    "Knowledge Management": "Sociology",

    # === Buddhism / Spirituality ===
    "Buddhism": "Spirituality",
    # Phase 46 final batch (Session 015)
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
}

def normalize_domain(domain):
    """Map any domain to its canonical parent.
    If already canonical, return as-is.
    If in upward map, return the canonical parent.
    Otherwise, return as-is (will get default color, flagged for review).
    """
    if domain in CANONICAL_DOMAINS:
        return domain
    if domain in DOMAIN_UPWARD_MAP:
        return DOMAIN_UPWARD_MAP[domain]
    # Unknown domain — log it so we can decide where it belongs
    print(f"  NOTE: Unmapped domain '{domain}' — using default color. Consider adding to DOMAIN_UPWARD_MAP.")
    return domain

EDGE_COLORS = {
    "builds_upon": "#10B981", "related_to": "#F59E0B",
    "specializes": "#8B5CF6", "contradicts": "#EF4444",
}

# DeepSeek theme constants
WHITE = "#FFFFFF"
DEEPSEEK_INDIGO = "#4F46E5"
DEEPSEEK_NAVY = "#1E1B4B"
DEEPSEEK_ACCENT = "#6366F1"
DEEPSEEK_SURFACE = "#F8FAFC"
DEEPSEEK_TEXT = "#0F172A"
DEEPSEEK_TEXT_LIGHT = "#475569"
DEEPSEEK_SUBTLE = "#E2E8F0"

LEGACY_EDGES_FILE = TOOLS_DIR / "legacy_edges.json"


def load_legacy_edges():
    if not LEGACY_EDGES_FILE.exists():
        return []
    with open(LEGACY_EDGES_FILE, "r") as f:
        return json.load(f)


def gather_concepts():
    """Load all concepts, extract graph data, merge with legacy edges.
    All domains are normalized to canonical top-level domains.
    """
    all_cids = load_all_concept_cids()
    print(f"Loading {len(all_cids)} concepts from blockstore...")

    nodes, node_ids = [], set()
    skipped = 0
    domain_counts = Counter()

    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            skipped += 1
            continue
        hid = concept.get('human_id', '')
        title = concept.get('title', hid.replace('_', ' ').title())
        raw_domain = concept.get('domain', 'Unknown')
        # Normalize to canonical top-level domain
        display_domain = normalize_domain(raw_domain)
        definition = concept.get('definition', '')[:200]
        domain_counts[display_domain] += 1
        color = DOMAIN_COLORS.get(display_domain, DEFAULT_COLOR)
        nodes.append({
            "id": hid, "label": title, "color": color,
            "domain": display_domain, "definition": definition,
        })
        node_ids.add(hid)

    # Gather blockstore edges
    blockstore_edges = []
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        hid = concept.get('human_id', '')
        rels = concept.get('relationships', {})
        for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
            for target in rels.get(rel_type, []):
                if isinstance(target, str):
                    blockstore_edges.append({
                        "source": hid, "target": target, "type": rel_type,
                    })

    # Merge with legacy edges
    legacy_edges = load_legacy_edges()
    merged = {}
    for e in blockstore_edges:
        merged[(e["source"], e["target"], e["type"])] = e
    for e in legacy_edges:
        merged[(e["source"], e["target"], e["type"])] = e

    all_edges = list(merged.values())
    valid_edges = [e for e in all_edges if e["source"] in node_ids and e["target"] in node_ids]
    orphan = len(all_edges) - len(valid_edges)
    if orphan:
        print(f"  Filtered {orphan} orphan edge(s)")

    print(f"  {len(nodes)} nodes, {len(valid_edges)} edges, {skipped} skipped")
    print(f"  Domains in legend: {len(domain_counts)} (canonical: {len([d for d in domain_counts if d in CANONICAL_DOMAINS])})")
    return nodes, valid_edges, domain_counts


def build_html_template():
    """Return the HTML/CSS/JS template with placeholders for dynamic content."""
    return '''<!DOCTYPE html>
<html>
<head>
    <title>CADMIES Mycelium Map</title>
    <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #FFFFFF;
            overflow: hidden;
        }
        #cy {
            width: 100vw; height: 100vh;
            position: absolute; top: 0; left: 0;
        }
        #info {
            position: absolute; bottom: 12px; left: 12px;
            background: #0F172A; color: #FFFFFF;
            padding: 8px 14px; border-radius: 8px;
            font-size: 11px; z-index: 100;
            pointer-events: none; font-family: monospace;
        }
        #searchBox {
            position: absolute; top: 20px; left: 20px;
            z-index: 1000;
        }
        #searchInput {
            padding: 10px 14px; font-size: 13px;
            border: 1px solid #E2E8F0; border-radius: 8px;
            width: 220px; font-family: sans-serif;
            outline: none;
        }
        #searchInput:focus {
            border-color: #4F46E5; box-shadow: 0 0 0 2px rgba(79,70,229,0.2);
        }
        .zoom-controls {
            position: absolute; bottom: 20px; right: 20px;
            display: flex; flex-direction: column; z-index: 1000;
        }
        .zoom-btn {
            font-size: 20px; cursor: pointer;
            margin: 2px; padding: 8px 14px;
            border: 1px solid #E2E8F0;
            background: #0F172A; color: #FFFFFF;
            border-radius: 8px; font-family: monospace;
            transition: background 0.2s;
        }
        .zoom-btn:hover { background: #1E1B4B; }
        .legend-toggle {
            position: absolute; top: 20px; right: 20px;
            background: #0F172A; color: #FFFFFF;
            border-radius: 30px; padding: 10px 16px;
            font-family: monospace; font-size: 14px;
            cursor: pointer; z-index: 1000;
            border: 1px solid #E2E8F0;
            transition: all 0.2s ease;
        }
        .legend-toggle:hover {
            background: #1E1B4B; transform: scale(1.02);
        }
        .legend-panel {
            position: absolute; top: 70px; right: 20px;
            background: #0F172A; color: #FFFFFF;
            border-radius: 12px; padding: 15px;
            font-family: monospace; font-size: 11px;
            border: 1px solid #E2E8F0; z-index: 999;
            min-width: 180px;
            transition: all 0.3s ease;
            opacity: 1; pointer-events: auto;
        }
        .legend-panel.collapsed {
            opacity: 0; pointer-events: none;
            transform: translateX(20px);
        }
        .legend-panel h4 {
            margin: 0 0 10px 0; color: #FFFFFF;
            font-size: 13px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .legend-item {
            display: flex; align-items: center;
            gap: 8px; margin-bottom: 5px;
        }
        .color-box {
            width: 12px; height: 12px;
            border-radius: 50%; flex-shrink: 0;
            cursor: pointer;
        }
        .color-box:hover { transform: scale(1.3); }
        .line-sample {
            width: 20px; height: 2px; flex-shrink: 0;
        }
        hr { margin: 8px 0; border-color: #475569; border-width: 0.5px; }
        .close-legend {
            float: right; cursor: pointer;
            color: #475569; margin-left: 10px; font-size: 14px;
        }
        .close-legend:hover { color: #FFFFFF; }
        .node-tooltip {
            position: absolute;
            background: #0F172A; color: #FFFFFF;
            padding: 8px 12px; border-radius: 6px;
            font-size: 11px; z-index: 2000;
            pointer-events: none; max-width: 280px;
            display: none; border: 1px solid #475569;
        }
        .concept-card {
            position: absolute;
            background: #0F172A;
            color: #FFFFFF;
            border-radius: 12px;
            padding: 18px 22px;
            z-index: 3000;
            max-width: 360px;
            min-width: 260px;
            max-height: 80vh;
            overflow-y: auto;
            border: 1px solid #475569;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            display: none;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            pointer-events: auto;
        }
        .concept-card h3 {
            margin: 0 0 4px 0;
            font-size: 16px;
            color: #FFFFFF;
        }
        .concept-card .card-domain {
            font-size: 11px;
            color: #94A3B8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
            .concept-card .card-definition {
            font-size: 13px;
            line-height: 1.5;
            color: #CBD5E1;
            margin-bottom: 10px;
        }
        .concept-card .card-relationships {
            font-size: 11px;
            color: #94A3B8;
            border-top: 1px solid #334155;
            padding-top: 8px;
            margin-top: 4px;
        }
        .concept-card .card-relationships span {
            display: inline-block;
            margin-right: 8px;
            margin-bottom: 4px;
        }
        .concept-card .card-close {
            position: absolute;
            top: 8px;
            right: 12px;
            cursor: pointer;
            color: #64748B;
            font-size: 16px;
        }
        .concept-card .card-close:hover {
            color: #FFFFFF;
        }
        .reset-btn {
            position: absolute; bottom: 55px; left: 20px;
            z-index: 1000; cursor: pointer;
            padding: 6px 12px; font-size: 11px;
            background: #0F172A; color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 6px; font-family: monospace;
        }
        .reset-btn:hover { background: #1E1B4B; }
    </style>
</head>
<body>
    <div id="cy"></div>
    <div id="info">__INFO_TEXT__</div>
    <div class="node-tooltip" id="nodeTooltip"></div>
    <div class="concept-card" id="conceptCard">
        <span class="card-close" id="cardClose">x</span>
        <h3 id="cardTitle"></h3>
        <div class="card-domain" id="cardDomain"></div>
        <div class="card-definition" id="cardDefinition"></div>
        <div class="card-relationships" id="cardRelationships"></div>
    </div>

    <div id="searchBox">
        <input id="searchInput" type="text" placeholder="Search concepts..." />
    </div>

    <div class="zoom-controls">
        <button class="zoom-btn" title="Zoom in" onclick="cy.zoom(cy.zoom() * 1.3); cy.center()">+</button>
        <button class="zoom-btn" title="Zoom out" onclick="cy.zoom(cy.zoom() * 0.7); cy.center()">−</button>
    </div>

    <button class="reset-btn" onclick="resetView()">Reset View</button>

    <div class="legend-toggle" id="legendToggle">Legend</div>
    <div class="legend-panel collapsed" id="legendPanel">
        <span class="close-legend" id="closeLegend">x</span>
        <h4>Mycelium Legend</h4>
        __LEGEND_ITEMS__
        <hr>
        __EDGE_LEGEND__
        <hr>
        <div class="legend-item"><span>Type 'cadmies' for easter egg</span></div>
    </div>

    <script>
        var elements = { nodes: [__NODES_JSON__], edges: [__EDGES_JSON__] };

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
                name: 'cose', idealEdgeLength: 120,
                nodeRepulsion: 6000, gravity: 0.15,
                numIter: 2000, animate: true, animationDuration: 1500
            }
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

        // Search functionality
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

        // Click node -> show concept card
        cy.on('tap', 'node', function(evt) {
            var node = evt.target;
            var card = document.getElementById('conceptCard');
            document.getElementById('cardTitle').textContent = node.data('label');
            document.getElementById('cardDomain').textContent = node.data('domain').replace(/_/g, ' ');
            document.getElementById('cardDefinition').textContent = node.data('definition') || 'No definition available.';

            // Gather relationships for this node
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
        });

        // Click background -> reset and dismiss card
        cy.on('tap', function(evt) {
            if (evt.target === cy) {
                cy.elements().style('opacity', 1);
                document.getElementById('conceptCard').style.display = 'none';
            }
        });

        // Close card via X button
        document.getElementById('cardClose').addEventListener('click', function() {
            document.getElementById('conceptCard').style.display = 'none';
        });

        function resetView() {
            cy.elements().style('opacity', 1);
            document.getElementById('conceptCard').style.display = 'none';
            cy.fit();
            cy.center();
        }

        // Tooltip on hover
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

        // Interactive legend
        document.querySelectorAll('.legend-item .color-box').forEach(function(box) {
            box.addEventListener('click', function() {
                var domainText = this.nextElementSibling.textContent.trim();
                cy.nodes().forEach(function(n) {
                    if (n.data('domain') === domainText) {
                        n.style({ 'opacity': 1, 'border-width': 3 });
                    } else {
                        n.style({ 'opacity': 0.1, 'border-width': 1 });
                    }
                });
                cy.edges().style('opacity', 0.1);
            });
        });

        // Legend toggle
        document.getElementById('legendToggle').addEventListener('click', function() {
            document.getElementById('legendPanel').classList.toggle('collapsed');
        });
        document.getElementById('closeLegend').addEventListener('click', function() {
            document.getElementById('legendPanel').classList.add('collapsed');
        });

        // Keyboard shortcut: / for search focus
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

        // EASTER EGG
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


def generate_html(nodes, edges, domain_counts):
    """Build complete mycelium_map.html with all data injected.
    Legend only shows canonical domains in defined order — nothing else.
    """
    template = build_html_template()

    # Build nodes JSON
    nodes_json = []
    for n in nodes:
        nodes_json.append(
            '{{ data: {{ id: "{}", label: "{}", definition: "{}", domain: "{}", background_color: "{}" }} }}'.format(
                n["id"].replace('"', '\\"'),
                n["label"].replace('"', '\\"'),
                n.get("definition", "").replace('"', '\\"'),
                n.get("domain", "").replace('"', '\\"'),
                n["color"]
            )
        )
    template = template.replace('__NODES_JSON__', ',\n'.join(nodes_json))

    # Build edges JSON
    edges_json = []
    for e in edges:
        edges_json.append(
            '{{ data: {{ source: "{}", target: "{}", label: "{}" }} }}'.format(
                e["source"].replace('"', '\\"'),
                e["target"].replace('"', '\\"'),
                e["type"]
            )
        )
    template = template.replace('__EDGES_JSON__', ',\n'.join(edges_json) if edges_json else '')

    # Build legend items — CANONICAL DOMAINS ONLY, in defined order
    legend_items = []
    for domain in CANONICAL_DOMAINS:
        if domain in domain_counts:
            color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
            legend_items.append(
                '<div class="legend-item"><div class="color-box" style="background:{}"></div><span>{}</span></div>'.format(
                    color, domain.replace('_', ' ')
                )
            )
    template = template.replace('__LEGEND_ITEMS__', '\n'.join(legend_items))

    # Build edge legend
    edge_legend = '''
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px solid #10B981"></div><span>→ builds_upon</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px solid #F59E0B"></div><span>— related_to</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px dashed #8B5CF6"></div><span>→ specializes</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:3px solid #EF4444"></div><span>→ contradicts</span></div>'''
    template = template.replace('__EDGE_LEGEND__', edge_legend)

    # Build info text
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    info_text = 'CADMIES Mycelium Map | {} nodes | {} edges | {} | Click node for details | / to search | Esc to reset'.format(
        len(nodes), len(edges), timestamp
    )
    template = template.replace('__INFO_TEXT__', info_text)

    return template


def main():
    print("=" * 60)
    print("CADMIES MYCELIUM MAP GENERATOR v2.3.0")
    print(f"Blockstore: {BLOCKS_DIR}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Canonical domains: {len(CANONICAL_DOMAINS)}")
    print("=" * 60)

    nodes, edges, domain_counts = gather_concepts()

    if not nodes:
        print("\nERROR: No concepts loaded. Check blockstore and index at:")
        print(f"  Index: {PROJECT_ROOT}/store/index/human_id_to_cid.json")
        print(f"  Blocks: {BLOCKS_DIR}")
        sys.exit(1)

    html = generate_html(nodes, edges, domain_counts)

    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"\nMap generated: {OUTPUT_FILE}")
    print(f"   {len(nodes)} nodes, {len(edges)} relationships, {len(domain_counts)} domains in data")
    legend_domains = [d for d in CANONICAL_DOMAINS if d in domain_counts]
    print(f"   Legend: {len(legend_domains)} canonical domains shown")
    print(f"   Features: zoom, search, tooltips, concept cards, directional arrows, interactive legend, keyboard shortcuts")
    print(f"   Phase 44: Canonical 15-domain allowlist with upward mapping")

    # Update Tkinter page count
    tkinter_page = PROJECT_ROOT / "cadmies-gui" / "pages" / "tkinter_mycelium_map.py"
    if tkinter_page.exists():
        with open(tkinter_page, "r") as f:
            content = f.read()
        content = content.replace(
            'all 119 concepts', f'all {len(nodes)} concepts'
        ).replace(
            'all 116 concepts', f'all {len(nodes)} concepts'
        )
        with open(tkinter_page, "w") as f:
            f.write(content)
        print(f"   Updated Tkinter page count to {len(nodes)} concepts.")

    # Auto-open in browser if available
    try:
        webbrowser.open(f"file://{OUTPUT_FILE}")
        print(f"   Opened map in browser.")
    except:
        pass


if __name__ == "__main__":
    main()