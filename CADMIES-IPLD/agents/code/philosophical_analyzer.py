"""
File: philosophical_analyzer.py
Author: CADMIES Research Group
Created: 2025-12-29
Version: 1.0.1
System: CADMIES
Document_ID: CA-2025-047-IMPLEMENTATION
Status: PUBLIC RELEASE
Modified: 2026-05-12
Related_Docs:
  - Runtime Interpreter Design Specification v1.0.0
  - Agent Schema Development Roadmap v1.0.0
  - CADMIES IPLD Technical Documentation
"""

"""
Philosophical Analyzer Agent Implementation v1.0.0
Purpose: Analyze philosophical concepts for patterns and connections
Signature: analyze_philosophical_patterns(concept_cids: list, context: dict) -> dict
Dependencies: json, re, collections (Python stdlib only)
Air-Gapped: Yes (no external dependencies)
"""

import json
import re
import time
import base64
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any, Optional

__version__ = "1.0.0"

# Use existing dag_cbor from our system
try:
    import dag_cbor
    DAG_CBOR_AVAILABLE = True
except ImportError:
    DAG_CBOR_AVAILABLE = False
    print("WARNING: dag_cbor not available - using JSON fallback")

def get_project_root() -> Path:
    """
    Get the CADMIES project root directory.
    Assumes this file is at: CADMIES-IPLD/agents_workspace/philosophical_analyzer.py
    """
    current_file = Path(__file__).resolve()
    # Go up to CADMIES-IPLD root
    project_root = current_file.parent.parent.parent
    return project_root

PROJECT_ROOT = get_project_root()
BLOCKSTORE_PATH = PROJECT_ROOT / "store" / "blocks"

def load_concept(cid: str, blockstore_path: Path = None) -> Dict[str, Any]:
    """
    Load a concept by CID from blockstore.
    
    Args:
        cid: Content Identifier of the concept
        blockstore_path: Optional path to blockstore (default: auto-detected)
        
    Returns:
        Dict containing concept data
        
    Raises:
        FileNotFoundError: If concept block doesn't exist
        ValueError: If CID format is invalid
    """
    if not cid.startswith('bafy'):
        raise ValueError(f"Invalid CID format: {cid}")
    
    # Determine blockstore path
    if blockstore_path is None:
        blockstore_path = BLOCKSTORE_PATH
    
    # Try with .cbor extension first
    cbor_file = blockstore_path / f"{cid}.cbor"
    if not cbor_file.exists():
        # Try without extension (legacy format)
        cbor_file = blockstore_path / cid
    
    if not cbor_file.exists():
        raise FileNotFoundError(f"Concept block not found: {cid} at {cbor_file}")
    
    with open(cbor_file, 'rb') as f:
        raw_data = f.read()
    
    if DAG_CBOR_AVAILABLE:
        try:
            return dag_cbor.decode(raw_data)
        except Exception as e:
            print(f"WARNING: DAG-CBOR decode failed for {cid}: {e}")
    
    # Fallback to JSON
    try:
        return json.loads(raw_data.decode('utf-8'))
    except Exception as e:
        print(f"ERROR: Failed to decode {cid}: {e}")
        return {
            'error': str(e), 
            'cid': cid, 
            '_raw': base64.b64encode(raw_data[:100]).decode('utf-8')
        }

def extract_key_terms(text: str, min_length: int = 4) -> List[str]:
    """
    Extract meaningful terms from text.
    
    Args:
        text: Input text to analyze
        min_length: Minimum word length to consider
        
    Returns:
        List of key terms
    """
    if not text:
        return []
    
    # Convert to lowercase
    text_lower = text.lower()
    
    # Remove common stop words (minimal set for philosophical text)
    stop_words = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'has', 
                  'was', 'were', 'are', 'is', 'be', 'been', 'being', 'does', 'do'}
    
    # Extract words (allow hyphens in words)
    words = re.findall(r'\b[a-z][a-z-]{2,}\b', text_lower)
    
    # Filter and return
    filtered_words = []
    for word in words:
        # Remove hyphens for length check
        clean_word = word.replace('-', '')
        if clean_word not in stop_words and len(clean_word) >= min_length:
            filtered_words.append(word)
    
    return filtered_words

