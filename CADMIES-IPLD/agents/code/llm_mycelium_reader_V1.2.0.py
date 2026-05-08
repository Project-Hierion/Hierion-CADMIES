"""
File: llm_mycelium_reader.py
Agent: Willie the Librarian
Author: CADMIES Research Group
Created: 2026-05-01
Updated: 2026-05-05 — Hybrid search + accuracy tags merge
Version: 1.2.0
System: CADMIES IPLD - LLM Bridge Agent
Agent Type: llm_mycelium_reader
Status: ACTIVE

Purpose: Bridge between natural language and the CADMIES mycelium.
         Reads concepts from blockstore, feeds them as context to a local
         LLM via Ollama, and returns informed answers with CID references.

Version 1.2.0 Changes (merge of two 1.1.0 branches):
  - Hybrid search: keyword matching + Mistral-powered semantic query expansion
  - Accuracy tags system: (empirical), (philosophical), (speculative), (CADMIES-defined)
  - Improved system prompt with four-step answer structure and full CADMIES name
  - search_mycelium() now accepts use_semantic parameter
  - keyword_search() extracted as standalone precision search
  - expand_query_semantically() bridges everyday language to technical vocabulary
  - load_all_concepts() helper added
  - CLI: --semantic and --keyword-only flags

Dependencies: ollama (pip install ollama), dag_cbor, json, re, collections
Air-Gapped: Yes (Ollama runs on localhost:11434, no external APIs)
"""

import json
import re
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

__version__ = "1.2.0"

# Try importing dag_cbor for block reading
try:
    import dag_cbor
    DAG_CBOR_AVAILABLE = True
except ImportError:
    DAG_CBOR_AVAILABLE = False
    print("WARNING: dag_cbor not available - using JSON fallback")

# Try importing ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("WARNING: ollama not installed. Install with: pip install ollama")


def get_project_root() -> Path:
    """Get the CADMIES project root directory."""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    return project_root


PROJECT_ROOT = get_project_root()
BLOCKSTORE_PATH = PROJECT_ROOT / "store" / "blocks"
INDEX_PATH = PROJECT_ROOT / "store" / "index" / "human_id_to_cid.json"

# Willie's personality quotes for response flavor
WILLIE_QUOTES = [
    "Ach, let me dig through the stacks for ye...",
    "Och, I remember where that one's filed...",
    "Back in the depths of the mycelium, I found...",
    "Aye, the spores whisper of this one...",
    "Greasin' the wheels of knowledge for ye...",
    "This concept's been gatherin' dust, good ye asked...",
]


def load_concept(cid: str, blockstore_path: Path = None) -> Dict[str, Any]:
    """
    Load a concept by CID from blockstore.
    
    Args:
        cid: Content Identifier of the concept
        blockstore_path: Optional path to blockstore
        
    Returns:
        Dict containing concept data, or error dict
    """
    if not cid.startswith('bafy'):
        return {'error': f"Invalid CID format: {cid}", 'cid': cid}
    
    if blockstore_path is None:
        blockstore_path = BLOCKSTORE_PATH
    
    cbor_file = blockstore_path / f"{cid}.cbor"
    if not cbor_file.exists():
        cbor_file = blockstore_path / cid
    
    if not cbor_file.exists():
        return {'error': f"Block not found: {cid}", 'cid': cid}
    
    try:
        with open(cbor_file, 'rb') as f:
            raw_data = f.read()
        
        if DAG_CBOR_AVAILABLE:
            return dag_cbor.decode(raw_data)
        else:
            return json.loads(raw_data.decode('utf-8'))
    except Exception as e:
        return {'error': f"Decode failed: {e}", 'cid': cid}


def load_all_concept_cids() -> List[str]:
    """Get all CIDs from the human_id index."""
    if not INDEX_PATH.exists():
        return []
    
    with open(INDEX_PATH, 'r') as f:
        index = json.load(f)
    
    return list(index.values())


def load_all_concepts() -> Dict[str, Dict[str, Any]]:
    """
    Load all concepts from the blockstore into a dictionary keyed by CID.
    Returns empty dict if index or blocks are unavailable.
    """
    all_cids = load_all_concept_cids()
    concepts = {}
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' not in concept:
            concepts[cid] = concept
    return concepts


