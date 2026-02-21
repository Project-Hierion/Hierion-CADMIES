#!/usr/bin/env python3
# ============================================================================
# MODULE METADATA
# ============================================================================
__version__ = "1.0.0"
__author__ = "Project Hieros - CADMIES-IPLD Research Group"
__created__ = "2026-01-07"
__status__ = "Public Release"
__license__ = "AGPLv3 with Commons Clause"
# ============================================================================

"""
AGPLv3 with Commons Clause

This software is free to use for:
- Individual learning and research
- Academic institutions
- Non-profit organizations
- Open source projects
- Personal knowledge management

This software may NOT be used for:
- Commercial SaaS offerings without contributing back
- Proprietary AI training without reciprocity
- Commercial products that don't share improvements

Commons Clause Condition:
The license granted under the AGPLv3 is hereby limited to exclude the right
to sell the Software, or products that include the Software, without the
express permission of the copyright holders.

For commercial licensing or permission, contact: hieroscadmies@proton.me

Copyright (c) 2026 Project Hieros - CADMIES-IPLD Research Group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

File: cbor_reader.py
Description: CBOR Reader for IPLD-based knowledge retrieval
Version: 1.0.0
System: CADMIES-IPLD Scientific Concept Tools
Purpose: Diminishing human ignorance through accessible knowledge retrieval
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Try to import dag-cbor (same as cid_generator.py)
try:
    import dag_cbor
    DAG_CBOR_AVAILABLE = True
except ImportError:
    DAG_CBOR_AVAILABLE = False
    print("ERROR: dag-cbor library not available. Required for CBOR decoding.")
    print("Install with: pip install dag-cbor")
    sys.exit(1)

class CBORReader:
    """
    CBOR Reader for Universal Scientific Concept Schema
    
    Reads CIDs and human-readable concepts from IPLD/DAG-CBOR blockstore.
    Compatible with universal_scientific_concept_schema_v1.0.0.json
    
    Philosophy: Knowledge retrieval should be as reliable as knowledge storage.
    Content-addressing ensures identical understanding across systems.
    """
    
    # Schema reference
    SCHEMA_NAME = "universal_scientific_concept_schema_v1.0.0.json"
    SCHEMA_VERSION = "1.0.0"
    
    def __init__(self, blocks_dir="./blocks", index_dir="./index", logs_dir="./logs"):
        """Initialize with configurable paths for knowledge storage."""
        self.version = "1.0.0"
        self.blocks_dir = Path(blocks_dir)
        self.index_file = Path(index_dir) / "human_id_to_cid.json"
        self.logs_dir = Path(logs_dir)
        
        # Create directories if they don't exist
        self.blocks_dir.mkdir(exist_ok=True)
        self.index_file.parent.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def validate_cid(self, cid: str) -> bool:
        """Validate CID format (basic check for educational purposes)."""
        # Basic CID validation - should start with bafy and be 59+ characters for SHA2-256
        return cid.startswith('bafy') and len(cid) >= 59
    
    def load_index(self) -> dict:
        """Load human_id to CID index for knowledge lookup."""
        if not self.index_file.exists():
            print(f"INFO: Index file not found, creating empty index: {self.index_file}")
            return {}
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in index file: {e}")
            print(f"Consider recreating index using cid_generator.py")
            sys.exit(3)
    
    def cid_from_human_id(self, human_id: str, index: dict) -> str:
        """Get CID from human_id using index for educational retrieval."""
        if human_id not in index:
            print(f"ERROR: human_id '{human_id}' not found in index")
            if index:
                print(f"Available human_ids (first 10): {', '.join(sorted(index.keys())[:10])}")
            else:
                print("Index is empty. Use cid_generator.py to create educational entries.")
            sys.exit(1)
        return index[human_id]
    
    def read_cbor_file(self, cid: str) -> dict:
        """Read and decode CBOR file containing knowledge concept."""
        cbor_file = self.blocks_dir / f"{cid}.cbor"
        
        if not cbor_file.exists():
            print(f"ERROR: Knowledge block not found: {cbor_file}")
            available_blocks = len(list(self.blocks_dir.glob('*.cbor')))
            print(f"Available knowledge blocks: {available_blocks}")
            
            if available_blocks > 0:
                print("Sample blocks (first 5):")
                for i, block in enumerate(list(self.blocks_dir.glob('*.cbor'))[:5]):
                    print(f"  {i+1}. {block.stem[:20]}...")
            
            sys.exit(1)
        
        try:
            with open(cbor_file, 'rb') as f:
                cbor_data = f.read()
            
            # Decode DAG-CBOR
            decoded = dag_cbor.decode(cbor_data)
            return decoded
        except Exception as e:
            print(f"ERROR: Failed to decode knowledge block: {e}")
            print(f"This may indicate corrupted data or format mismatch")
            sys.exit(4)
    
    def describe_schema_compliance(self, concept: dict) -> str:
        """Describe how this concept complies with the universal scientific schema."""
        schema_info = []
        
        schema_info.append("📋 SCHEMA COMPLIANCE:")
        schema_info.append(f"  Schema: {self.SCHEMA_NAME}")
        schema_info.append(f"  Version: {self.SCHEMA_VERSION}")
        schema_info.append("  Purpose: Standardized representation of educational concepts")
        
        # Check required schema fields
        required_fields = [
            "schema_version", "human_id", "title", "definition", 
            "type", "domain", "metadata"
        ]
        
        present_required = [f for f in required_fields if f in concept]
        schema_info.append(f"  Required Fields: {len(present_required)}/{len(required_fields)} present")
        
        if 'schema_version' in concept:
            schema_info.append(f"  Concept Schema Version: {concept['schema_version']}")
        
        # Check metadata requirements
        if 'metadata' in concept:
            meta = concept['metadata']
            meta_required = ["created", "creator", "certainty_score", "version"]
            present_meta = [f for f in meta_required if f in meta]
            schema_info.append(f"  Metadata Fields: {len(present_meta)}/{len(meta_required)} present")
        
        # Educational purpose check
        if 'metadata' in concept and 'purpose' in concept['metadata']:
            purpose = concept['metadata']['purpose']
            valid_purposes = ["educational", "research", "personal_knowledge"]
            if purpose in valid_purposes:
                schema_info.append(f"  Purpose: {purpose} ✓ (valid educational use)")
            else:
                schema_info.append(f"  Purpose: {purpose} ⚠️ (check alignment with knowledge sharing ethics)")
        
        # License information
        if 'metadata' in concept and 'license' in concept['metadata']:
            license_info = concept['metadata']['license']
            schema_info.append(f"  License: {license_info}")
        
        return "\n".join(schema_info)
    
    def format_concept(self, concept: dict, cid: str, verbose: bool = False) -> str:
        """Format knowledge concept for human-readable educational display."""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append(f"KNOWLEDGE CONCEPT")
        output.append(f"Title: {concept.get('title', 'Educational Concept')}")
        output.append(f"CID: {cid}")
        output.append(f"Human ID: {concept.get('human_id', 'Not specified')}")
        output.append("-" * 80)
        
        # Schema compliance information (when verbose)
        if verbose:
            output.append("\n" + self.describe_schema_compliance(concept))
            output.append("-" * 80)
        
        # Core concept information
        output.append("\nCORE INFORMATION:")
        output.append(f"  Type: {concept.get('type', 'Educational Content')}")
        output.append(f"  Domain: {concept.get('domain', 'General Knowledge')}")
        
        if 'subdomain' in concept and concept['subdomain']:
            output.append(f"  Subdomain: {concept['subdomain']}")
        
        # Definition with wrapping for readability
        output.append(f"\n  Definition:")
        definition = concept.get('definition', 'No definition provided')
        
        # Simple text wrapping for educational display
        import textwrap
        wrapped_def = textwrap.fill(definition, width=76, subsequent_indent='    ')
        output.append(f"    {wrapped_def}")
        
        # Expert level explanation (most detailed educational content)
        if 'difficulty_levels' in concept and 'expert' in concept['difficulty_levels']:
            output.append(f"\n  Expert Level Explanation:")
            expert = concept['difficulty_levels']['expert']
            wrapped_expert = textwrap.fill(expert, width=76, subsequent_indent='    ')
            output.append(f"    {wrapped_expert}")
        
        # Metadata with educational context
        output.append("\nMETADATA:")
        metadata = concept.get('metadata', {})
        
        if 'created' in metadata:
            output.append(f"  Created: {metadata['created']}")
        
        if 'creator' in metadata:
            output.append(f"  Creator: {metadata['creator']}")
        
        if 'certainty_score' in metadata:
            score = metadata['certainty_score']
            if isinstance(score, (int, float)):
                percentage = int(score * 100)
                confidence = "High" if percentage >= 80 else "Medium" if percentage >= 50 else "Low"
                output.append(f"  Certainty: {percentage}% ({confidence} confidence)")
            else:
                output.append(f"  Certainty: {score}")
        
        if 'version' in metadata:
            output.append(f"  Version: {metadata['version']}")
        
        if 'license' in metadata:
            output.append(f"  License: {metadata['license']}")
        
        if 'purpose' in metadata:
            output.append(f"  Purpose: {metadata['purpose']}")
        
        # Educational relationships
        relationships = concept.get('relationships', {})
        if any(relationships.values()):
            output.append("\nEDUCATIONAL RELATIONSHIPS:")
            for rel_type, rel_list in relationships.items():
                if rel_list:
                    # Format for educational display
                    rel_type_formatted = rel_type.replace('_', ' ').title()
                    output.append(f"  {rel_type_formatted}: {', '.join(rel_list[:5])}")
                    if len(rel_list) > 5:
                        output.append(f"    ... and {len(rel_list) - 5} more")
        
        # Proofs and evidence (for scientific/educational credibility)
        proofs = concept.get('proofs', [])
        if proofs:
            output.append(f"\nEVIDENCE & PROOFS ({len(proofs)} sources):")
            for i, proof in enumerate(proofs[:3], 1):  # Show first 3 for brevity
                proof_type = proof.get('type', 'unknown').title()
                confidence = proof.get('confidence', 0)
                output.append(f"  {i}. {proof_type} evidence (confidence: {confidence})")
            
            if len(proofs) > 3:
                output.append(f"  ... plus {len(proofs) - 3} additional sources")
        
        # Learning path for educational context
        if 'learning_path' in concept:
            learning = concept['learning_path']
            if 'prerequisites' in learning and learning['prerequisites']:
                output.append(f"\nPREREQUISITES FOR LEARNING:")
                output.append(f"  {', '.join(learning['prerequisites'][:5])}")
                if len(learning['prerequisites']) > 5:
                    output.append(f"  ... and {len(learning['prerequisites']) - 5} more")
        
        # Note about extra educational content
        if 'extra_fields' in concept and concept['extra_fields']:
            extra_count = len(concept['extra_fields'])
            output.append(f"\nADDITIONAL EDUCATIONAL CONTENT: {extra_count} fields")
            # Show a sample of extra fields for educational context
            extra_samples = list(concept['extra_fields'].items())[:3]
            for key, value in extra_samples:
                output.append(f"  • {key}: {str(value)[:40]}{'...' if len(str(value)) > 40 else ''}")
        
        # Schema reference
        output.append("\n" + "-" * 80)
        output.append(f"SCHEMA REFERENCE: This concept follows {self.SCHEMA_NAME}")
        output.append("ETHICAL USE: Knowledge shared for educational purposes under AGPLv3 + Commons Clause")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def list_all_blocks(self, index: dict, verbose: bool = False) -> str:
        """List all knowledge blocks in the system for educational overview."""
        output = []
        
        # Get actual files
        cbor_files = list(self.blocks_dir.glob("*.cbor"))
        total_files = len(cbor_files)
        
        output.append("=" * 80)
        output.append(f"IPLD KNOWLEDGE STORE INVENTORY")
        output.append(f"Schema: {self.SCHEMA_NAME}")
        output.append(f"Location: {self.blocks_dir}")
        output.append(f"Total knowledge blocks: {total_files}")
        output.append(f"Indexed concepts: {len(index)}")
        output.append("-" * 80)
        
        if total_files == 0:
            output.append("No knowledge blocks found.")
            output.append("Use cid_generator.py to create educational concepts.")
            output.append("=" * 80)
            return "\n".join(output)
        
        # Group blocks for educational display
        known_blocks = []
        unknown_blocks = []
        
        # Reverse index: CID -> human_id
        reverse_index = {cid: human_id for human_id, cid in index.items()}
        
        for cbor_file in sorted(cbor_files):
            cid = cbor_file.stem  # Remove .cbor extension
            
            if cid in reverse_index:
                human_id = reverse_index[cid]
                # Try to read title for display
                try:
                    concept = self.read_cbor_file(cid)
                    title = concept.get('title', 'Untitled Concept')
                    concept_type = concept.get('type', 'Unknown')
                    domain = concept.get('domain', 'Unknown')
                    known_blocks.append((cid, human_id, title, concept_type, domain))
                except:
                    known_blocks.append((cid, human_id, "Error reading block", "Unknown", "Unknown"))
            else:
                unknown_blocks.append(cid)
        
        # Output known educational concepts
        if known_blocks:
            output.append("\nINDEXED EDUCATIONAL CONCEPTS:")
            for i, (cid, human_id, title, concept_type, domain) in enumerate(known_blocks, 1):
                short_cid = cid[:16] + "..." if len(cid) > 20 else cid
                output.append(f"  {i:2d}. {title[:50]}{'...' if len(title) > 50 else ''}")
                output.append(f"       ID: {human_id}")
                output.append(f"       Type: {concept_type}, Domain: {domain}")
                output.append(f"       CID: {short_cid}")
                if i < len(known_blocks):  # Add spacing between items
                    output.append("")
        
        # Output unknown blocks (orphaned data)
        if unknown_blocks:
            output.append(f"\nUNINDEXED BLOCKS ({len(unknown_blocks)} not in index):")
            output.append("These blocks exist but aren't in the human-readable index.")
            for i, cid in enumerate(unknown_blocks[:5], 1):  # Show first 5
                short_cid = cid[:16] + "..." if len(cid) > 20 else cid
                output.append(f"  {i:2d}. {short_cid}")
            
            if len(unknown_blocks) > 5:
                output.append(f"  ... and {len(unknown_blocks) - 5} more")
        
        # Educational statistics
        output.append("\n" + "-" * 80)
        output.append("KNOWLEDGE BASE STATISTICS:")
        
        if known_blocks:
            # Group by domain for educational analysis
            domains = {}
            for _, _, _, _, domain in known_blocks:
                domains[domain] = domains.get(domain, 0) + 1
            
            output.append(f"  Concepts by Domain:")
            for domain, count in sorted(domains.items()):
                output.append(f"    • {domain}: {count} concepts")
        
        # Schema compliance note
        output.append(f"\n  Schema Compliance:")
        output.append(f"    • Using: {self.SCHEMA_NAME}")
        output.append(f"    • All blocks compatible with universal scientific concept schema")
        
        # File size analysis for educational context
        if verbose and total_files > 0:
            total_size = sum(f.stat().st_size for f in cbor_files)
            avg_size = total_size / total_files
            
            output.append(f"\n  Storage Analysis:")
            output.append(f"    Total: {total_size:,} bytes ({total_size/1024:.1f} KB)")
            output.append(f"    Average per concept: {avg_size:.0f} bytes")
            output.append(f"    Blocks directory: {self.blocks_dir.absolute()}")
        
        output.append("\nEDUCATIONAL NOTE: This system demonstrates content-addressed")
        output.append("knowledge storage. Each CID uniquely identifies specific understanding.")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def log_retrieval(self, identifier: str, cid: str, success: bool):
        """Log knowledge retrieval for educational auditing."""
        log_file = self.logs_dir / "knowledge_retrieval.jsonl"
        
        log_entry = {
            "timestamp": datetime.now().isoformat() + "Z",
            "operation": "knowledge_retrieval",
            "tool_version": self.version,
            "identifier": identifier,
            "cid": cid,
            "success": success,
            "blocks_dir": str(self.blocks_dir.absolute()),
            "schema": self.SCHEMA_NAME,
            "purpose": "educational_access"
        }
        
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except:
            pass  # Logging is optional for educational use


def main():
    """Main function with command-line argument parsing for educational retrieval."""
    parser = argparse.ArgumentParser(
        description="IPLD CBOR Reader v1.0.0 - Retrieve knowledge concepts by CID or human ID",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
ETHICAL USE STATEMENT:
This tool retrieves knowledge shared for educational purposes.
Commercial use requires contributing back to the commons.

Schema: universal_scientific_concept_schema_v1.0.0.json

Examples:
  %(prog)s bafyreifh5f5i6elunhcqfuw7n2t3c2rl4z6jtv76rz4wm2kz2q7bj7gnji  # By CID
  %(prog)s Physics:Law/ConservationOfEnergy  # By human ID
  %(prog)s --list                            # List all knowledge blocks
  %(prog)s --list --verbose                  # Detailed list
  %(prog)s --blocks-dir ./my-knowledge       # Custom blocks directory
  %(prog)s --version                         # Show version info
  
Requirements: dag-cbor package
Install: pip install dag-cbor
        """
    )
    
    parser.add_argument(
        'identifier',
        nargs='?',
        help='CID or human_id of knowledge concept to retrieve'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all knowledge blocks in the system'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed information including schema compliance'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--blocks-dir',
        type=str,
        default="./blocks",
        help='Directory containing knowledge blocks (default: ./blocks)'
    )
    
    parser.add_argument(
        '--index-dir',
        type=str,
        default="./index",
        help='Directory containing index files (default: ./index)'
    )
    
    parser.add_argument(
        '--logs-dir',
        type=str,
        default="./logs",
        help='Directory for operation logs (default: ./logs)'
    )
    
    args = parser.parse_args()
    
    # Initialize reader with configurable paths
    reader = CBORReader(
        blocks_dir=args.blocks_dir,
        index_dir=args.index_dir,
        logs_dir=args.logs_dir
    )
    
    print("=" * 70)
    print("IPLD CBOR READER v1.0.0")
    print("Content-Addressed Knowledge Retrieval")
    print("Schema: universal_scientific_concept_schema_v1.0.0.json")
    print("License: AGPLv3 with Commons Clause")
    print("=" * 70)
    
    # Show version
    if args.version:
        print(f"\nVersion: {reader.version}")
        print(f"Author: {__author__}")
        print(f"Created: {__created__}")
        print(f"License: {__license__}")
        print(f"Schema: {reader.SCHEMA_NAME}")
        print(f"Blocks Directory: {reader.blocks_dir.absolute()}")
        
        cbor_files = list(reader.blocks_dir.glob("*.cbor"))
        print(f"Knowledge Blocks Found: {len(cbor_files)}")
        sys.exit(0)
    
    # Load index for lookups and listing
    try:
        index = reader.load_index()
    except SystemExit:
        # load_index already printed error and exited
        return
    
    # Handle --list option
    if args.list:
        print(reader.list_all_blocks(index, args.verbose))
        
        if args.verbose and index:
            print(f"\n📊 SCHEMA COMPLIANCE SUMMARY:")
            print(f"  Total indexed concepts: {len(index)}")
            print(f"  Schema: {reader.SCHEMA_NAME}")
            
            # Sample educational concepts from index
            print(f"  Sample concepts (first 5):")
            for i, (human_id, cid) in enumerate(list(index.items())[:5], 1):
                short_cid = cid[:16] + "..." if len(cid) > 20 else cid
                print(f"    {i}. {human_id}")
                print(f"       → {short_cid}")
        
        sys.exit(0)
    
    # Handle knowledge retrieval
    if not args.identifier:
        parser.print_help()
        print(f"\nERROR: No identifier provided.")
        print(f"Provide a CID or human_id, or use --list to see available concepts.")
        
        if index:
            print(f"\nAvailable educational concepts (first 5):")
            for i, (human_id, cid) in enumerate(list(index.items())[:5], 1):
                print(f"  {i}. {human_id}")
        else:
            print(f"\nNo concepts indexed yet. Use cid_generator.py to create knowledge.")
        
        sys.exit(10)
    
    identifier = args.identifier
    
    # Determine if identifier is CID or human_id
    if reader.validate_cid(identifier):
        # It's a CID
        cid = identifier
        id_type = "CID"
    else:
        # Assume it's a human_id, look up CID
        try:
            cid = reader.cid_from_human_id(identifier, index)
            id_type = "human_id"
        except SystemExit:
            # cid_from_human_id already printed error and exited
            reader.log_retrieval(identifier, "unknown", False)
            return
    
    # Read and display the knowledge concept
    try:
        concept = reader.read_cbor_file(cid)
        print(reader.format_concept(concept, cid, args.verbose))
        
        # Log successful retrieval
        reader.log_retrieval(identifier, cid, True)
        
        # Educational summary
        print(f"\n📋 RETRIEVAL SUMMARY:")
        print(f"   Retrieved via: {id_type} ('{identifier}')")
        print(f"   Content ID: {cid}")
        print(f"   Title: {concept.get('title', 'Unknown')}")
        print(f"   Schema: {reader.SCHEMA_NAME}")
        
        if 'metadata' in concept:
            metadata = concept['metadata']
            if 'purpose' in metadata:
                print(f"   Purpose: {metadata['purpose']}")
            if 'license' in metadata:
                print(f"   License: {metadata['license']}")
        
        print(f"\n✅ Knowledge retrieved successfully!")
        print(f"   This content will always be accessible via this CID.")
        print(f"   Shared understanding → diminished ignorance")
        
    except SystemExit:
        # read_cbor_file already printed error and exited
        reader.log_retrieval(identifier, cid, False)
        return
    
    # Reminder about ethical use
    print(f"\n📜 ETHICAL REMINDER:")
    print(f"   Retrieved knowledge is licensed as indicated above.")
    print(f"   Educational and research use is encouraged.")
    print(f"   Commercial use requires permission (Commons Clause).")
    print(f"   Contact: hieroscadmies@proton.me")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