def find_semantic_connections(concept1: Dict, concept2: Dict) -> List[Dict]:
    """
    Find semantic connections between two concepts.
    
    Args:
        concept1: First concept data
        concept2: Second concept data
        
    Returns:
        List of connection objects
    """
    connections = []
    
    # Check for shared domain
    domain1 = concept1.get('domain')
    domain2 = concept2.get('domain')
    if domain1 and domain1 == domain2:
        connections.append({
            'type': 'shared_domain',
            'description': f"Both concepts belong to domain: {domain1}",
            'confidence': 0.8,
            'evidence': [domain1]
        })
    
    # Check for shared type
    type1 = concept1.get('type')
    type2 = concept2.get('type')
    if type1 and type1 == type2:
        connections.append({
            'type': 'shared_type',
            'description': f"Both are {type1} concepts",
            'confidence': 0.7,
            'evidence': [type1]
        })
    
    # Check for shared subdomain
    subdomain1 = concept1.get('subdomain')
    subdomain2 = concept2.get('subdomain')
    if subdomain1 and subdomain1 == subdomain2:
        connections.append({
            'type': 'shared_subdomain',
            'description': f"Both focus on subdomain: {subdomain1}",
            'confidence': 0.9,
            'evidence': [subdomain1]
        })
    
    # Text-based similarity (simple version)
    text1 = f"{concept1.get('title', '')} {concept1.get('definition', '')}"
    text2 = f"{concept2.get('title', '')} {concept2.get('definition', '')}"
    
    terms1 = set(extract_key_terms(text1))
    terms2 = set(extract_key_terms(text2))
    
    shared_terms = terms1.intersection(terms2)
    if shared_terms:
        connections.append({
            'type': 'shared_terminology',
            'description': f"Share {len(shared_terms)} key terms",
            'confidence': min(0.3 + (len(shared_terms) * 0.1), 0.9),
            'evidence': list(sorted(shared_terms))[:5]
        })
    
    return connections