def expand_query_semantically(text: str, model: str = "mistral:7b") -> List[str]:
    """
    Use Mistral to expand a query or conversation snippet into related search terms,
    synonyms, and domain-specific vocabulary. Bridges the gap between everyday
    language and technical/philosophical terminology.
    
    Args:
        text: The query or conversation text to expand
        model: Ollama model to use for expansion (default: mistral:7b)
        
    Returns:
        List of expanded search terms
    """
    if not OLLAMA_AVAILABLE:
        return []
    
    expansion_prompt = (
        "You are a search query expander for a knowledge system containing concepts "
        "in philosophy, biology, cognitive science, buddhist philosophy, complexity science, "
        "physics, and related domains.\n\n"
        "Given the text below, generate a list of search keywords and phrases that would "
        "help find RELATED concepts — even ones that use different vocabulary.\n\n"
        "Think across domains:\n"
        "- If the text mentions vampires, also think about: parasitism, symbiosis, predation, hematophagy\n"
        "- If the text mentions letting go, also think about: non-attachment, acceptance, wu wei, surrender\n"
        "- If the text mentions patterns, also think about: fractals, emergence, self-organization\n"
        "- If the text mentions the self, also think about: anatta, ego, identity, consciousness\n\n"
        "Include synonyms, broader terms, narrower terms, and domain-specific technical vocabulary.\n"
        "Return ONLY a comma-separated list of keywords and short phrases. No other text.\n\n"
        "TEXT TO EXPAND:\n" + text[:2000]
    )
    
    try:
        response = ollama.generate(
            model=model,
            prompt=expansion_prompt,
            options={
                'temperature': 0.3,
                'num_predict': 150,
            }
        )
        raw = response.get('response', '').strip()
        
        # Parse comma-separated list
        terms = []
        for term in raw.split(','):
            cleaned = term.strip().strip('"').strip("'").lower()
            if cleaned and len(cleaned) > 2:
                terms.append(cleaned)
        
        return terms
        
    except Exception as e:
        print(f"  (Query expansion failed: {e})")
        return []


def keyword_search(query: str, all_cids: List[str]) -> List[Dict[str, Any]]:
    """
    Original keyword-based search. Tokenizes query and matches against
    title, definition, human_id, and domain. Precision-focused.
    
    Args:
        query: User's question or conversation text
        all_cids: List of all CIDs to search through
        
    Returns:
        List of relevant concepts with relevance scores
    """
    query_terms = set(re.findall(r'[a-zA-Z]{3,}', query.lower()))
    
    results = []
    
    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue
        
        title = concept.get('title', '').lower()
        definition = concept.get('definition', '').lower()
        human_id = concept.get('human_id', '').lower()
        domain = concept.get('domain', '').lower()
        
        search_text = f"{title} {definition} {human_id} {domain}"
        search_terms = set(re.findall(r'[a-zA-Z]{3,}', search_text))
        
        matches = query_terms.intersection(search_terms)
        
        if matches:
            score = len(matches) / max(len(query_terms), 1)
            results.append({
                'cid': cid,
                'title': concept.get('title', 'Unknown'),
                'human_id': concept.get('human_id', ''),
                'domain': concept.get('domain', 'Unknown'),
                'definition_snippet': definition[:300] if definition else '',
                'relevance_score': round(score, 3),
                'matched_terms': list(matches)[:5],
                'match_type': 'keyword'
            })
    
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results


