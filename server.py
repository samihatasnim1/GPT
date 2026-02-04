import os
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from framework.backends import LlamaLocalBackend, OpenAIBackend
from framework.pipeline import run_pipeline
from framework.storage import new_run_dir, save_json
from framework.exporter import export_markdown
from framework.refine import refine_materials
load_dotenv()

app = FastAPI()

# Serve your HTML/CSS/JS from /web
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
def root():
    return FileResponse("web/index.html")

class PipelineRequest(BaseModel):
    mode: str  # "llama" or "openai"
    max_refine_iters: int = 1
    learner_profile: str
    prerequisites: str
    topic_scope: str
    learning_objectives: str
    duration_format: str
    constraints: str

class ReviewRequest(BaseModel):
    run_dir: str
    expert_name: str
    topic: str
    technical_accuracy_1to5: int
    conceptual_completeness_1to5: int
    pedagogical_clarity_1to5: int
    objective_alignment_1to5: int
    overall_quality_1to5: int
    comments: str = ""
class RefineRequest(BaseModel):
    run_dir: str
    user_comment: str
    mode: str = "openai"
    max_refine_iters: int = 1

def get_backend(mode: str):
    if mode == "llama":
        return LlamaLocalBackend(model="llama3")
    elif mode == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment/.env")
        return OpenAIBackend(api_key=api_key, model="gpt-4.1-mini")
    else:
        raise RuntimeError("Unknown mode. Use 'llama' or 'openai'.")

@app.post("/api/run")
def api_run(req: PipelineRequest):
    backend = get_backend(req.mode)

    inputs = {
        "learner_profile": req.learner_profile,
        "prerequisites": req.prerequisites,
        "topic_scope": req.topic_scope,
        "learning_objectives": req.learning_objectives,
        "duration_format": req.duration_format,
        "constraints": req.constraints,
    }

    run_dir = new_run_dir()

    blueprint, draft, final_materials, report = run_pipeline(
        inputs, backend, max_refine_iters=req.max_refine_iters
    )

    # Save artifacts
    save_json(run_dir / "inputs.json", inputs)
    save_json(run_dir / "blueprint.json", blueprint)
    save_json(run_dir / "draft.json", draft)
    save_json(run_dir / "final_materials.json", final_materials)
    save_json(run_dir / "validation_report.json", report)

    # Export markdown
    md_path = run_dir / "final_materials.md"
    export_markdown(md_path, inputs, blueprint, final_materials)

    return {
        "run_dir": str(run_dir),
        "blueprint": blueprint,
        "final_materials": final_materials,
        "report": report,
        "markdown_path": str(md_path)
    }

@app.post("/api/review")
def api_review(req: ReviewRequest):
    run_dir = Path(req.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    reviews_path = run_dir / "expert_reviews.csv"

    # Append CSV safely
    header = [
        "expert_name","topic",
        "technical_accuracy_1to5","conceptual_completeness_1to5",
        "pedagogical_clarity_1to5","objective_alignment_1to5",
        "overall_quality_1to5","comments"
    ]
    row = [
        req.expert_name, req.topic,
        req.technical_accuracy_1to5, req.conceptual_completeness_1to5,
        req.pedagogical_clarity_1to5, req.objective_alignment_1to5,
        req.overall_quality_1to5, req.comments.replace("\n"," ").strip()
    ]

    if not reviews_path.exists():
        reviews_path.write_text(",".join(header) + "\n", encoding="utf-8")

    with reviews_path.open("a", encoding="utf-8") as f:
        f.write(",".join(map(str, row)) + "\n")

    return {"ok": True, "saved_to": str(reviews_path)}
@app.post("/api/refine")
def refine(req: RefineRequest):
    run_dir = Path(req.run_dir)

    blueprint = json.loads((run_dir / "blueprint.json").read_text())
    current = json.loads((run_dir / "final_materials.json").read_text())

    backend = get_backend(req.mode)  # your existing backend selection

    updated_materials, report = refine_materials(
        blueprint, current, req.user_comment, backend, max_refine_iters=req.max_refine_iters
    )

    # overwrite outputs for the same run
    save_json(run_dir / "final_materials.json", updated_materials)
    save_json(run_dir / "validation_report.json", report)

    md_path = run_dir / "final_materials.md"
    export_markdown(md_path, json.loads((run_dir/"inputs.json").read_text()), blueprint, updated_materials)

    return {
        "run_dir": str(run_dir),
        "final_materials": updated_materials,
        "report": report,
        "markdown_path": str(md_path)
    }


