# framework/schemas.py
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any

@dataclass
class Inputs:
    learner_profile: str
    prerequisites: str
    topic_scope: str
    learning_objectives: str  # can be empty => system generates
    duration_format: str      # e.g., "1 lecture (60 min), notes+examples+exercises"
    constraints: str          # e.g., "2 pages notes, simple academic tone"

@dataclass
class Blueprint:
    subtopics: List[str]
    objectives: List[str]
    prereq_map: Dict[str, List[str]]        # subtopic -> prerequisites
    objective_map: Dict[str, Dict[str, Any]] # objective -> {subtopic, difficulty, assessment_type}

@dataclass
class DraftMaterials:
    notes: List[Dict[str, str]]          # [{title, content}]
    worked_examples: List[Dict[str, str]]# [{title, steps}]
    exercises: List[Dict[str, str]]      # [{title, prompt, difficulty}]
    solutions: Optional[List[Dict[str, str]]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ValidationReport:
    passed: bool
    issues: List[str]
    fixes_applied: List[str]
    iterations: int
