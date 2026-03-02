from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Literal, List, Dict, Any
import re

# Match your existing schema types from UniversalScientificConcept v1.0.0
ConceptType = Literal[
    "MetaphysicalPrinciple",
    "PhilosophicalHypothesis", 
    "PhilosophicalTheory",
    "MechanisticPrinciple",
    "MetaphysicalConcept",
    "TestConcept",
    "ScientificLaw"
]

Domain = Literal[
    "Metaphysics",
    "SystemsTheory",
    "InformationTheory",
    "ConsciousnessStudies",
    "Testing",
    "Physics",
    "Quantum"
]

class Concept(BaseModel):
    """Matches UniversalScientificConcept schema v1.0.0 for CID generator"""
    name: str = Field(..., min_length=1, max_length=100)
    concept_type: ConceptType
    domain: Domain
    subdomain: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=10)
    file_path: Optional[str] = None
    cid: Optional[str] = None
    date_added: datetime = datetime.now()
    
    # Optional fields for richer concepts
    formula: Optional[str] = None
    proofs: List[Dict[str, Any]] = []
    cross_references: Dict[str, str] = {}
    relationships: Dict[str, List[str]] = {}
    difficulty_levels: Dict[str, str] = {}
    learning_path: Dict[str, List[str]] = {}
    extra_fields: Dict[str, Any] = {}
    
    @validator('name')
    def name_must_be_valid(cls, v):
        """Convert to human_id format (lowercase with underscores)"""
        cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', v)
        cleaned = cleaned.lower().replace(' ', '_')
        if len(cleaned) < 3:
            raise ValueError('Name too short after cleaning')
        return cleaned
    
    def to_json(self) -> Dict[str, Any]:
        """Format for cid_generator - matches UniversalScientificConcept schema"""
        return {
            "schema_version": "1.0.0",
            "human_id": self.name,
            "title": self.name.replace('_', ' ').title(),
            "definition": self.description,
            "type": self.concept_type,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "formula": self.formula or "",
            "proofs": self.proofs or [],
            "cross_references": self.cross_references or {},
            "metadata": {
                "created": self.date_added.isoformat() + "Z",
                "creator": "CADMIES GUI v1.0",
                "certainty_score": 0.95,
                "version": 1,
                "supersedes": None,
                "superseded_by": None
            },
            "relationships": self.relationships or {
                "builds_upon": [],
                "contradicts": [],
                "related_to": [],
                "specializes": []
            },
            "difficulty_levels": self.difficulty_levels or {
                "beginner": self.description[:100] + "...",
                "intermediate": self.description,
                "expert": self.description + " (advanced)"
            },
            "learning_path": self.learning_path or {
                "prerequisites": [],
                "next_steps": []
            },
            "extra_fields": self.extra_fields or {}
        }
    
    class Config:
        schema_extra = {
            "example": {
                "name": "fractal_reality_principle",
                "concept_type": "MetaphysicalPrinciple",
                "domain": "Metaphysics",
                "subdomain": "Philosophy of Science",
                "description": "Reality exhibits fractal patterns at all scales..."
            }
        }