def search_mycelium(
    query: str,
    all_cids: List[str],
    use_semantic: bool = True,
    semantic_model: str = "mistral:7b",
    keyword_weight: float = 0.6,
    semantic_weight: float = 0.4
) -> List[Dict[str, Any]]:
    """
    Hybrid search: combines keyword matching (precision) with semantic query
    expansion (recall) to find relevant concepts across vocabulary boundaries.
    
    Args:
        query: User's question or conversation text
        all_cids: List of all CIDs to search through
        use_semantic: Enable semantic query expansion (default: True)
        semantic_model: Ollama model for query expansion
        keyword_weight: Weight for keyword match scores (default: 0.6)
        semantic_weight: Weight for semantic match scores (default: 0.4)
        
    Returns:
        List of relevant concepts with combined relevance scores,
        deduplicated across both search methods, with match_type labels
    """
    
    # === KEYWORD SEARCH (always runs) ===
    keyword_results = keyword_search(query, all_cids)
    
    # Track which CIDs we've found and their current best scores
    combined = {}
    for r in keyword_results:
        combined[r['cid']] = {
            'cid': r['cid'],
            'title': r['title'],
            'human_id': r['human_id'],
            'domain': r['domain'],
            'definition_snippet': r['definition_snippet'],
            'relevance_score': r['relevance_score'] * keyword_weight,
            'matched_terms': r.get('matched_terms', []),
            'match_type': 'keyword'
        }
    
    # === SEMANTIC SEARCH (optional) ===
    if use_semantic and OLLAMA_AVAILABLE:
        print("  Expanding query for semantic search...")
        expanded_terms = expand_query_semantically(query, semantic_model)
        
        if expanded_terms:
            print(f"  Semantic terms: {', '.join(expanded_terms[:10])}")
            # Run keyword search using the expanded terms
            expanded_query = ' '.join(expanded_terms)
            semantic_results = keyword_search(expanded_query, all_cids)
            
            # Merge with combined dict, applying semantic weight
            for r in semantic_results:
                cid = r['cid']
                semantic_score = r['relevance_score'] * semantic_weight
                
                if cid in combined:
                    # Add semantic score to existing keyword score
                    combined[cid]['relevance_score'] += semantic_score
                    combined[cid]['match_type'] = 'hybrid'
                    # Merge matched terms
                    existing_terms = set(combined[cid].get('matched_terms', []))
                    new_terms = set(r.get('matched_terms', []))
                    combined[cid]['matched_terms'] = list(existing_terms | new_terms)[:8]
                else:
                    # New concept found only via semantic search
                    combined[cid] = {
                        'cid': r['cid'],
                        'title': r['title'],
                        'human_id': r['human_id'],
                        'domain': r['domain'],
                        'definition_snippet': r['definition_snippet'],
                        'relevance_score': semantic_score,
                        'matched_terms': r.get('matched_terms', []),
                        'match_type': 'semantic'
                    }
        else:
            print("  (No semantic terms generated — using keyword results only)")
    
    # Convert back to sorted list
    results = list(combined.values())
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    # Report match types for debugging
    if use_semantic:
        kw_count = sum(1 for r in results if r['match_type'] == 'keyword')
        hy_count = sum(1 for r in results if r['match_type'] == 'hybrid')
        sm_count = sum(1 for r in results if r['match_type'] == 'semantic')
        print(f"  Search results: {kw_count} keyword, {hy_count} hybrid, {sm_count} semantic-only")
    
    return results


def build_context_for_llm(relevant_concepts: List[Dict], max_concepts: int = 3) -> str:
    """
    Build a context string from relevant concepts for the LLM prompt.
    
    Args:
        relevant_concepts: List of concept dicts from search_mycelium
        max_concepts: Maximum number of concepts to include
        
    Returns:
        Formatted context string
    """
    if not relevant_concepts:
        return "No relevant concepts found in the mycelium."
    
    context_parts = []
    
    for i, concept in enumerate(relevant_concepts[:max_concepts]):
        context_parts.append(f"CADMIES CONCEPT {i+1}: {concept['title']}")
        context_parts.append(f"Domain: {concept['domain']}")
        context_parts.append(f"CID: {concept['cid']}")
        context_parts.append(f"Mycelium definition: {concept['definition_snippet']}")
        context_parts.append("")
    
    return "\n".join(context_parts)


