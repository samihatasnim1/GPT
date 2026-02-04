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
MODULE2_REFINE_PROMPT = """
You are refining existing course materials based on an instructor comment.

Goal: Apply ONLY the requested changes. Do NOT rewrite unaffected content.

Return ONLY JSON with fields:
- lecture_notes: list of {{title, content}}
- worked_examples: list of {{title, steps}}
- exercises: list of {{title, prompt, difficulty}}
- metadata: {{objective_coverage_note: string}}

Rules (STRICT):
1) Keep all existing items unchanged unless the comment requires changes.
2) If the comment says "add N examples", append N new examples ONLY.
3) If the comment says "remove X", remove ONLY that part.
4) If the comment says "edit section Y", edit ONLY that section.
5) Keep titles and numbering consistent. Do not rename existing titles unless asked.
6) Preserve style + notation.

Blueprint:
{blueprint_json}

Current materials JSON:
{current_materials_json}

Instructor comment (apply as patch):
{user_comment}

Return ONLY JSON. No markdown. No code fences.
"""
MODULE3_PROMPT = """
Validate and refine the generated materials.

Return ONLY JSON with fields:
- passed (true/false)
- checks (object with booleans):
    - objective_coverage
    - notation_consistency
    - difficulty_match
    - examples_step_by_step
    - domain_control_ok
    - domain_mechatronics_ok
    - domain_construction_ok
- issues (list of strings)
- fixes_applied (list of strings)
- revised_materials (same schema as draft materials)

Validation rules:
1) Each objective must be covered in notes AND assessed by at least one exercise.
2) Terminology/notation consistent.
3) Difficulty matches learner profile.
4) Worked examples are step-by-step.
5) Control: if control strategy mentioned, include objective + control law/structure.
6) Mechatronics: include sensor→control→actuator loop at least once.
7) Construction: include at least one construction scenario/constraint.

Blueprint:
{blueprint_json}

Draft materials:
{draft_json}

"""



