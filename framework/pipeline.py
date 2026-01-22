# framework/pipeline.py
import json
from .prompts import MODULE1_PROMPT, MODULE2_PROMPT, MODULE3_PROMPT

def run_pipeline(inputs: dict, backend, max_refine_iters: int = 2):
    # Module 1
    blueprint = backend.call(MODULE1_PROMPT.format(**inputs))

    # Module 2
    draft = backend.call(MODULE2_PROMPT.format(
        blueprint_json=json.dumps(blueprint, indent=2)
    ))
    

    # Module 3 (validate + refine loop)

    materials = draft
    report = {"iterations": 0, "passed": False, "issues": [], "fixes_applied": []}

    for i in range(max_refine_iters + 1):
        report["iterations"] = i
        val = backend.call(MODULE3_PROMPT.format(
            blueprint_json=json.dumps(blueprint, indent=2),
            draft_json=json.dumps(materials, indent=2),
        ))
        report["passed"] = bool(val.get("passed", False))
        report["issues"] = val.get("issues", [])
        report["fixes_applied"] = val.get("fixes_applied", [])
        materials = val.get("revised_materials", materials)

        if report["passed"]:
            break

    return blueprint, draft, materials, report
