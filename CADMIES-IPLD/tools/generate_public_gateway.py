#!/usr/bin/env python3
"""
File: generate_public_gateway.py
Tool: CADMIES Public Mycelium Gateway Generator
Version: 3.0.0
System: CADMIES / tools
Status: ACTIVE

Purpose: Generates a single-page public-facing website from the blockstore.
         All concepts rendered as filterable, searchable cards on one page.
         Includes JSON-LD structured data feed and XML sitemap.

         No personal information. No internal tooling references.
         Just the knowledge the mycelium wants to share with the world.

Usage:
    python tools/generate_public_gateway.py

Output:
    ../docs/ — static site served by web server

Version History:
  v3.0.0 (2026-06-24): Project renamed from Hieros to Hierion. Updated all
      URLs and references to reflect new project identity and domain.
  v2.0.1 (2026-05-27): Fixed OUTPUT_DIR from public_concepts_gateway/ to ../docs/.
      Updated SITE_URL. Updated deploy message to reference /docs folder.
  v2.0.0 (2026-05-15): Initial public gateway release with filterable concept cards,
      interactive map, JSON-LD feed, and XML sitemap.
"""

import json, sys
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

OUTPUT_DIR = PROJECT_ROOT.parent / "docs"
SITE_URL = "https://project-hierion.duckdns.org"

# Domain display names for the public site
DOMAIN_DISPLAY = {
    "Physics": "Physics",
    "Philosophy": "Philosophy",
    "Biology": "Biology",
    "Mathematics": "Mathematics",
    "Genomics": "Genomics",
    "Consciousness": "Consciousness Studies",
    "Chemistry": "Chemistry",
    "Ethics": "Ethics",
    "Epistemology": "Epistemology",
    "Complexity_Science": "Complexity Science",
    "Cosmology": "Cosmology",
    "Computer_Science": "Computer Science",
    "Psychology": "Psychology",
    "Spirituality": "Spirituality",
    "Buddhism": "Buddhism",
    "Buddhist_Philosophy": "Buddhist Philosophy",
    "Cognitive_Science": "Cognitive Science",
    "Ecology": "Ecology",
    "Metaphysics": "Metaphysics",
    "MolecularBiology": "Molecular Biology",
    "Neuroscience": "Neuroscience",
    "Sociology": "Sociology",
    "Economics": "Economics",
    "Education": "Education",
    "Political_Science": "Political Science",
    "Medicine": "Medicine",
    "Artificial Intelligence": "Artificial Intelligence",
    "Theoretical Physics": "Theoretical Physics",
    "Emotional_Physics": "Emotional Physics",
}

RELATIONSHIP_LABELS = {
    "builds_upon": "Builds Upon",
    "related_to": "Related To",
    "specializes": "Specializes",
    "contradicts": "Contradicts",
}


def gather_public_concepts():
    """Load all concepts, return only public-facing data."""
    all_cids = load_all_concept_cids()
    concepts = []
    domain_counts = Counter()

    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue

        hid = concept.get('human_id', '')
        title = concept.get('title', hid.replace('_', ' ').title())
        domain = concept.get('domain', 'Unknown')
        definition = concept.get('definition', '')
        rels = concept.get('relationships', {})
        extra = concept.get('extra_fields', {})

        domain_counts[domain] += 1

        concepts.append({
            "human_id": hid,
            "title": title,
            "domain": domain,
            "domain_display": DOMAIN_DISPLAY.get(domain, domain.replace('_', ' ')),
            "definition": definition,
            "poetic_version": extra.get("poetic_version", ""),
            "mantra": extra.get("mantra", ""),
            "insight": extra.get("insight", ""),
            "cid": cid,
            "relationships": {
                "builds_upon": [r for r in rels.get("builds_upon", []) if isinstance(r, str)],
                "related_to": [r for r in rels.get("related_to", []) if isinstance(r, str)],
                "specializes": [r for r in rels.get("specializes", []) if isinstance(r, str)],
                "contradicts": [r for r in rels.get("contradicts", []) if isinstance(r, str)],
            },
        })

    # Build ID-to-title lookup for relationship display
    id_to_title = {c["human_id"]: c["title"] for c in concepts}

    for c in concepts:
        filtered_rels = {}
        for rel_type, targets in c["relationships"].items():
            filtered_rels[rel_type] = [
                {"id": t, "title": id_to_title.get(t, t)}
                for t in targets
                if t in id_to_title
            ]
        c["relationships"] = filtered_rels

    return sorted(concepts, key=lambda c: c["title"]), domain_counts


