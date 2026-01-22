# framework/validators.py
from typing import Dict, List, Tuple

def objective_coverage_check(blueprint: Dict, draft: Dict) -> Tuple[bool, List[str]]:
    objectives = blueprint.get("objectives", [])
    notes_text = " ".join([n.get("content", "") for n in draft.get("notes", [])]).lower()
    exercises_text = " ".join([e.get("prompt", "") for e in draft.get("exercises", [])]).lower()

    issues = []
    for obj in objectives:
        key = obj.lower()
        # simple heuristic: objective phrase (or key words) should appear
        # you can replace this later with better matching
        if key[:25] not in notes_text:  # rough check
            issues.append(f"Objective not clearly covered in notes: {obj}")
        if key[:25] not in exercises_text:
            issues.append(f"Objective not assessed in exercises: {obj}")

    return (len(issues) == 0), issues

def basic_format_check(draft: Dict) -> Tuple[bool, List[str]]:
    issues = []
    if not draft.get("notes"):
        issues.append("No lecture notes generated.")
    if not draft.get("worked_examples"):
        issues.append("No worked examples generated.")
    if not draft.get("exercises"):
        issues.append("No exercises generated.")
    return (len(issues) == 0), issues
