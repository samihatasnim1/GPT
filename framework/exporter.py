# framework/exporter.py
from pathlib import Path
import pypandoc

def export_markdown(out_path: Path, inputs: dict, blueprint: dict, materials: dict):
    md = []
    md.append(f"# {inputs.get('topic_scope','Course Materials')}\n")

    md.append("## Learner Profile\n")
    md.append(inputs.get("learner_profile","") + "\n")

    md.append("## Learning Objectives\n")
    for obj in blueprint.get("learning_objectives", []):
        md.append(f"- {obj}")
    md.append("")

    md.append("## Lecture Notes\n")
    for sec in materials.get("lecture_notes", []):
        md.append(f"### {sec.get('title','Section')}\n")
        md.append(sec.get("content","") + "\n")

    md.append("## Worked Examples\n")
    for ex in materials.get("worked_examples", []):
        md.append(f"### {ex.get('title','Example')}\n")

        steps = ex.get("steps", "")
        if isinstance(steps, list):
            for s in steps:
                md.append(f"- {s}")
            md.append("")  # blank line
        else:
            md.append(steps + "\n")


    md.append("## Exercises\n")
    for i, ex in enumerate(materials.get("exercises", []), start=1):
        md.append(f"### Exercise {i}: {ex.get('title','')}")
        md.append(f"**Difficulty:** {ex.get('difficulty','')}\n")
        md.append(ex.get("prompt","") + "\n")

    out_path.write_text("\n".join(md), encoding="utf-8")
def export_pdf(md_path):
    pdf_path = md_path.with_suffix(".pdf")
    pypandoc.convert_file(
        str(md_path),
        "pdf",
        outputfile=str(pdf_path),
        extra_args=["--standalone"]
    )
    return pdf_path