def escape_html(text):
    """Escape text for safe HTML embedding."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_card(concept):
    """Build a single concept card with expandable detail."""
    hid = concept["human_id"]
    title = escape_html(concept["title"])
    domain = concept["domain"]
    domain_display = escape_html(concept["domain_display"])
    definition = escape_html(concept["definition"])
    domain_class = domain.lower().replace(" ", "-").replace("_", "-")

    # Relationships
    rel_html_parts = []
    for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
        targets = concept["relationships"].get(rel_type, [])
        if targets:
            label = RELATIONSHIP_LABELS.get(rel_type, rel_type)
            tags = "".join(f'<span class="rel-tag rel-{rel_type}">{escape_html(t["title"])}</span>' for t in targets)
            rel_html_parts.append(f'<div class="rel-group"><strong>{label}:</strong> {tags}</div>')
    rel_html = "".join(rel_html_parts) if rel_html_parts else '<p class="no-rels"><em>No relationships recorded yet.</em></p>'

    # Insight / Poetics / Mantra
    extras = []
    if concept.get("insight"):
        extras.append(f'<div class="extra-section"><strong>Core Insight:</strong> {escape_html(concept["insight"])}</div>')
    if concept.get("poetic_version"):
        poetic = escape_html(concept["poetic_version"]).replace("\n", "<br>")
        extras.append(f'<div class="extra-section poetic"><strong>Poetic Version:</strong><blockquote>{poetic}</blockquote></div>')
    if concept.get("mantra"):
        extras.append(f'<div class="extra-section mantra"><strong>Mantra:</strong> <em>"{escape_html(concept["mantra"])}"</em></div>')
    extras_html = "".join(extras)

    return f'''
    <article class="concept-card" data-domain="{domain}" data-search="{title.lower()} {domain_display.lower()} {hid.lower()}">
        <div class="card-header" onclick="this.parentElement.classList.toggle('expanded')">
            <span class="domain-badge domain-{domain_class}">{domain_display}</span>
            <h2>{title}</h2>
            <p class="definition-preview">{definition[:250]}{'...' if len(definition) > 250 else ''}</p>
            <span class="expand-hint">Click to expand ↓</span>
        </div>
        <div class="card-detail">
            <div class="definition-full">
                <p>{definition}</p>
            </div>
            {extras_html}
            <div class="relationships">
                <h3>Relationships</h3>
                {rel_html}
            </div>
            <div class="cid-box">
                <strong>Permanent CID:</strong><br>
                <code>{concept["cid"]}</code>
            </div>
        </div>
    </article>'''


def build_index_page(concepts, domain_counts):
    """Build the single-page public gateway."""
    cards = [build_card(c) for c in concepts]

    # Domain filter buttons
    domains_sorted = sorted(domain_counts.keys())
    domain_filters = []
    for d in domains_sorted:
        count = domain_counts[d]
        display = DOMAIN_DISPLAY.get(d, d.replace('_', ' '))
        domain_filters.append(f'<button class="filter-btn" data-filter="{d}">{display} ({count})</button>')

    total_edges = sum(
        sum(len(targets) for targets in c["relationships"].values())
        for c in concepts
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CADMIES Mycelium — Public Knowledge Graph</title>
    <meta name="description" content="A decentralized knowledge graph of {len(concepts)} interconnected scientific and philosophical concepts. Content-addressed, open-source, forever.">
    <meta name="robots" content="index, follow">
    <link rel="sitemap" type="application/xml" href="sitemap.xml">
    <link rel="alternate" type="application/json" href="concepts.json">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0d1117; color: #c9d1d9; line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}

        /* Header */
        header {{ background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); border-bottom: 1px solid #30363d; padding: 50px 20px 40px; text-align: center; }}
        header h1 {{ font-size: 2.4em; color: #e6edf3; margin-bottom: 8px; }}
        header .subtitle {{ color: #8b949e; font-size: 1.05em; max-width: 600px; margin: 0 auto 20px; }}
        .map-link {{ display: inline-block; margin-top: 12px; padding: 10px 24px; background: #238636; color: #ffffff; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.95em; transition: background 0.2s; }}
        .map-link:hover {{ background: #2ea043; }}

        /* Stats */
        .stats {{ display: flex; gap: 20px; justify-content: center; margin: 24px 0 0; flex-wrap: wrap; }}
        .stat {{ background: #161b22; border: 1px solid #30363d; padding: 14px 24px; border-radius: 8px; }}
        .stat-number {{ font-size: 1.6em; font-weight: bold; color: #e6edf3; }}
        .stat-label {{ font-size: 0.8em; color: #8b949e; }}

        /* Search */
        .search-bar {{ margin: 24px 0; }}
        .search-bar input {{ width: 100%; padding: 12px 18px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 1em; outline: none; }}
        .search-bar input:focus {{ border-color: #58a6ff; }}
        .search-bar input::placeholder {{ color: #484f58; }}

        /* Filters */
        .filters {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; }}
        .filter-btn {{ background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 0.85em; transition: all 0.2s; }}
        .filter-btn:hover {{ background: #30363d; }}
        .filter-btn.active {{ background: #58a6ff; color: #ffffff; border-color: #58a6ff; }}

        /* Cards */
        .concept-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }}
        .concept-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; overflow: hidden; transition: border-color 0.2s; }}
        .concept-card:hover {{ border-color: #58a6ff; }}
        .concept-card.hidden {{ display: none; }}
        .card-header {{ padding: 20px; cursor: pointer; user-select: none; }}
        .card-header h2 {{ font-size: 1.15em; color: #e6edf3; margin-bottom: 6px; }}
        .definition-preview {{ color: #8b949e; font-size: 0.9em; }}
        .expand-hint {{ display: block; font-size: 0.75em; color: #484f58; margin-top: 10px; }}

        /* Expanded detail */
        .card-detail {{ display: none; padding: 0 20px 20px; border-top: 1px solid #30363d; }}
        .concept-card.expanded .card-detail {{ display: block; }}
        .concept-card.expanded .expand-hint {{ display: none; }}
        .definition-full {{ margin: 16px 0; padding: 16px; background: #0d1117; border-radius: 8px; border: 1px solid #21262d; }}
        .definition-full p {{ color: #c9d1d9; font-size: 0.95em; }}

        /* Relationships */
        .relationships {{ margin: 16px 0; }}
        .relationships h3 {{ font-size: 0.9em; color: #8b949e; margin-bottom: 10px; }}
        .rel-group {{ margin: 8px 0; font-size: 0.85em; color: #8b949e; }}
        .rel-group strong {{ color: #c9d1d9; }}
        .rel-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; margin: 2px 4px 2px 0; }}
        .rel-builds_upon {{ background: #1b3a1b; color: #7ee787; }}
        .rel-related_to {{ background: #1b2d4a; color: #79c0ff; }}
        .rel-specializes {{ background: #2d1b3a; color: #d2a8ff; }}
        .rel-contradicts {{ background: #3a1b1b; color: #ff7b72; }}
        .no-rels {{ color: #484f58; font-style: italic; font-size: 0.85em; }}

        /* Extras */
        .extra-section {{ margin: 12px 0; font-size: 0.9em; color: #c9d1d9; }}
        .extra-section strong {{ color: #e6edf3; }}
        .poetic blockquote {{ border-left: 3px solid #58a6ff; padding-left: 14px; color: #8b949e; font-style: italic; margin: 8px 0; }}
        .mantra em {{ color: #d2a8ff; }}

        /* CID box */
        .cid-box {{ margin: 16px 0; padding: 12px; background: #0d1117; border-radius: 6px; font-size: 0.8em; color: #8b949e; }}
        .cid-box code {{ word-break: break-all; color: #484f58; }}

        /* Domain badges */
        .domain-badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.72em; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .domain-physics {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-philosophy {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-biology {{ background: #1b3a1b; color: #7ee787; }}
        .domain-mathematics {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-ethics {{ background: #3a1b2d; color: #ff9bce; }}
        .domain-psychology {{ background: #1b3a2d; color: #7ee787; }}
        .domain-chemistry {{ background: #3a361b; color: #e3b341; }}
        .domain-genomics {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-consciousness {{ background: #21262d; color: #c9d1d9; }}
        .domain-epistemology {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-complexity-science {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-ecology {{ background: #1b3a1b; color: #7ee787; }}
        .domain-spirituality {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-buddhism {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-buddhist-philosophy {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-cosmology {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-computer-science {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-cognitive-science {{ background: #1b3a2d; color: #7ee787; }}
        .domain-neuroscience {{ background: #1b3a2d; color: #7ee787; }}
        .domain-sociology {{ background: #3a1b2d; color: #ff9bce; }}
        .domain-economics {{ background: #3a361b; color: #e3b341; }}
        .domain-education {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-political-science {{ background: #3a1b2d; color: #ff9bce; }}
        .domain-medicine {{ background: #1b3a1b; color: #7ee787; }}
        .domain-artificial-intelligence {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-theoretical-physics {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-metaphysics {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-molecular-biology {{ background: #1b3a1b; color: #7ee787; }}
        .domain-emotional-physics {{ background: #3a1b2d; color: #ff9bce; }}

        /* Footer */
        footer {{ text-align: center; padding: 40px 20px; color: #484f58; font-size: 0.85em; border-top: 1px solid #30363d; margin-top: 40px; }}
        footer a {{ color: #58a6ff; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}

        /* Results count */
        .results-count {{ color: #8b949e; font-size: 0.85em; margin: 8px 0 16px; }}

        @media (max-width: 640px) {{
            .concept-grid {{ grid-template-columns: 1fr; }}
            header h1 {{ font-size: 1.6em; }}
            .stats {{ gap: 10px; }}
            .stat {{ padding: 10px 16px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>CADMIES</h1>
            <p class="subtitle">A decentralized knowledge graph of interconnected scientific and philosophical concepts.<br>Content-addressed. Open-source. Forever.</p>
            <a href="mycelium_map.html" class="map-link">Explore the Interactive Mycelium Map</a>
            <div class="stats">
                <div class="stat"><div class="stat-number">{len(concepts)}</div><div class="stat-label">Concepts</div></div>
                <div class="stat"><div class="stat-number">{len(domain_counts)}</div><div class="stat-label">Domains</div></div>
                <div class="stat"><div class="stat-number">{total_edges}</div><div class="stat-label">Relationships</div></div>
                <div class="stat"><div class="stat-number">CC BY-SA 4.0</div><div class="stat-label">License</div></div>
            </div>
        </div>
    </header>
    <main class="container">
        <div class="search-bar">
            <input type="text" id="search" placeholder="Search concepts..." oninput="filterConcepts()">
        </div>
        <div class="filters" id="filters">
            <button class="filter-btn active" data-filter="all" onclick="setFilter('all', this)">All ({len(concepts)})</button>
            {''.join(domain_filters)}
        </div>
        <div class="results-count" id="resultsCount">Showing {len(concepts)} concepts</div>
        <div class="concept-grid" id="conceptGrid">
            {''.join(cards)}
        </div>
    </main>
    <footer>
        <div class="container">
            <p>CADMIES — Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem</p>
            <p>All concepts licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Each concept has a permanent CID (Content Identifier) — the hash proves nothing was altered.</p>
            <p><a href="sitemap.xml">Sitemap</a> · <a href="concepts.json">JSON Feed</a> · <a href="https://github.com/Project-Hierion/Hierion-CADMIES">GitHub</a></p>
        </div>
    </footer>
    <script>
        let currentFilter = 'all';

        function setFilter(filter, btn) {{
            currentFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterConcepts();
        }}

        function filterConcepts() {{
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const cards = document.querySelectorAll('.concept-card');
            let visible = 0;

            cards.forEach(card => {{
                const domain = card.dataset.domain;
                const searchData = card.dataset.search;
                const matchesFilter = currentFilter === 'all' || domain === currentFilter;
                const matchesSearch = searchData.includes(searchTerm);
                
                if (matchesFilter && matchesSearch) {{
                    card.classList.remove('hidden');
                    visible++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            document.getElementById('resultsCount').textContent = 'Showing ' + visible + ' of {len(concepts)} concepts';
        }}
    </script>
</body>
</html>'''


def build_json_feed(concepts):
    """Build a JSON-LD structured data feed for AI ingestion."""
    items = []
    for c in concepts:
        items.append({
            "@type": "DefinedTerm",
            "name": c["title"],
            "description": c["definition"],
            "termCode": c["cid"],
            "inDefinedTermSet": {
                "@type": "DefinedTermSet",
                "name": "CADMIES Mycelium",
            },
            "url": f"{SITE_URL}/index.html#{c['human_id']}",
        })
    return json.dumps({"@context": "https://schema.org", "@graph": items}, indent=2)


def build_sitemap(concepts):
    """Build XML sitemap for search engines."""
    urls = [f'<url><loc>{SITE_URL}/index.html</loc></url>']
    for c in concepts:
        urls.append(f'<url><loc>{SITE_URL}/index.html#{c["human_id"]}</loc></url>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''


def main():
    print("=" * 60)
    print("CADMIES PUBLIC MYCELIUM GATEWAY GENERATOR v2.0.1")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    concepts, domain_counts = gather_public_concepts()
    total_edges = sum(
        sum(len(targets) for targets in c["relationships"].values())
        for c in concepts
    )
    print(f"\nLoaded {len(concepts)} concepts across {len(domain_counts)} domains with {total_edges} edges")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build single-page index
    print("Generating index.html (single-page gateway)...")
    index_html = build_index_page(concepts, domain_counts)
    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(index_html)

    # Build JSON-LD feed
    print("Generating concepts.json (structured data)...")
    json_feed = build_json_feed(concepts)
    with open(OUTPUT_DIR / "concepts.json", "w") as f:
        f.write(json_feed)

    # Build sitemap
    print("Generating sitemap.xml...")
    sitemap = build_sitemap(concepts)
    with open(OUTPUT_DIR / "sitemap.xml", "w") as f:
        f.write(sitemap)

    # Ensure .nojekyll
    nojekyll = OUTPUT_DIR / ".nojekyll"
    if not nojekyll.exists():
        nojekyll.touch()

    print(f"\nPublic gateway generated: {OUTPUT_DIR}")
    print(f"   index.html — single-page app with {len(concepts)} concept cards")
    print(f"   concepts.json — JSON-LD structured data feed")
    print(f"   sitemap.xml — search engine sitemap")
    print(f"   .nojekyll — bypass Jekyll processing")
    print(f"\nDeploy: push to GitHub, Pages serves from /docs folder")


if __name__ == "__main__":
    main()