def query_mycelium(concept_cids: List[str] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main entry point for Willie the Librarian.
    
    Takes a natural language query, searches the mycelium for relevant
    concepts using hybrid search, feeds them to the LLM via Ollama, and
    returns an informed answer with CID references and accuracy tags.
    
    Args:
        concept_cids: Optional list of specific CIDs to search (uses all if None)
        context: Execution context with keys:
            - user_query: Natural language question (required)
            - model: Ollama model name (default: "tinyllama:1.1b")
            - max_concepts: Max concepts to feed LLM (default: 3)
            - tone: Response tone (default: "helpful")
            - analysis_depth: basic/detailed/comprehensive (default: "basic")
            - use_semantic: Enable hybrid search (default: True)
        
    Returns:
        Dict with query, answer, concepts_used, and metadata
    """
    start_time = time.time()
    
    if context is None:
        context = {}
    
    user_query = context.get('user_query', '')
    model = context.get('model', 'tinyllama:1.1b')
    max_concepts = context.get('max_concepts', 3)
    tone = context.get('tone', 'helpful')
    use_semantic = context.get('use_semantic', True)
    
    if not user_query:
        return {
            'success': False,
            'error': "No user_query provided in context. "
                     "Usage: query_mycelium(context={'user_query': 'What is natural selection?'})",
            'metadata': {'willie_says': "Ach, ye gotta ask me somethin' first!"}
        }
    
    if not OLLAMA_AVAILABLE:
        return {
            'success': False,
            'error': "Ollama Python package not installed. Install with: pip install ollama",
            'metadata': {'willie_says': "The pipes to the thinkin' machine are clogged!"}
        }
    
    print(f"\n{'='*60}")
    print(f"WILLIE THE LIBRARIAN v{__version__} - QUERY")
    print(f"{'='*60}")
    print(f"Query: {user_query}")
    print(f"Model: {model}")
    print(f"Max Concepts: {max_concepts}")
    print(f"Hybrid Search: {'ON' if use_semantic else 'OFF (keyword only)'}")
    
    # Step 1: Get CIDs to search
    if concept_cids:
        search_cids = concept_cids
        print(f"Searching {len(search_cids)} specified CIDs")
    else:
        search_cids = load_all_concept_cids()
        print(f"Searching all {len(search_cids)} indexed concepts")
    
    # Step 2: Hybrid search
    print("\nSEARCHING MYCELIUM...")
    relevant = search_mycelium(
        user_query,
        search_cids,
        use_semantic=use_semantic,
        semantic_model="mistral:7b"
    )
    
    if not relevant:
        return {
            'success': True,
            'query': user_query,
            'answer': "Ach, I dug through the whole mycelium and couldn't find any concepts "
                      "matchin' yer query. Try different keywords or add more concepts to the store.",
            'concepts_used': 0,
            'concepts_found': 0,
            'metadata': {
                'model': model,
                'execution_time_seconds': round(time.time() - start_time, 2),
                'willie_says': "Nothin' in the stacks for that one, pal."
            }
        }
    
    print(f"Found {len(relevant)} relevant concepts")
    for r in relevant[:5]:
        print(f"  - {r['title']} [{r.get('match_type', 'unknown')}] (score: {r['relevance_score']:.3f})")
    
    # Step 3: Build context for LLM
    context_str = build_context_for_llm(relevant, max_concepts)
    
    # Step 4: Build prompt with accuracy tags
    system_prompt = (
        f"You are Willie the Librarian, caretaker of CADMIES (Cosmium Angelo Digital "
        f"Mycorrhizal Intelligence EcoSystem) — a content-addressed "
        f"knowledge network of scientific and philosophical concepts.\n\n"
        f"HOW TO ANSWER:\n"
        f"1. FIRST: Answer the user's question using YOUR OWN knowledge. "
        f"Explain the topic clearly in natural language.\n"
        f"2. SECOND: Compare your answer to what CADMIES says. "
        f"Point out where the mycelium concepts agree, differ, or add nuance. "
        f"Say things like 'The CADMIES concept of X defines this as...' or "
        f"'My understanding aligns with the mycelium here, because...'\n"
        f"3. THIRD: Explain how the mycelium concepts connect to each other. "
        f"Find the threads between them — shared domains, complementary ideas, tensions.\n"
        f"4. FINALLY: Give a brief summary that weaves everything together.\n\n"
        f"ACCURACY TAGS: After EVERY factual claim, append a tag in parentheses "
        f"to indicate its epistemic status:\n"
        f"  (empirical) — Established scientific fact, verifiable by experimental evidence\n"
        f"  (philosophical) — Philosophical argument, logical inquiry, or conceptual analysis\n"
        f"  (speculative) — Theoretical, hypothetical, or conjectural; not yet verified\n"
        f"  (CADMIES-defined) — A term or concept defined specifically within the CADMIES "
        f"ecosystem, which may differ from mainstream usage\n\n"
        f"IMPORTANT: Tag EVERY factual statement. If you say 'Natural selection drives "
        f"evolution', tag it. If you say 'The mycelium defines consciousness as...', "
        f"tag it. Be honest about what is proven and what is speculative.\n\n"
        f"Example: 'Natural selection explains how organisms with advantageous heritable "
        f"traits survive and reproduce at higher rates (empirical). The mycelium defines "
        f"it as differential survival and reproduction of individuals due to differences "
        f"in heritable traits (CADMIES-defined — aligns with standard definition). "
        f"The Fractal Resonance Hypothesis suggests the same patterns echo at every "
        f"scale of existence (speculative).'\n\n"
        f"TONE: {tone}. Speak with occasional Scottish groundskeeper flavor — "
        f"just a wee bit, don't overdo it.\n\n"
        f"If the mycelium doesn't have relevant concepts, say so honestly "
        f"and just answer from your own knowledge."
    )
    
    full_prompt = f"{context_str}\n\nUser Question: {user_query}\n\nWillie's Answer:"
    
    # Step 5: Query Ollama
    print(f"\nASKING {model}...")
    
    try:
        response = ollama.generate(
            model=model,
            prompt=full_prompt,
            system=system_prompt,
            options={
                'temperature': 0.7,
                'num_predict': 800,
            }
        )
        
        answer = response.get('response', '').strip()
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Ollama query failed: {e}",
            'metadata': {
                'model': model,
                'willie_says': "The thinkin' machine's on strike! Is Ollama runnin'?"
            }
        }
    
    execution_time = round(time.time() - start_time, 2)
    
    print(f"\nANSWER ({execution_time}s):")
    print(answer[:200] + "..." if len(answer) > 200 else answer)
    
    # Step 6: Return results
    return {
        'success': True,
        'query': user_query,
        'answer': answer,
        'concepts_used': min(len(relevant), max_concepts),
        'concepts_found': len(relevant),
        'concepts_referenced': [
            {
                'cid': c['cid'],
                'title': c['title'],
                'relevance_score': c['relevance_score'],
                'match_type': c.get('match_type', 'unknown')
            }
            for c in relevant[:max_concepts]
        ],
        'metadata': {
            'model': model,
            'tone': tone,
            'execution_time_seconds': execution_time,
            'agent_version': __version__,
            'hybrid_search': use_semantic,
            'willie_says': WILLIE_QUOTES[hash(user_query) % len(WILLIE_QUOTES)]
        }
    }


def test_agent() -> Dict[str, Any]:
    """
    Self-test: verify Willie can connect to Ollama and read the mycelium
    with hybrid search operational.
    """
    print("=" * 60)
    print(f"WILLIE THE LIBRARIAN v{__version__} - SELF TEST")
    print("=" * 60)
    
    if not OLLAMA_AVAILABLE:
        print("FAILED: Ollama not installed")
        return {'success': False, 'error': 'Ollama not installed'}
    
    # Test 1: Check Ollama connection
    print("\nTEST 1: Ollama connectivity...")
    try:
        list_response = ollama.list()
        model_names = [m.model for m in list_response.models]
        print(f"  Connected! Available models: {model_names}")
    except Exception as e:
        print(f"  FAILED: {e}")
        return {'success': False, 'error': f'Ollama connection failed: {e}'}
    
    # Test 2: Load mycelium index
    print("\nTEST 2: Mycelium access...")
    all_cids = load_all_concept_cids()
    print(f"  Found {len(all_cids)} indexed concepts")
    
    if len(all_cids) < 1:
        print("  WARNING: No concepts in index — run import_from_github.py first")
    
    # Test 3: Keyword search
    print("\nTEST 3: Keyword search...")
    test_query = "natural selection"
    results = keyword_search(test_query, all_cids)
    print(f"  Query '{test_query}' found {len(results)} keyword results")
    
    # Test 4: Hybrid search
    print("\nTEST 4: Hybrid search (keyword + semantic)...")
    results = search_mycelium(test_query, all_cids, use_semantic=True)
    print(f"  Hybrid search found {len(results)} total results")
    for r in results[:3]:
        print(f"    - {r['title']} [{r.get('match_type', '?')}] score={r['relevance_score']:.3f}")
    
    # Test 5: Full LLM query
    print("\nTEST 5: LLM query test...")
    test_context = {
        'user_query': "What concepts in the mycelium relate to evolution or natural selection?",
        'model': 'tinyllama:1.1b',
        'max_concepts': 2,
        'tone': 'helpful',
        'use_semantic': True
    }
    
    result = query_mycelium(context=test_context)
    
    if result['success']:
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED - Willie is operational!")
        print("=" * 60)
    else:
        print(f"\nFAILED: {result.get('error')}")
    
    return result


# Command-line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Willie the Librarian - Ask the mycelium questions via local LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python llm_mycelium_reader.py --test
  python llm_mycelium_reader.py --query "What is natural selection?"
  python llm_mycelium_reader.py --query "Explain entropy" --model mistral:7b
  python llm_mycelium_reader.py --query "Find concepts about evolution" --max-concepts 5
  python llm_mycelium_reader.py --query "vampire feeding" --semantic
  python llm_mycelium_reader.py --query "Fact-check concept X" --tone scholarly
        """
    )
    
    parser.add_argument('--test', action='store_true', help='Run self-test')
    parser.add_argument('--query', type=str, help='Natural language question for Willie')
    parser.add_argument('--model', type=str, default='tinyllama:1.1b',
                       help='Ollama model (default: tinyllama:1.1b)')
    parser.add_argument('--max-concepts', type=int, default=3,
                       help='Max concepts to feed LLM (default: 3)')
    parser.add_argument('--tone', type=str, default='helpful',
                       choices=['helpful', 'scholarly', 'casual', 'scottish'],
                       help='Response tone (default: helpful)')
    parser.add_argument('--cids', nargs='+', help='Specific CIDs to search instead of all')
    parser.add_argument('--semantic', action='store_true', default=True,
                       help='Enable hybrid semantic search (default: True)')
    parser.add_argument('--keyword-only', action='store_true',
                       help='Disable semantic search, use keyword only')
    
    args = parser.parse_args()
    
    # Handle --keyword-only override
    use_semantic = args.semantic and not args.keyword_only
    
    if args.test:
        result = test_agent()
        
    elif args.query:
        context = {
            'user_query': args.query,
            'model': args.model,
            'max_concepts': args.max_concepts,
            'tone': args.tone,
            'use_semantic': use_semantic
        }
        
        result = query_mycelium(concept_cids=args.cids, context=context)
        
        if result['success']:
            print(f"\n{'='*60}")
            print(f"WILLIE SAYS:")
            print(f"{'='*60}")
            print(result['answer'])
            print(f"\n{'='*60}")
            print(f"Concepts referenced: {result['concepts_used']}")
            for c in result.get('concepts_referenced', []):
                print(f"  - {c['title']} [{c.get('match_type', '?')}] ({c['cid'][:16]}...)")
            print(f"Time: {result['metadata']['execution_time_seconds']}s")
            print(f"Model: {result['metadata']['model']}")
            print(f"Willie: \"{result['metadata']['willie_says']}\"")
        else:
            print(f"ERROR: {result.get('error')}")
        
        # Save results
        results_dir = PROJECT_ROOT / "analysis_results"
        results_dir.mkdir(exist_ok=True)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        output_file = results_dir / f"willie_query_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nFull results saved to: {output_file}")
        
    else:
        parser.print_help()
        print("\nAch, ye need to ask me somethin'! Try --test or --query.")