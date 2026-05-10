#!/usr/bin/env python3
"""
File: generate_mycelium_map.py
Tool: CADMIES Mycelium Map Generator
Version: 1.0.0
System: CADMIES-IPLD / tools
Status: ACTIVE

Purpose: Dynamically generates mycelium_map.html from the live blockstore.
         Reads every concept via llm_mycelium_reader.load_concept(),
         extracts domains and all four relationship types, builds a
         Cytoscape.js force-directed graph with DeepSeek-themed colors,
         and writes the complete HTML to the project root.

         Replaces the old static hand-curated map that went stale after
         the NiceGUI→Tkinter migration.

Usage:
    python tools/generate_mycelium_map.py

Output:
    mycelium_map.html (project root) — open in any modern browser

Design:
    - White background, DeepSeek palette for nodes/edges/legend
    - Node text auto-sizes to fit within circles, scales with zoom
    - Legend dynamically built from domains present in the data
    - Easter egg preserved: type "cadmies"

Dependencies: llm_mycelium_reader, paths
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from llm_mycelium_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

# === CONFIG ===
OUTPUT_FILE = PROJECT_ROOT / "mycelium_map.html"

# DeepSeek-themed domain → node color mapping
# Extended palette for graph legibility while staying in the DeepSeek family
DOMAIN_COLORS = {
    "Physics":                "#4F46E5",  # Indigo — fundamental forces
    "Philosophy":             "#6366F1",  # Accent — bridging domains
    "Biology":                "#10B981",  # Success Green — living systems
    "Mathematics":            "#1E1B4B",  # Navy — pure structure
    "Genomics":               "#8B5CF6",  # Violet — information encoding
    "Consciousness":          "#0F172A",  # Near-black — the hard problem
    "Chemistry":              "#F59E0B",  # Amber — reactions, bonds
    "Ethics":                 "#EC4899",  # Pink — moral weight
    "Epistemology":           "#6366F1",  # → Philosophy (Accent)
    "Complexity_Science":     "#1E1B4B",  # → Mathematics (Navy)
    "Cosmology":              "#4F46E5",  # → Physics (Indigo)
    "Computer_Science":       "#3B82F6",  # Blue — computation
    "Psychology":             "#14B8A6",  # Teal — mind
    "Spirituality":           "#A78BFA",  # Soft violet
    "Buddhism":               "#A78BFA",  # → Spirituality
    "Neuroscience":           "#14B8A6",  # → Psychology
    "Sociology":              "#EC4899",  # → Ethics (social)
    "Economics":              "#F59E0B",  # → Chemistry (dynamic systems)
    "Education":              "#3B82F6",  # → CS (knowledge transfer)
    "Political_Science":      "#EC4899",  # → Ethics
    "Medicine":               "#10B981",  # → Biology
}
DEFAULT_COLOR = {
    "#64748B"  # Slate — uncategorized / unknown domain
        "Buddhist_Philosophy":     "#A78BFA",  # → Spirituality
    "Cognitive_Science":       "#14B8A6",  # → Psychology
    "Ecology":                 "#10B981",  # → Biology
    "Metaphysics":             "#6366F1",  # → Philosophy
    "MolecularBiology":        "#10B981",  # → Biology
    "ConsciousnessStudies":    "#0F172A",  # → Consciousness
    "Climate Ethics":          "#EC4899",  # → Ethics
    "Philosophy of Art":       "#6366F1",  # → Philosophy
    "Biology, Philosophy":     "#10B981",  # → Biology (primary)
    "Ethics, Social Science":  "#EC4899",  # → Ethics
    "Ethics & Philosophy of Mind": "#EC4899",  # → Ethics
    "Metaphysics & Philosophy of Mind": "#6366F1",  # → Philosophy
    "Artificial Intelligence": "#3B82F6",  # → CS
    "Theoretical Physics":     "#4F46E5",  # → Physics
    "Philosophy of Science & Spirituality": "#6366F1",  # → Philosophy
    "Philosophy of Daily Life": "#6366F1",  # → Philosophy
    "Philosophy of Technology": "#6366F1",  # → Philosophy
}

# Relationship type → edge color
EDGE_COLORS = {
    "builds_upon":  "#10B981",  # Green — foundational
    "related_to":   "#F59E0B",  # Amber — associative
    "specializes":  "#8B5CF6",  # Violet — refinement
    "contradicts":  "#EF4444",  # Red — opposition
}

# Legacy hand-curated edges from the original NiceGUI map
# These supplement blockstore relationships until auto-edge generation is built
LEGACY_EDGES_FILE = TOOLS_DIR / "legacy_edges.json"

# DeepSeek theme colors for UI elements
DEEPSEEK_INDIGO = "#4F46E5"
DEEPSEEK_NAVY = "#1E1B4B"
DEEPSEEK_ACCENT = "#6366F1"
DEEPSEEK_SURFACE = "#F8FAFC"
DEEPSEEK_TEXT = "#0F172A"
DEEPSEEK_TEXT_LIGHT = "#475569"
DEEPSEEK_SUBTLE = "#E2E8F0"
WHITE = "#FFFFFF"


# ============================================================================
# DATA GATHERING
# ============================================================================

def load_legacy_edges():
    """Load legacy hand-curated edges from JSON file."""
    if not LEGACY_EDGES_FILE.exists():
        print("  No legacy edges file found — using blockstore edges only.")
        return []
    with open(LEGACY_EDGES_FILE, "r") as f:
        legacy = json.load(f)
    print(f"  Loaded {len(legacy)} legacy edges from {LEGACY_EDGES_FILE.name}")
    return legacy


def gather_concepts():
    """Load all concepts from blockstore, extract graph data, merge with legacy edges."""
    all_cids = load_all_concept_cids()
    print(f"Loading {len(all_cids)} concepts from blockstore...")

    nodes = []
    node_ids = set()
    skipped = 0
    domain_counts = Counter()

    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            skipped += 1
            continue

        human_id = concept.get('human_id', '')
        title = concept.get('title', human_id.replace('_', ' ').title())
        domain = concept.get('domain', 'Unknown')
        domain_counts[domain] += 1

        color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
        nodes.append({
            "id": human_id,
            "label": title,
            "color": color,
            "domain": domain,
        })
        node_ids.add(human_id)

    # Gather edges from blockstore relationships
    blockstore_edges = []
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        human_id = concept.get('human_id', '')
        rels = concept.get('relationships', {})
        for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
            targets = rels.get(rel_type, [])
            if not targets:
                continue
            for target in targets:
                if not isinstance(target, str):
                    continue
                blockstore_edges.append({
                    "source": human_id,
                    "target": target,
                    "type": rel_type,
                })

    # Load legacy edges
    legacy_edges = load_legacy_edges()

    # Merge: use dict keyed by (source, target, type) — legacy wins on overlap
    merged = {}
    for e in blockstore_edges:
        key = (e["source"], e["target"], e["type"])
        merged[key] = e
    legacy_count = 0
    for e in legacy_edges:
        key = (e["source"], e["target"], e["type"])
        merged[key] = e

    all_edges = list(merged.values())

    # Filter to only edges where both nodes exist
    valid_edges = [e for e in all_edges if e["source"] in node_ids and e["target"] in node_ids]
    orphan_edges = len(all_edges) - len(valid_edges)
    if orphan_edges:
        print(f"  Filtered {orphan_edges} orphan edge(s) (target/source concept not in blockstore)")

    bs_edge_count = len(blockstore_edges)
    legacy_edge_count = sum(1 for e in valid_edges if (e["source"], e["target"], e["type"]) in {(le["source"], le["target"], le["type"]) for le in legacy_edges})

    print(f"  {len(nodes)} nodes, {len(valid_edges)} edges ({bs_edge_count} blockstore, {legacy_edge_count} legacy), {skipped} skipped")
    print(f"  Domains: {dict(domain_counts.most_common())}")
    return nodes, valid_edges, domain_counts

    # Filter edges to only those where both source and target exist as nodes
    valid_edges = [e for e in edges if e["source"] in node_ids and e["target"] in node_ids]
    orphan_edges = len(edges) - len(valid_edges)
    if orphan_edges:
        print(f"  Filtered {orphan_edges} orphan edge(s) (target concept not in blockstore)")

    print(f"  {len(nodes)} nodes, {len(valid_edges)} edges, {skipped} skipped")
    print(f"  Domains: {dict(domain_counts.most_common())}")
    return nodes, valid_edges, domain_counts


# ============================================================================
# HTML GENERATION
# ============================================================================

def generate_html(nodes, edges, domain_counts):
    """Build the complete mycelium_map.html string."""

    # Build nodes JSON
    nodes_json_lines = []
    for n in nodes:
        escaped_label = n["label"].replace('"', '\\"')
        escaped_id = n["id"].replace('"', '\\"')
        nodes_json_lines.append(
            f'                {{ data: {{ id: "{escaped_id}", label: "{escaped_label}" }}, style: {{ "background-color": "{n["color"]}" }} }}'
        )
    nodes_json = ",\n".join(nodes_json_lines)

    # Build edges JSON
    edges_json_lines = []
    for e in edges:
        escaped_source = e["source"].replace('"', '\\"')
        escaped_target = e["target"].replace('"', '\\"')
        edges_json_lines.append(
            f'                {{ data: {{ source: "{escaped_source}", target: "{escaped_target}", label: "{e["type"]}" }} }}'
        )
    edges_json = ",\n".join(edges_json_lines)

    # Build legend items dynamically from domains actually present
    legend_items = []
    # Order: show core domains first, then alphabetical for the rest
    core_order = ["Physics", "Philosophy", "Biology", "Mathematics", "Consciousness",
                  "Chemistry", "Ethics", "Genomics", "Computer_Science", "Psychology",
                  "Spirituality", "Buddhism", "Complexity_Science", "Cosmology",
                  "Epistemology", "Neuroscience", "Sociology", "Economics", "Education",
                  "Political_Science", "Medicine"]
    shown_domains = set()
    for domain in core_order:
        if domain in domain_counts and domain not in shown_domains:
            color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
            label = domain.replace("_", " ")
            legend_items.append(f'        <div class="legend-item"><div class="color-box" style="background: {color};"></div><span>{label}</span></div>')
            shown_domains.add(domain)
    # Any remaining domains not in core_order
    for domain in sorted(domain_counts.keys()):
        if domain not in shown_domains:
            color = DOMAIN_COLORS.get(domain, DEFAULT_COLOR)
            label = domain.replace("_", " ")
            legend_items.append(f'        <div class="legend-item"><div class="color-box" style="background: {color};"></div><span>{label}</span></div>')
            shown_domains.add(domain)
    legend_html = "\n".join(legend_items)

    # Generate timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Edge legend — static, matches EDGE_COLORS
    edge_legend = f'''
        <div class="legend-item"><div class="line-sample" style="border-bottom: 2px solid {EDGE_COLORS["builds_upon"]};"></div><span>builds_upon</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom: 2px solid {EDGE_COLORS["related_to"]};"></div><span>related_to</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom: 2px dashed {EDGE_COLORS["specializes"]};"></div><span>specializes</span></div>
        <div class="legend-item"><div class="line-sample" style="border-bottom: 3px solid {EDGE_COLORS["contradicts"]};"></div><span>contradicts</span></div>'''

    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>CADMIES Mycelium Map</title>
    <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: {WHITE};
        }}
        #cy {{
            width: 100vw;
            height: 100vh;
            position: absolute;
            top: 0;
            left: 0;
        }}
        #info {{
            position: absolute;
            bottom: 12px;
            left: 12px;
            background: {DEEPSEEK_TEXT};
            color: {WHITE};
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 11px;
            z-index: 100;
            pointer-events: none;
            font-family: monospace;
        }}

        .legend-toggle {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: {DEEPSEEK_TEXT};
            color: {WHITE};
            backdrop-filter: blur(8px);
            border-radius: 30px;
            padding: 10px 16px;
            font-family: monospace;
            font-size: 14px;
            cursor: pointer;
            z-index: 1000;
            border: 1px solid {DEEPSEEK_SUBTLE};
            transition: all 0.2s ease;
        }}

        .legend-toggle:hover {{
            background: {DEEPSEEK_NAVY};
            transform: scale(1.02);
        }}

        .legend-panel {{
            position: absolute;
            top: 70px;
            right: 20px;
            background: {DEEPSEEK_TEXT};
            color: {WHITE};
            backdrop-filter: blur(8px);
            border-radius: 12px;
            padding: 15px;
            font-family: monospace;
            font-size: 11px;
            border: 1px solid {DEEPSEEK_SUBTLE};
            z-index: 999;
            min-width: 180px;
            transition: all 0.3s ease;
            opacity: 1;
            pointer-events: auto;
        }}

        .legend-panel.collapsed {{
            opacity: 0;
            pointer-events: none;
            transform: translateX(20px);
        }}

        .legend-panel h4 {{
            margin: 0 0 10px 0;
            color: {WHITE};
            font-size: 13px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 5px;
        }}

        .color-box {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        .line-sample {{
            width: 20px;
            height: 2px;
            flex-shrink: 0;
        }}

        hr {{
            margin: 8px 0;
            border-color: {DEEPSEEK_TEXT_LIGHT};
            border-width: 0.5px;
        }}

        .close-legend {{
            float: right;
            cursor: pointer;
            color: {DEEPSEEK_TEXT_LIGHT};
            margin-left: 10px;
            font-size: 14px;
        }}

        .close-legend:hover {{
            color: {WHITE};
        }}
    </style>
</head>
<body>
    <div id="cy"></div>
    <div id="info">CADMIES Mycelium Map | {len(nodes)} nodes | {len(edges)} relationships | {timestamp} | Click node for concept</div>

    <div class="legend-toggle" id="legendToggle">📖 Legend</div>

    <div class="legend-panel collapsed" id="legendPanel">
        <span class="close-legend" id="closeLegend">✕</span>
        <h4>Mycelium Legend</h4>
{legend_html}
        <hr>
{edge_legend}
        <hr>
        <div class="legend-item"><span>💡 Tip: Type 'cadmies'</span></div>
        <div class="legend-item"><span>for an easter egg</span></div>
    </div>

    <script>
        var elements = {{
            nodes: [
{nodes_json}
            ],
            edges: [
{edges_json}
            ]
        }};

        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                {{
                    selector: 'node',
                    style: {{
                        'label': 'data(label)',
                        'background-color': 'data(background-color)',
                        'width': 50,
                        'height': 50,
                        'font-size': '10px',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'color': '{WHITE}',
                        'text-wrap': 'wrap',
                        'text-max-width': '44px',
                        'text-overflow-wrap': 'anywhere',
                        'border-width': 2,
                        'border-color': '{DEEPSEEK_SUBTLE}'
                    }}
                }},
                {{
                    selector: 'edge',
                    style: {{
                        'width': 2,
                        'line-color': '{DEEPSEEK_TEXT_LIGHT}',
                        'curve-style': 'bezier',
                        'label': 'data(label)',
                        'font-size': '8px',
                        'text-rotation': 'autorotate',
                        'color': '{DEEPSEEK_TEXT_LIGHT}',
                        'text-background-color': '{WHITE}',
                        'text-background-opacity': 0.8,
                        'text-background-padding': '2px'
                    }}
                }},
                {{ selector: 'edge[label = "builds_upon"]', style: {{ 'line-color': '{EDGE_COLORS["builds_upon"]}', 'width': 2 }} }},
                {{ selector: 'edge[label = "related_to"]', style: {{ 'line-color': '{EDGE_COLORS["related_to"]}', 'width': 2 }} }},
                {{ selector: 'edge[label = "specializes"]', style: {{ 'line-color': '{EDGE_COLORS["specializes"]}', 'line-style': 'dashed', 'width': 2 }} }},
                {{ selector: 'edge[label = "contradicts"]', style: {{ 'line-color': '{EDGE_COLORS["contradicts"]}', 'width': 3 }} }}
            ],
            layout: {{
                name: 'cose',
                idealEdgeLength: 120,
                nodeRepulsion: 6000,
                gravity: 0.15,
                numIter: 2000,
                animate: true,
                animationDuration: 1500
            }}
        }});

        // Auto-size node text on zoom — expand circles so labels always fit
        cy.on('zoom', function() {{
            var zoom = cy.zoom();
            var baseSize = Math.max(36, 50 / Math.sqrt(zoom));
            cy.style()
                .selector('node')
                .style({{
                    'width': baseSize,
                    'height': baseSize,
                    'font-size': Math.max(7, baseSize * 0.2) + 'px',
                    'text-max-width': (baseSize * 0.88) + 'px'
                }})
                .update();
        }});

        cy.on('tap', 'node', function(evt) {{
            var node = evt.target;
            alert('Concept: ' + node.data('label') + '\\nID: ' + node.id());
        }});

        // Legend toggle
        var legendToggle = document.getElementById('legendToggle');
        var legendPanel = document.getElementById('legendPanel');
        var closeLegend = document.getElementById('closeLegend');

        legendToggle.addEventListener('click', function() {{
            legendPanel.classList.toggle('collapsed');
        }});

        closeLegend.addEventListener('click', function() {{
            legendPanel.classList.add('collapsed');
        }});

        // EASTER EGG: Type "cadmies"
        var keyBuffer = [];
        document.addEventListener('keydown', function(e) {{
            if (e.key.length === 1 && /[a-zA-Z]/.test(e.key)) {{
                keyBuffer.push(e.key.toLowerCase());
                if (keyBuffer.length > 7) keyBuffer.shift();

                if (keyBuffer.join('') === 'cadmies') {{
                    cy.style()
                        .selector('node')
                        .style({{
                            'background-color': '#ffd700',
                            'border-color': '#ff6600',
                            'border-width': '3px',
                            'shape': 'ellipse'
                        }})
                        .update();

                    var msg = document.createElement('div');
                    msg.innerHTML = '<div style="text-align: center;"><div style="font-size: 20px; font-weight: bold;">🎸 LET THE GOOD TIMES ROLL WITH CADMIES! 🎸</div><div style="font-size: 12px; font-style: italic; color: #ffd700; margin-top: 5px;">💿 homage to The Cars</div></div>';
                    msg.style.position = 'fixed';
                    msg.style.bottom = '50px';
                    msg.style.left = '50%';
                    msg.style.transform = 'translateX(-50%)';
                    msg.style.background = 'linear-gradient(90deg, #ff6600, #ffd700)';
                    msg.style.color = 'black';
                    msg.style.padding = '12px 24px';
                    msg.style.borderRadius = '50px';
                    msg.style.zIndex = '9999';
                    msg.style.fontFamily = 'monospace';
                    msg.style.boxShadow = '0 0 20px rgba(255,102,0,0.5)';
                    msg.style.animation = 'fadeInOut 3s ease-in-out';
                    document.body.appendChild(msg);

                    var style = document.createElement('style');
                    style.textContent = '@keyframes fadeInOut {{ 0% {{ opacity: 0; transform: translateX(-50%) scale(0.8); }} 20% {{ opacity: 1; transform: translateX(-50%) scale(1); }} 80% {{ opacity: 1; transform: translateX(-50%) scale(1); }} 100% {{ opacity: 0; transform: translateX(-50%) scale(0.8); }} }}';
                    document.head.appendChild(style);

                    setTimeout(function() {{ msg.remove(); }}, 4000);
                    keyBuffer = [];
                }}
            }}
        }});
    </script>
</body>
</html>'''
    return html


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("CADMIES MYCELIUM MAP GENERATOR v1.0.0")
    print(f"Blockstore: {BLOCKS_DIR}")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)

    nodes, edges, domain_counts = gather_concepts()

    if not nodes:
        print("\nERROR: No concepts loaded. Check blockstore and index.")
        sys.exit(1)

    html = generate_html(nodes, edges, domain_counts)

    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    print(f"\n✅ Map generated: {OUTPUT_FILE}")
    print(f"   {len(nodes)} nodes, {len(edges)} relationships")
    print(f"   {len(domain_counts)} domains represented")
    print(f"   Open in Firefox to view.")

    # Also update the Tkinter page's hardcoded count (cosmetic)
    tkinter_page = PROJECT_ROOT / "cadmies-gui" / "pages" / "tkinter_mycelium_map.py"
    if tkinter_page.exists():
        with open(tkinter_page, "r") as f:
            content = f.read()
        # Update the count shown in the info text
        import re
        content = re.sub(r'all \d+ concepts', f'all {len(nodes)} concepts', content)
        with open(tkinter_page, "w") as f:
            f.write(content)
        print(f"   Updated Tkinter page count to {len(nodes)} concepts.")


if __name__ == "__main__":
    main()