def analyze_philosophical_patterns(concept_cids: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze philosophical concepts for patterns and connections.
    
    Args:
        concept_cids: List of CIDs for philosophical concepts to analyze
        context: Optional execution context with metadata
        
    Returns:
        Dict with analysis results following the specification
        
    Example context:
        {
            "focus_area": "metaphysics",
            "analysis_depth": "basic|detailed|comprehensive",
            "previous_results": {...},
            "user_query": "Find connections between these concepts"
        }
    """
    start_time = time.time()
    
    # Initialize context
    if context is None:
        context = {}
    
    focus_area = context.get('focus_area', 'general')
    analysis_depth = context.get('analysis_depth', 'basic')
    
    print("PHILOSOPHICAL ANALYSIS STARTED")
    print(f"   Concepts: {len(concept_cids)}")
    print(f"   Focus: {focus_area}")
    print(f"   Depth: {analysis_depth}")
    
    # Load all concepts
    concepts = []
    load_errors = []
    
    for cid in concept_cids:
        try:
            concept_data = load_concept(cid, BLOCKSTORE_PATH)
            concepts.append({
                'cid': cid,
                'data': concept_data,
                'title': concept_data.get('title', 'Unknown'),
                'type': concept_data.get('type', 'Unknown'),
                'domain': concept_data.get('domain', 'Unknown'),
                'subdomain': concept_data.get('subdomain', ''),
                'definition': concept_data.get('definition', ''),
                'human_id': concept_data.get('human_id', '')
            })
            title = concept_data.get('title', cid[:16])
            print(f"   LOADED: {title}...")
        except Exception as e:
            error_msg = f"Failed to load {cid}: {e}"
            print(f"   ERROR: {error_msg}")
            load_errors.append(error_msg)
    
    if not concepts:
        return {
            'success': False,
            'error': 'No concepts could be loaded',
            'load_errors': load_errors,
            'metadata': {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'concepts_requested': len(concept_cids),
                'concepts_loaded': 0
            }
        }
    
    print(f"SUCCESS: Loaded {len(concepts)}/{len(concept_cids)} concepts")
    
    # Perform analysis based on depth
    results = {
        'success': True,
        'concepts_analyzed': len(concepts),
        'patterns_found': [],
        'connections': [],
        'insights': [],
        'recommendations': [],
        'metadata': {
            'analyzer_version': __version__,
            'analysis_timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'execution_time_seconds': 0,
            'focus_area': focus_area,
            'analysis_depth': analysis_depth,
            'load_errors': load_errors if load_errors else None
        }
    }
    
    # BASIC ANALYSIS (always performed)
    
    # 1. Domain distribution
    domains = Counter([c['domain'] for c in concepts if c['domain']])
    if domains:
        results['domain_distribution'] = dict(domains)
        if len(domains) == 1:
            results['insights'].append({
                'type': 'domain_focus',
                'description': f"All concepts focus on {list(domains.keys())[0]}",
                'confidence': 0.9
            })
    
    # 2. Type distribution
    types = Counter([c['type'] for c in concepts if c['type']])
    if types:
        results['type_distribution'] = dict(types)
    
    # 3. Term frequency analysis
    all_text = ' '.join([f"{c.get('title', '')} {c.get('definition', '')}" for c in concepts])
    key_terms = extract_key_terms(all_text)
    term_freq = Counter(key_terms)
    
    if term_freq:
        # Get top terms
        top_terms = dict(term_freq.most_common(10))
        results['common_terminology'] = top_terms
        
        # Look for interesting term patterns
        philosophical_terms = {'reality', 'consciousness', 'existence', 'knowledge', 
                              'truth', 'being', 'mind', 'nature', 'universe', 'theory'}
        found_terms = philosophical_terms.intersection(set(top_terms.keys()))
        if found_terms:
            results['insights'].append({
                'type': 'core_philosophical_terms',
                'description': f"Found core philosophical terms: {', '.join(sorted(found_terms))}",
                'confidence': 0.8
            })
    
    # DETAILED ANALYSIS (if requested)
    if analysis_depth in ['detailed', 'comprehensive']:
        # Find connections between all concept pairs
        all_connections = []
        
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                conns = find_semantic_connections(concepts[i], concepts[j])
                for conn in conns:
                    connection_record = {
                        'source_cid': concepts[i]['cid'],
                        'source_title': concepts[i]['title'],
                        'target_cid': concepts[j]['cid'],
                        'target_title': concepts[j]['title'],
                        'connection_type': conn['type'],
                        'description': conn['description'],
                        'confidence': conn['confidence'],
                        'evidence': conn.get('evidence', [])
                    }
                    all_connections.append(connection_record)
        
        results['connections'] = all_connections
        
        # Group connections by type
        if all_connections:
            connection_types = Counter([c['connection_type'] for c in all_connections])
            results['connection_analysis'] = {
                'total_connections': len(all_connections),
                'by_type': dict(connection_types),
                'strongest_connections': sorted(all_connections, 
                                               key=lambda x: x['confidence'], 
                                               reverse=True)[:5]
            }
    
    # COMPREHENSIVE ANALYSIS (additional insights)
    if analysis_depth == 'comprehensive' and len(concepts) >= 3:
        # Look for conceptual clusters
        domain_groups = defaultdict(list)
        for concept in concepts:
            if concept['domain']:
                domain_groups[concept['domain']].append(concept['title'])
        
        if len(domain_groups) > 1:
            results['insights'].append({
                'type': 'multi_domain_analysis',
                'description': f"Concepts span {len(domain_groups)} different domains",
                'confidence': 0.7,
                'details': {domain: len(titles) for domain, titles in domain_groups.items()}
            })
    
    # Generate recommendations
    if len(concepts) >= 2:
        results['recommendations'].append({
            'type': 'further_exploration',
            'description': f"Explore relationships between '{concepts[0]['title']}' and '{concepts[1]['title']}'",
            'reason': 'These are primary concepts with potential deep connections',
            'priority': 'high'
        })
    
    if len(concepts) > 2:
        results['recommendations'].append({
            'type': 'synthesis_opportunity',
            'description': f"Create synthetic concept combining insights from {len(concepts)} concepts",
            'reason': 'Multiple related concepts suggest synthesis potential',
            'priority': 'medium'
        })
    
    # Calculate execution time
    execution_time = time.time() - start_time
    results['metadata']['execution_time_seconds'] = execution_time
    
    print("ANALYSIS COMPLETE")
    print(f"   Patterns found: {len(results.get('patterns_found', []))}")
    print(f"   Connections: {len(results.get('connections', []))}")
    print(f"   Insights: {len(results.get('insights', []))}")
    print(f"   Time: {execution_time:.2f}s")
    
    return results

def test_agent() -> Dict[str, Any]:
    """
    Test function to verify the agent works with stored concepts.
    
    Returns:
        Test results
    """
    print("TESTING PHILOSOPHICAL ANALYZER AGENT")
    print("=" * 50)
    
    # Use the 5 philosophical concepts from the system
    test_cids = [
        "bafyreignxp73ooqeiwdgecmvqv7dbmnimm4orgyca7srzdiykm7kleqbja",  # fractal_reality_principle
        "bafyreiftvhx64umvh3jq3tjjzxw6vkcgom7nzqnfojdmqtn4v77bafwu7m",  # bond_breaking_as_liberation_mechanism
        "bafyreigcii5de4qhwnn25i62gxa245s5fwn5nbrzz3in346ut5kem4j474",  # cyclic_liberation_force_hypothesis
        "bafyreihlh4vwiexvuq667arus727jqs7sifuf3vjuyczwmqqcfpcopghsq",  # cosmic_mind_pattern_isomorphism
        "bafyreiht7rhfuixpxqtfelgckhwboi7ytzar4sullw2f73mksbbsn74f4q"   # informational_pattern_as_cosmic_dna
    ]
    
    test_context = {
        "focus_area": "metaphysics",
        "analysis_depth": "detailed",
        "test_mode": True,
        "description": "Testing philosophical analyzer with 5 core concepts"
    }
    
    try:
        results = analyze_philosophical_patterns(test_cids, test_context)
        
        print("\nTEST RESULTS SUMMARY:")
        print(f"   Success: {results.get('success', False)}")
        print(f"   Concepts analyzed: {results.get('concepts_analyzed', 0)}")
        print(f"   Connections found: {len(results.get('connections', []))}")
        print(f"   Insights generated: {len(results.get('insights', []))}")
        
        if results.get('success'):
            print("TEST PASSED - Agent is operational")
        else:
            print("TEST FAILED - Check errors above")
        
        return results
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': 'See console output',
            'metadata': {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'test_cids': len(test_cids)
            }
        }
        print(f"TEST FAILED WITH EXCEPTION: {e}")
        return error_result

# Command-line interface for direct execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Philosophical Analyzer Agent - Analyze philosophical concepts for patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--test', action='store_true', help='Run self-test with stored concepts')
    parser.add_argument('--cids', nargs='+', help='List of CIDs to analyze')
    parser.add_argument('--context', type=str, help='JSON context string')
    parser.add_argument('--depth', choices=['basic', 'detailed', 'comprehensive'], 
                       default='basic', help='Analysis depth')
    
    args = parser.parse_args()
    
    if args.test:
        # Run self-test
        results = test_agent()
        print("\n" + "=" * 50)
        print("TEST COMPLETE")
        
    elif args.cids:
        # Analyze specific CIDs
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid context JSON: {e}")
                exit(1)
        
        context['analysis_depth'] = args.depth
        
        print(f"EXECUTING AGENT WITH {len(args.cids)} CIDs")
        results = analyze_philosophical_patterns(args.cids, context)
        
        # Print summary
        print("\n" + "=" * 50)
        print("ANALYSIS SUMMARY")
        print(f"Success: {results.get('success')}")
        print(f"Concepts: {results.get('concepts_analyzed')}")
        if results.get('connections'):
            print(f"Connections found: {len(results['connections'])}")
        if results.get('insights'):
            print(f"Insights: {len(results['insights'])}")
        
        # Save results to analysis directory
        results_dir = PROJECT_ROOT / "analysis_results"
        results_dir.mkdir(exist_ok=True)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        output_file = results_dir / f"analysis_results_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {output_file}")
        
    else:
        # No arguments - show help
        parser.print_help()
        print("\nExamples:")
        print("  python philosophical_analyzer.py --test")
        print("  python philosophical_analyzer.py --cids bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji")
        print("  python philosophical_analyzer.py --cids CID1 CID2 CID3 --depth detailed")
