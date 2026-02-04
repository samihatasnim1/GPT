import json
from .prompts import MODULE2_REFINE_PROMPT, MODULE3_PROMPT

def refine_materials(blueprint: dict, current_materials: dict, user_comment: str, backend, max_refine_iters: int = 1):
    # Module 2 (patch)
    updated = backend.call(MODULE2_REFINE_PROMPT.format(
        blueprint_json=json.dumps(blueprint, indent=2),
        current_materials_json=json.dumps(current_materials, indent=2),
        user_comment=user_comment
    ))

    # Module 3 validate + optional loop
    materials = updated
    report = {"iterations": 0, "passed": False, "checks": {}, "issues": [], "fixes_applied": []}

    for i in range(max_refine_iters + 1):
        report["iterations"] = i
        val = backend.call(MODULE3_PROMPT.format(
            blueprint_json=json.dumps(blueprint, indent=2),
            draft_json=json.dumps(materials, indent=2),
        ))

        report["passed"] = bool(val.get("passed", False))
        report["checks"] = val.get("checks", {})
        report["issues"] = val.get("issues", [])
        report["fixes_applied"] = val.get("fixes_applied", [])
        materials = val.get("revised_materials", materials)

        if report["passed"]:
            break

    return materials, report
