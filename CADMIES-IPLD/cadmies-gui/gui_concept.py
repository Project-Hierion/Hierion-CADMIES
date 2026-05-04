from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import re

class Concept(BaseModel):
    """Matches UniversalScientificConcept schema v1.0.0 for CID generator"""
    
    # === REQUIRED FIELDS ===
    name: str = Field(..., min_length=1, max_length=100)
    concept_type: str = Field(..., min_length=1)
    domain: str = Field(..., min_length=1)
    subdomain: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=10)
    
    # === OPTIONAL ENRICHMENT FIELDS ===
    axioms: Optional[List[str]] = None
    poetic_version: Optional[str] = None
    mantra: Optional[str] = None
    
    # === OPTIONAL RELATIONSHIP FIELDS ===
    builds_upon: Optional[List[str]] = None
    related_to: Optional[List[str]] = None
    contradicts: Optional[List[str]] = None
    
    # === OPTIONAL METADATA FIELDS ===
    certainty_score: Optional[float] = 0.8
    purpose: Optional[str] = "educational"
    genesis: Optional[str] = None
    
    # === OPTIONAL DIFFICULTY LEVELS ===
    difficulty_levels: Optional[Dict[str, str]] = None
    
    # === SYSTEM FIELDS ===
    file_path: Optional[str] = None
    cid: Optional[str] = None
    date_added: datetime = datetime.now()
    
    # Legacy compatibility
    formula: Optional[str] = None
    proofs: List[Dict[str, Any]] = []
    cross_references: Dict[str, str] = {}
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
        """Format for cid_generator - matches UniversalScientificConcept schema v2.0.1"""
        output = {
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
                "creator": "CADMIES GUI v1.1",
                "certainty_score": self.certainty_score or 0.8,
                "version": 1,
                "license": "CC BY-SA 4.0",
                "purpose": self.purpose or "educational",
                "supersedes": None,
                "superseded_by": None
            },
            "relationships": {
                "builds_upon": self.builds_upon or [],
                "contradicts": self.contradicts or [],
                "related_to": self.related_to or [],
                "specializes": []
            },
            "difficulty_levels": self.difficulty_levels or {
                "beginner": f"{self.description[:100]}...",
                "intermediate": self.description,
                "expert": f"{self.description} (awaiting expert elaboration)"
            },
            "learning_path": self.learning_path or {
                "prerequisites": [],
                "next_steps": []
            },
            "extra_fields": self.extra_fields or {}
        }
        
        # Add enrichment fields if provided
        if self.axioms:
            output["axioms"] = self.axioms
        if self.poetic_version:
            output["poetic_version"] = self.poetic_version
        if self.mantra:
            output["mantra"] = self.mantra
        if self.genesis:
            output["metadata"]["genesis"] = self.genesis
            
        return output
    
    class Config:
        schema_extra = {
            "example": {
                "name": "fractal_reality_principle",
                "concept_type": "MetaphysicalPrinciple",
                "domain": "Metaphysics",
                "subdomain": "Philosophy of Science",
                "description": "Reality exhibits fractal patterns at all scales...",
                "axioms": ["Patterns repeat across scales.", "Self-similarity is a fundamental property."],
                "poetic_version": "The whole in the part, the part in the whole.",
                "mantra": "As above, so below."
            }
        }
