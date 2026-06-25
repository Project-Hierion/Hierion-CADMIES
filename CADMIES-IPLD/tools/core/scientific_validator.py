#!/usr/bin/env python3
"""
File: scientific_validator.py
Tool: CADMIES Scientific Validator
Version: 1.0.0
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Enforce scientific rigor before CID generation.
         The quality gatekeeper for the knowledge garden.
         No weak concepts enter the mycelium.

Usage:
    python tools/core/scientific_validator.py

Validation Levels:
    BASIC    — Required fields present
    STANDARD — Field types and constraints
    RIGOROUS — Scientific quality checks
    STRICT   — Maximum scientific rigor
"""

import json
from typing import Dict, Any, List, Tuple
from datetime import datetime

class ScientificValidator:
    """
    Validator for UniversalScientificConcept format
    
    Validation Levels:
    - BASIC: Required fields present
    - STANDARD: Field types and constraints
    - RIGOROUS: Scientific quality checks
    - STRICT: Maximum scientific rigor
    """
    
    REQUIRED_FIELDS = [
        "schema_version",
        "human_id", 
        "title",
        "definition",
        "type",
        "domain",
        "subdomain",
        "proofs",
        "metadata",
        "relationships",
        "difficulty_levels"
    ]
    
    VALID_TYPES = [
        "Law", "Theory", "Principle", "Observation", 
        "Method", "Concept", "CoreConcept", "Framework",
        "Model", "Hypothesis", "Discovery", "Invention"
    ]
    
    def __init__(self, validation_level: str = "STANDARD"):
        """Initialize validator with specified rigor level"""
        self.validation_level = validation_level.upper()
        self.validation_rules = self._get_validation_rules()
        
        print(f"Scientific Validator v1.0.0 initialized")
        print(f"   Level: {self.validation_level}")
        print(f"   Mission: Ensure only rigorous concepts enter the garden")
    
    def _get_validation_rules(self) -> Dict:
        """Get validation rules based on level"""
        rules = {
            "BASIC": {
                "description": "Minimum viable concept",
                "checks": ["required_fields", "field_types"]
            },
            "STANDARD": {
                "description": "Standard scientific entry",
                "checks": ["required_fields", "field_types", "constraints", "proof_minimum"]
            },
            "RIGOROUS": {
                "description": "High scientific quality",
                "checks": ["required_fields", "field_types", "constraints", "proof_quality", "metadata_completeness"]
            },
            "STRICT": {
                "description": "Maximum scientific rigor",
                "checks": ["required_fields", "field_types", "constraints", "proof_quality", 
                          "metadata_completeness", "definition_quality", "cross_references"]
            }
        }
        return rules.get(self.validation_level, rules["STANDARD"])
    
    def validate(self, concept: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Validate a scientific concept
        
        Returns: (is_valid, errors, validation_report)
        """
        print(f"\nValidating concept: '{concept.get('title', 'Untitled')}'")
        print(f"   Level: {self.validation_level}")
        
        errors = []
        warnings = []
        validation_report = {
            "concept_title": concept.get("title", "Unknown"),
            "human_id": concept.get("human_id", "Unknown"),
            "validation_level": self.validation_level,
            "timestamp": datetime.now().isoformat() + "Z",
            "checks_passed": [],
            "checks_failed": [],
            "warnings": [],
            "score": 0
        }
        
        for check_name in self.validation_rules["checks"]:
            check_method = getattr(self, f"_check_{check_name}", None)
            if check_method:
                check_result = check_method(concept)
                if check_result["valid"]:
                    validation_report["checks_passed"].append(check_name)
                else:
                    validation_report["checks_failed"].append(check_name)
                    errors.extend(check_result["errors"])
                
                if check_result.get("warnings"):
                    warnings.extend(check_result["warnings"])
                    validation_report["warnings"].extend(check_result["warnings"])
        
        total_checks = len(validation_report["checks_passed"]) + len(validation_report["checks_failed"])
        if total_checks > 0:
            validation_report["score"] = len(validation_report["checks_passed"]) / total_checks * 100
        
        is_valid = len(errors) == 0
        
        if is_valid:
            print(f"   VALIDATION PASSED")
            print(f"   Score: {validation_report['score']:.1f}%")
            if warnings:
                print(f"   Warnings: {len(warnings)}")
        else:
            print(f"   VALIDATION FAILED")
            print(f"   Score: {validation_report['score']:.1f}%")
            print(f"   Errors: {len(errors)}")
        
        validation_report["errors"] = errors
        validation_report["warnings"] = warnings
        
        return is_valid, errors, validation_report
    
    def _check_required_fields(self, concept: Dict) -> Dict:
        """Check all required fields are present"""
        errors = []
        for field in self.REQUIRED_FIELDS:
            if field not in concept:
                errors.append(f"Missing required field: '{field}'")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _check_field_types(self, concept: Dict) -> Dict:
        """Check field types are correct"""
        errors = []
        
        type_checks = [
            ("title", str),
            ("definition", str),
            ("type", str),
            ("domain", str),
            ("subdomain", str),
            ("proofs", list),
            ("metadata", dict),
            ("relationships", dict),
            ("difficulty_levels", dict)
        ]
        
        for field, expected_type in type_checks:
            if field in concept and not isinstance(concept[field], expected_type):
                errors.append(f"Field '{field}' should be {expected_type.__name__}, got {type(concept[field]).__name__}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _check_constraints(self, concept: Dict) -> Dict:
        """Check field constraints"""
        errors = []
        warnings = []
        
        if "title" in concept:
            title = concept["title"]
            if len(title) == 0:
                errors.append("Title cannot be empty")
            elif len(title) > 200:
                errors.append(f"Title exceeds 200 character limit ({len(title)} chars)")
            elif len(title) < 5:
                warnings.append("Title is very short (consider being more descriptive)")
        
        if "definition" in concept:
            definition = concept["definition"]
            if len(definition) < 10:
                errors.append(f"Definition must be at least 10 characters ({len(definition)} chars)")
            elif len(definition) < 20:
                warnings.append("Definition is quite short (consider expanding)")
            elif len(definition) > 5000:
                warnings.append("Definition is very long (consider splitting into multiple concepts)")
        
        if "type" in concept and concept["type"] not in self.VALID_TYPES:
            warnings.append(f"Type '{concept['type']}' not in standard types list: {self.VALID_TYPES}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _check_proof_minimum(self, concept: Dict) -> Dict:
        """Check minimum proof requirements"""
        errors = []
        
        if "proofs" in concept:
            proofs = concept["proofs"]
            if len(proofs) == 0:
                errors.append("At least one proof is required")
            else:
                for i, proof in enumerate(proofs):
                    if not isinstance(proof, dict):
                        errors.append(f"Proof {i+1} must be a dictionary")
                    elif "type" not in proof:
                        errors.append(f"Proof {i+1} missing 'type' field")
                    elif "description" not in proof:
                        errors.append(f"Proof {i+1} missing 'description' field")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _check_proof_quality(self, concept: Dict) -> Dict:
        """Check proof quality (rigorous level)"""
        warnings = []
        
        if "proofs" in concept:
            proofs = concept["proofs"]
            for i, proof in enumerate(proofs):
                confidence = proof.get("confidence")
                if confidence is not None:
                    if confidence < 0.5:
                        warnings.append(f"Proof {i+1} has low confidence ({confidence})")
                    elif confidence > 0.95:
                        warnings.append(f"Proof {i+1} has very high confidence ({confidence}) - verify")
                else:
                    warnings.append(f"Proof {i+1} missing confidence score")
                
                if "date" not in proof:
                    warnings.append(f"Proof {i+1} missing date")
                
                if "reference" not in proof:
                    warnings.append(f"Proof {i+1} missing reference/citation")
        
        return {
            "valid": True,
            "warnings": warnings
        }
    
    def _check_metadata_completeness(self, concept: Dict) -> Dict:
        """Check metadata completeness"""
        warnings = []
        
        if "metadata" in concept:
            metadata = concept["metadata"]
            required_meta = ["created", "creator", "certainty_score", "version"]
            
            for field in required_meta:
                if field not in metadata:
                    warnings.append(f"Metadata missing '{field}' field")
            
            certainty = metadata.get("certainty_score")
            if certainty is not None:
                if certainty < 0.5:
                    warnings.append(f"Low certainty score ({certainty}) - consider more evidence")
        
        return {
            "valid": True,
            "warnings": warnings
        }
    
    def _check_definition_quality(self, concept: Dict) -> Dict:
        """Check definition quality (strict level)"""
        warnings = []
        
        if "definition" in concept:
            definition = concept["definition"]
            
            if not definition.endswith(('.', '!', '?')):
                warnings.append("Definition doesn't end with proper punctuation")
            
            if len(definition) < 50:
                warnings.append("Definition may be too brief for rigorous concept")
            
            vague_terms = ["something", "stuff", "things", "maybe", "perhaps", "possibly"]
            for term in vague_terms:
                if term in definition.lower():
                    warnings.append(f"Definition contains vague term: '{term}'")
        
        return {
            "valid": True,
            "warnings": warnings
        }
    
    def _check_cross_references(self, concept: Dict) -> Dict:
        """Check for cross-references (strict level)"""
        warnings = []
        
        if "cross_references" not in concept:
            warnings.append("No cross_references field - consider adding external citations")
        else:
            refs = concept["cross_references"]
            if not isinstance(refs, dict) or len(refs) == 0:
                warnings.append("cross_references is empty - add DOI, Wikipedia, or textbook references")
        
        return {
            "valid": True,
            "warnings": warnings
        }


def test_validation():
    """Test the validator with sample concepts"""
    print("=" * 60)
    print("CADMIES SCIENTIFIC VALIDATOR v1.0.0")
    print("Quality Gatekeeper for the Knowledge Garden")
    print("=" * 60)
    
    good_concept = {
        "schema_version": "1.0.0",
        "human_id": "test_scientific_law",
        "title": "Test Scientific Law",
        "definition": "A test law for validation purposes with a complete sentence.",
        "type": "Law",
        "domain": "Physics",
        "subdomain": "Test Physics",
        "proofs": [
            {
                "type": "experimental",
                "description": "Test experiment description",
                "confidence": 0.85,
                "date": "2025-12-24",
                "reference": "Test Reference"
            }
        ],
        "metadata": {
            "created": datetime.now().isoformat() + "Z",
            "creator": "Test System",
            "certainty_score": 0.9,
            "version": 1
        },
        "relationships": {},
        "difficulty_levels": {
            "intermediate": "Intermediate explanation"
        }
    }
    
    bad_concept = {
        "human_id": "test_bad_concept",
        "title": "Bad",
        "definition": "Short",
    }
    
    for level in ["BASIC", "STANDARD", "RIGOROUS", "STRICT"]:
        print(f"\n{'='*40}")
        print(f"VALIDATION LEVEL: {level}")
        print(f"{'='*40}")
        
        validator = ScientificValidator(level)
        
        print(f"\nTesting GOOD concept:")
        valid1, errors1, report1 = validator.validate(good_concept)
        
        print(f"\nTesting BAD concept:")
        valid2, errors2, report2 = validator.validate(bad_concept)
    
    print(f"\n{'='*60}")
    print("Validation testing complete!")
    print("Ready to guard the garden from weak concepts...")

if __name__ == "__main__":
    test_validation()
