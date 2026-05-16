#!/usr/bin/env python3
"""
File: generate_mycelium_map.py
Tool: CADMIES Mycelium Map Generator
Version: 2.0.0
System: CADMIES-IPLD / tools
Status: ACTIVE — Enhanced with zoom controls, search, tooltips, interactive legend

Purpose: Dynamically generates mycelium_map.html from the live blockstore.
         Enhanced features: zoom buttons, concept search, hover tooltips,
         click-to-highlight connections, interactive domain legend,
         keyboard shortcuts, responsive design.

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

# DeepSeek-themed domain colors
DOMAIN_COLORS = {
    "Physics": "#4F46E5", "Philosophy": "#6366F1", "Biology": "#10B981",
    "Mathematics": "#1E1B4B", "Genomics": "#8B5CF6", "Consciousness": "#0F172A",
    "Chemistry": "#F59E0B", "Ethics": "#EC4899", "Epistemology": "#6366F1",
    "Complexity_Science": "#1E1B4B", "Cosmology": "#4F46E5",
    "Computer_Science": "#3B82F6", "Psychology": "#14B8A6",
    "Spirituality": "#A78BFA", "Buddhism": "#A78BFA",
    "Neuroscience": "#14B8A6", "Sociology": "#EC4899",
    "Economics": "#F59E0B", "Education": "#3B82F6",
    "Political_Science": "#EC4899", "Medicine": "#10B981",
    "Buddhist_Philosophy": "#A78BFA", "Cognitive_Science": "#14B8A6",
    "Ecology": "#10B981", "Metaphysics": "#6366F1",
    "MolecularBiology": "#10B981", "ConsciousnessStudies": "#0F172A",
    "Climate Ethics": "#EC4899", "Philosophy of Art": "#6366F1",
    "Biology, Philosophy": "#10B981", "Ethics, Social Science": "#EC4899",
    "Ethics & Philosophy of Mind": "#EC4899",
    "Metaphysics & Philosophy of Mind": "#6366F1",
    "Artificial Intelligence": "#3B82F6", "Theoretical Physics": "#4F46E5",
    "Philosophy of Science & Spirituality": "#6366F1",
    "Philosophy of Daily Life": "#6366F1", "Philosophy of Technology": "#6366F1",
    "Psychology, Physics": "#14B8A6",
}
DEFAULT_COLOR = "#64748B"

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
    """Load all concepts, extract graph data, merge with legacy edges."""
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
        domain = concept.get('domain', 'Unknown')
        definition = concept.get('definition', '')[:150]
        domain_counts[domain] += 1
        color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
        nodes.append({
            "id": hid, "label": title, "color": color,
            "domain": domain, "definition": definition,
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
                    'width': 45, 'height': 45, 'font-size': '10px',
                    'text-valign': 'center', 'text-halign': 'center',
                    'color': '#FFFFFF', 'text-wrap': 'wrap',
                    'text-max-width': '40px', 'text-overflow-wrap': 'anywhere',
                    'border-width': 2, 'border-color': '#E2E8F0'
                }},
                { selector: 'edge', style: {
                    'width': 2, 'line-color': '#475569',
                    'curve-style': 'bezier', 'label': 'data(label)',
                    'font-size': '8px', 'text-rotation': 'autorotate',
                    'color': '#475569', 'text-background-color': '#FFFFFF',
                    'text-background-opacity': 0.8, 'text-background-padding': '2px'
                }},
                { selector: 'edge[label = "builds_upon"]', style: { 'line-color': '#10B981', 'width': 2 }},
                { selector: 'edge[label = "related_to"]', style: { 'line-color': '#F59E0B', 'width': 2 }},
                { selector: 'edge[label = "specializes"]', style: { 'line-color': '#8B5CF6', 'line-style': 'dashed', 'width': 2 }},
                { selector: 'edge[label = "contradicts"]', style: { 'line-color': '#EF4444', 'width': 3 }}
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
            var base = Math.max(32, 45 / Math.sqrt(zoom));
            cy.style().selector('node').style({
                'width': base, 'height': base,
                'font-size': Math.max(7, base * 0.2) + 'px',
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

        // Click node -> highlight connections
        cy.on('tap', 'node', function(evt) {
            var node = evt.target;
            alert('Concept: ' + node.data('label') + ' (ID: ' + node.id() + ')');
            cy.elements().style('opacity', 0.15);
            node.style('opacity', 1);
            node.neighborhood().style('opacity', 1);
        });

        // Click background -> reset
        cy.on('tap', function(evt) {
            if (evt.target === cy) { cy.elements().style('opacity', 1); }
        });

        function resetView() {
            cy.elements().style('opacity', 1);
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
    """Build complete mycelium_map.html with all data injected."""
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

    # Build legend items
    core_order = ["Physics", "Philosophy", "Biology", "Mathematics", "Consciousness",
                  "Chemistry", "Ethics", "Genomics", "Computer_Science", "Psychology",
                  "Spirituality", "Buddhism", "Complexity_Science", "Cosmology",
                  "Epistemology", "Neuroscience", "Sociology", "Economics", "Education",
                  "Political_Science", "Medicine"]
    shown = set()
    legend_items = []
    for domain in core_order:
        if domain in domain_counts and domain not in shown:
            color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
            legend_items.append(
                '<div class="legend-item"><div class="color-box" style="background:{}"></div><span>{}</span></div>'.format(
                    color, domain.replace('_', ' ')
                )
            )
            shown.add(domain)
    for domain in sorted(domain_counts.keys()):
        if domain not in shown:
            color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
            legend_items.append(
                '<div class="legend-item"><div class="color-box" style="background:{}"></div><span>{}</span></div>'.format(
                    color, domain.replace('_', ' ')
                )
            )
            shown.add(domain)
    template = template.replace('__LEGEND_ITEMS__', '\n'.join(legend_items))

    # Build edge legend
    edge_legend = '''
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px solid #10B981"></div><span>builds_upon</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px solid #F59E0B"></div><span>related_to</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:2px dashed #8B5CF6"></div><span>specializes</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom:3px solid #EF4444"></div><span>contradicts</span></div>'''
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
    print("CADMIES MYCELIUM MAP GENERATOR v2.0.0")
    print(f"Blockstore: {BLOCKS_DIR}")
    print(f"Output: {OUTPUT_FILE}")
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
    print(f"   {len(nodes)} nodes, {len(edges)} relationships, {len(domain_counts)} domains")
    print(f"   Features: zoom buttons, search, tooltips, click-to-highlight, interactive legend, keyboard shortcuts")
    
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