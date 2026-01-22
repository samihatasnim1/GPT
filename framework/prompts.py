# # framework/prompts.py

# MODULE1_BLUEPRINT_PROMPT = """
# You are building an instructional blueprint.

# Return ONLY valid JSON with keys:
# subtopics: list of strings (ordered)
# objectives: list of measurable learning objectives
# prereq_map: dict where each subtopic maps to a list of prerequisites
# objective_map: dict where each objective maps to:
#   subtopic, difficulty (intro/intermediate/advanced), assessment_type (exercise/quiz/short answer)

# Inputs:
# Learner profile: {learner_profile}
# Prerequisites (given): {prerequisites}
# Topic scope: {topic_scope}
# Learning objectives (if provided, use them; if empty, generate): {learning_objectives}
# Duration/format: {duration_format}
# Constraints: {constraints}
# """

# MODULE2_GENERATE_PROMPT = """
# Generate course materials from the blueprint.

# Return ONLY valid JSON with keys:
# notes: list of {{"title","content"}}
# worked_examples: list of {{"title","steps"}}
# exercises: list of {{"title","prompt","difficulty"}}
# (optional) solutions: list of {{"title","solution"}}
# metadata: {{"objective_coverage":..., "style":...}}

# Rules:
# - Simple academic tone.
# - Match learner level.
# - Keep notation consistent.
# - Cover ALL objectives.

# Blueprint JSON:
# {blueprint_json}
# """

# MODULE3_VALIDATE_REFINE_PROMPT = """
# Validate the draft materials against the blueprint and refine if needed.

# Return ONLY valid JSON with keys:
# passed: true/false
# issues: list of problems found
# fixes_applied: list of fixes made (or planned)
# revised_materials: full revised materials JSON in same format as draft

# Validation checks:
# 1) Every objective is covered in notes AND at least one exercise.
# 2) Notation/terms consistent.
# 3) Difficulty matches learner profile.
# 4) Explanations are clear (no missing steps in examples).

# Blueprint JSON:
# {blueprint_json}

# Draft Materials JSON:
# {draft_json}
# Return ONLY JSON. Do not include markdown code fences.
# """


# framework/prompts.py

MODULE1_PROMPT = """
Create an instructional blueprint.

Return ONLY JSON with fields:
- subtopics (ordered list)
- learning_objectives (list of measurable objectives)
- prerequisite_map (subtopic -> list of prerequisites)
- difficulty_map (subtopic -> intro/intermediate/advanced)

Inputs:
Learner profile: {learner_profile}
Prerequisites (given): {prerequisites}
Topic scope: {topic_scope}
Learning objectives (if empty, generate): {learning_objectives}
Duration/format: {duration_format}
Constraints: {constraints}
"""

MODULE2_PROMPT = """
Generate course materials from the instructional blueprint.

Return ONLY JSON with fields:
- lecture_notes: list of {{title, content}}
- worked_examples: list of {{title, steps}}
- exercises: list of {{title, prompt, difficulty}}
- metadata: {{objective_coverage_note: string}}

Rules:
- Simple academic tone
- Match learner level
- Keep notation consistent
- Cover all learning objectives

Blueprint:
{blueprint_json}
"""

MODULE3_PROMPT = """
Validate and refine the generated materials.

Return ONLY JSON with fields:
- passed (true/false)
- issues (list of strings)
- fixes_applied (list of strings)
- revised_materials (same schema as draft materials)

Validation rules:
1) Each objective must be covered in notes AND assessed by at least one exercise.
2) Terminology/notation consistent.
3) Difficulty matches learner profile.
4) Explanations are clear (worked examples are step-by-step).

Blueprint:
{blueprint_json}

Draft materials:
{draft_json}
"""
