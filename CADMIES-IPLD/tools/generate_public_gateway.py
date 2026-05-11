#!/usr/bin/env python3
"""
File: generate_public_gateway.py
Tool: CADMIES Public Mycelium Gateway Generator
Version: 1.0.0
System: CADMIES-IPLD / tools
Status: ACTIVE

Purpose: Generates a static public-facing website from the blockstore.
         Each concept gets its own HTML page with title, definition,
         domain, relationships, and CID. Includes index page, JSON-LD
         structured data, and sitemap for search engine discovery.

         No personal information. No internal tooling references.
         Just the knowledge the mycelium wants to share with the world.

Usage:
    python tools/generate_public_gateway.py

Output:
    docs/public/ — static site ready for GitHub Pages deployment
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

from llm_mycelium_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

OUTPUT_DIR = PROJECT_ROOT / "docs" / "public"

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
        
        # Only include relationships that reference real concepts (we'll filter after)
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
    
    # Filter relationships to only include valid cross-references
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


def build_index_page(concepts, domain_counts):
    """Build the main index.html page listing all concepts."""
    concept_cards = []
    for c in concepts:
        domain_class = c["domain"].lower().replace(" ", "-").replace("_", "-")
        concept_cards.append(f'''\
        <article class="concept-card" data-domain="{c['domain']}">
            <span class="domain-badge domain-{domain_class}">{c['domain_display']}</span>
            <h2><a href="{c['human_id']}.html">{c['title']}</a></h2>
            <p>{c['definition'][:200]}{'...' if len(c['definition']) > 200 else ''}</p>
            <div class="card-meta">
                <span>CID: <code>{c['cid'][:16]}...</code></span>
            </div>
        </article>''')
    
    # Domain filter buttons
    domains_sorted = sorted(domain_counts.keys())
    domain_filters = []
    for d in domains_sorted:
        count = domain_counts[d]
        display = DOMAIN_DISPLAY.get(d, d.replace('_', ' '))
        domain_class = d.lower().replace(" ", "-").replace("_", "-")
        domain_filters.append(f'<button class="filter-btn" data-filter="{d}">{display} ({count})</button>')
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CADMIES Mycelium — Public Knowledge Graph</title>
    <meta name="description" content="A decentralized knowledge graph of {len(concepts)} interconnected scientific and philosophical concepts. Content-addressed, open-source, forever.">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #F8FAFC; color: #0F172A; line-height: 1.6; }}
        .container {{ max-width: 960px; margin: 0 auto; padding: 20px; }}
        header {{ background: #0F172A; color: #FFFFFF; padding: 40px 20px; text-align: center; }}
        header h1 {{ font-size: 2em; margin-bottom: 8px; }}
        header p {{ color: #94A3B8; font-size: 0.95em; }}
        .stats {{ display: flex; gap: 20px; justify-content: center; margin: 20px 0; flex-wrap: wrap; }}
        .stat {{ background: #1E1B4B; padding: 12px 20px; border-radius: 8px; }}
        .stat-number {{ font-size: 1.5em; font-weight: bold; }}
        .stat-label {{ font-size: 0.8em; color: #94A3B8; }}
        .filters {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0; }}
        .filter-btn {{ background: #E2E8F0; border: none; padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 0.85em; transition: background 0.2s; }}
        .filter-btn:hover, .filter-btn.active {{ background: #4F46E5; color: #FFFFFF; }}
        .filter-btn.active {{ background: #4F46E5; color: #FFFFFF; }}
        .concept-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
        .concept-card {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; transition: box-shadow 0.2s; }}
        .concept-card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .concept-card.hidden {{ display: none; }}
        .concept-card h2 {{ font-size: 1.1em; margin-bottom: 8px; }}
        .concept-card h2 a {{ color: #0F172A; text-decoration: none; }}
        .concept-card h2 a:hover {{ color: #4F46E5; }}
        .concept-card p {{ color: #475569; font-size: 0.9em; margin-bottom: 10px; }}
        .domain-badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75em; font-weight: 600; margin-bottom: 8px; }}
        .domain-physics {{ background: #EEF2FF; color: #4F46E5; }}
        .domain-philosophy {{ background: #F0EFFF; color: #6366F1; }}
        .domain-biology {{ background: #ECFDF5; color: #10B981; }}
        .domain-mathematics {{ background: #1E1B4B; color: #C7D2FE; }}
        .domain-ethics {{ background: #FDF2F8; color: #EC4899; }}
        .domain-psychology {{ background: #F0FDFA; color: #14B8A6; }}
        .domain-chemistry {{ background: #FFFBEB; color: #F59E0B; }}
        .domain-genomics {{ background: #F5F3FF; color: #8B5CF6; }}
        .domain-consciousness {{ background: #F1F5F9; color: #0F172A; }}
        .domain-epistemology {{ background: #F0EFFF; color: #6366F1; }}
        .domain-complexity-science {{ background: #1E1B4B; color: #C7D2FE; }}
        .domain-ecology {{ background: #ECFDF5; color: #10B981; }}
        .domain-spirituality {{ background: #F5F3FF; color: #A78BFA; }}
        .domain-buddhism {{ background: #F5F3FF; color: #A78BFA; }}
        .domain-buddhist-philosophy {{ background: #F5F3FF; color: #A78BFA; }}
        .domain-cosmology {{ background: #EEF2FF; color: #4F46E5; }}
        .domain-computer-science {{ background: #EFF6FF; color: #3B82F6; }}
        .domain-cognitive-science {{ background: #F0FDFA; color: #14B8A6; }}
        .domain-neuroscience {{ background: #F0FDFA; color: #14B8A6; }}
        .domain-sociology {{ background: #FDF2F8; color: #EC4899; }}
        .domain-economics {{ background: #FFFBEB; color: #F59E0B; }}
        .domain-education {{ background: #EFF6FF; color: #3B82F6; }}
        .domain-political-science {{ background: #FDF2F8; color: #EC4899; }}
        .domain-medicine {{ background: #ECFDF5; color: #10B981; }}
        .domain-artificial-intelligence {{ background: #EFF6FF; color: #3B82F6; }}
        .domain-theoretical-physics {{ background: #EEF2FF; color: #4F46E5; }}
        .domain-metaphysics {{ background: #F0EFFF; color: #6366F1; }}
        .domain-molecular-biology {{ background: #ECFDF5; color: #10B981; }}
        .card-meta {{ font-size: 0.75em; color: #94A3B8; }}
        .card-meta code {{ background: #F1F5F9; padding: 1px 5px; border-radius: 4px; }}
        footer {{ text-align: center; padding: 40px 20px; color: #94A3B8; font-size: 0.85em; }}
        footer a {{ color: #4F46E5; }}
        @media (max-width: 640px) {{
            .concept-grid {{ grid-template-columns: 1fr; }}
            header h1 {{ font-size: 1.5em; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🌱 CADMIES Mycelium</h1>
            <p>A decentralized knowledge graph of interconnected scientific and philosophical concepts.<br>Content-addressed. Open-source. Forever.</p>
            <div class="stats">
                <div class="stat"><div class="stat-number">{len(concepts)}</div><div class="stat-label">Concepts</div></div>
                <div class="stat"><div class="stat-number">{len(domain_counts)}</div><div class="stat-label">Domains</div></div>
                <div class="stat"><div class="stat-number">CC BY-SA 4.0</div><div class="stat-label">License</div></div>
            </div>
        </div>
    </header>
    <main class="container">
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All ({len(concepts)})</button>
            {''.join(domain_filters)}
        </div>
        <div class="concept-grid">
            {''.join(concept_cards)}
        </div>
    </main>
    <footer>
        <div class="container">
            <p>CADMIES — Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem</p>
            <p>All concepts licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Each concept has a permanent CID (Content Identifier).</p>
            <p><a href="sitemap.xml">Sitemap</a> · <a href="concepts.json">JSON Feed</a></p>
        </div>
    </footer>
    <script>
        // Domain filter functionality
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.filter;
                document.querySelectorAll('.concept-card').forEach(card => {{
                    if (filter === 'all' || card.dataset.domain === filter) {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>'''


def build_concept_page(concept, all_concepts):
    """Build an individual concept page."""
    # Relationship lists
    rel_sections = []
    for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
        targets = concept["relationships"].get(rel_type, [])
        if targets:
            label = RELATIONSHIP_LABELS.get(rel_type, rel_type)
            links = [f'<a href="{t["id"]}.html">{t["title"]}</a>' for t in targets]
            rel_sections.append(f'<div class="rel-section"><h3>{label}</h3><ul><li>' + '</li><li>'.join(links) + '</li></ul></div>')
    
    # Poetic version
    poetic_html = ""
    if concept.get("poetic_version"):
        poetic_html = f'<div class="poetic"><h3>Poetic Version</h3><blockquote>{concept["poetic_version"].replace(chr(10), "<br>")}</blockquote></div>'
    
    # Mantra
    mantra_html = ""
    if concept.get("mantra"):
        mantra_html = f'<div class="mantra"><h3>Mantra</h3><p><em>"{concept["mantra"]}"</em></p></div>'
    
    # Insight
    insight_html = ""
    if concept.get("insight"):
        insight_html = f'<div class="insight"><h3>Core Insight</h3><p>{concept["insight"]}</p></div>'
    
    domain_class = concept["domain"].lower().replace(" ", "-").replace("_", "-")
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{concept["title"]} — CADMIES Mycelium</title>
    <meta name="description" content="{concept["definition"][:160]}">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": "{concept["title"]}",
        "description": "{concept["definition"][:300]}",
        "inDefinedTermSet": {{
            "@type": "DefinedTermSet",
            "name": "CADMIES Mycelium",
            "url": "https://github.com/Hieros-CADMIES/CADMIES"
        }},
        "termCode": "{concept["cid"]}",
        "url": "https://hieros-cadmies.github.io/CADMIES/public/{concept["human_id"]}.html"
    }}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #F8FAFC; color: #0F172A; line-height: 1.7; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        header {{ background: #0F172A; color: #FFFFFF; padding: 30px 20px; }}
        header a {{ color: #94A3B8; text-decoration: none; font-size: 0.9em; }}
        header a:hover {{ color: #FFFFFF; }}
        .concept-header {{ padding: 30px 0 20px; }}
        .domain-badge {{ display: inline-block; padding: 3px 12px; border-radius: 12px; font-size: 0.8em; font-weight: 600; margin-bottom: 10px; }}
        .domain-physics {{ background: #EEF2FF; color: #4F46E5; }}
        .domain-philosophy {{ background: #F0EFFF; color: #6366F1; }}
        .domain-biology {{ background: #ECFDF5; color: #10B981; }}
        .domain-mathematics {{ background: #1E1B4B; color: #C7D2FE; }}
        .domain-ethics {{ background: #FDF2F8; color: #EC4899; }}
        .domain-psychology {{ background: #F0FDFA; color: #14B8A6; }}
        .domain-chemistry {{ background: #FFFBEB; color: #F59E0B; }}
        .domain-genomics {{ background: #F5F3FF; color: #8B5CF6; }}
        .domain-consciousness {{ background: #F1F5F9; color: #0F172A; }}
        .domain-epistemology {{ background: #F0EFFF; color: #6366F1; }}
        .domain-complexity-science {{ background: #1E1B4B; color: #C7D2FE; }}
        .domain-ecology {{ background: #ECFDF5; color: #10B981; }}
        .domain-spirituality {{ background: #F5F3FF; color: #A78BFA; }}
        .domain-buddhism {{ background: #F5F3FF; color: #A78BFA; }}
        .domain-buddhist-philosophy {{ background: #F5F3FF; color: #A78BFA; }}
        .domain-cosmology {{ background: #EEF2FF; color: #4F46E5; }}
        .domain-computer-science {{ background: #EFF6FF; color: #3B82F6; }}
        .domain-cognitive-science {{ background: #F0FDFA; color: #14B8A6; }}
        .domain-neuroscience {{ background: #F0FDFA; color: #14B8A6; }}
        .domain-sociology {{ background: #FDF2F8; color: #EC4899; }}
        .domain-economics {{ background: #FFFBEB; color: #F59E0B; }}
        .domain-education {{ background: #EFF6FF; color: #3B82F6; }}
        .domain-political-science {{ background: #FDF2F8; color: #EC4899; }}
        .domain-medicine {{ background: #ECFDF5; color: #10B981; }}
        .domain-artificial-intelligence {{ background: #EFF6FF; color: #3B82F6; }}
        .domain-theoretical-physics {{ background: #EEF2FF; color: #4F46E5; }}
        .domain-metaphysics {{ background: #F0EFFF; color: #6366F1; }}
        .domain-molecular-biology {{ background: #ECFDF5; color: #10B981; }}
        h1 {{ font-size: 1.8em; margin-bottom: 10px; }}
        .definition {{ font-size: 1.05em; color: #334155; margin: 20px 0; padding: 20px; background: #FFFFFF; border-radius: 10px; border: 1px solid #E2E8F0; }}
        .rel-section {{ margin: 15px 0; }}
        .rel-section h3 {{ font-size: 0.9em; color: #64748B; margin-bottom: 6px; }}
        .rel-section ul {{ list-style: none; }}
        .rel-section li {{ margin: 4px 0; }}
        .rel-section a {{ color: #4F46E5; text-decoration: none; }}
        .rel-section a:hover {{ text-decoration: underline; }}
        .poetic, .mantra, .insight {{ margin: 20px 0; padding: 20px; background: #FFFFFF; border-radius: 10px; border: 1px solid #E2E8F0; }}
        .poetic blockquote {{ font-style: italic; color: #475569; border-left: 3px solid #4F46E5; padding-left: 15px; }}
        .mantra em {{ color: #6366F1; }}
        .cid-box {{ margin: 20px 0; padding: 15px; background: #F1F5F9; border-radius: 8px; font-size: 0.85em; }}
        .cid-box code {{ word-break: break-all; color: #0F172A; }}
        footer {{ text-align: center; padding: 40px 20px; color: #94A3B8; font-size: 0.85em; border-top: 1px solid #E2E8F0; margin-top: 40px; }}
        footer a {{ color: #4F46E5; }}
        @media (max-width: 640px) {{
            h1 {{ font-size: 1.4em; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="index.html">← Back to Mycelium Index</a>
        </div>
    </header>
    <main class="container">
        <div class="concept-header">
            <span class="domain-badge domain-{domain_class}">{concept["domain_display"]}</span>
            <h1>{concept["title"]}</h1>
        </div>
        <div class="definition">
            <p>{concept["definition"]}</p>
        </div>
        {insight_html}
        {poetic_html}
        {mantra_html}
        {''.join(rel_sections) if rel_sections else '<p><em>No relationships recorded yet.</em></p>'}
        <div class="cid-box">
            <strong>Permanent CID:</strong><br>
            <code>{concept["cid"]}</code>
        </div>
        <p style="font-size:0.85em;color:#64748B;">Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. This concept is part of the CADMIES open knowledge graph.</p>
    </main>
    <footer>
        <div class="container">
            <p>🌱 CADMIES Mycelium — Content-addressed knowledge, forever.</p>
            <p><a href="index.html">All Concepts</a> · <a href="sitemap.xml">Sitemap</a></p>
        </div>
    </footer>
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
            "url": f"https://hieros-cadmies.github.io/CADMIES/public/{c['human_id']}.html",
        })
    return json.dumps({"@context": "https://schema.org", "@graph": items}, indent=2)


def build_sitemap(concepts):
    """Build XML sitemap for search engines."""
    urls = ['<url><loc>https://hieros-cadmies.github.io/CADMIES/public/index.html</loc></url>']
    for c in concepts:
        urls.append(f'<url><loc>https://hieros-cadmies.github.io/CADMIES/public/{c["human_id"]}.html</loc></url>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''


def main():
    print("=" * 60)
    print("CADMIES PUBLIC MYCELIUM GATEWAY GENERATOR v1.0.0")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    concepts, domain_counts = gather_public_concepts()
    print(f"\nLoaded {len(concepts)} concepts across {len(domain_counts)} domains")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build index page
    print("Generating index.html...")
    index_html = build_index_page(concepts, domain_counts)
    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(index_html)

    # Build individual concept pages
    print(f"Generating {len(concepts)} concept pages...")
    for c in concepts:
        page_html = build_concept_page(c, concepts)
        with open(OUTPUT_DIR / f"{c['human_id']}.html", "w") as f:
            f.write(page_html)

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

    print(f"\n✅ Public gateway generated: {OUTPUT_DIR}")
    print(f"   {len(concepts)} concept pages + index + JSON feed + sitemap")
    print(f"   Deploy: push to GitHub, enable Pages on /docs folder")


if __name__ == "__main__":
    main()