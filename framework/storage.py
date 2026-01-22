# framework/storage.py
import json
from pathlib import Path
from datetime import datetime

BASE = Path("outputs")
RUNS = BASE / "runs"
RUNS.mkdir(parents=True, exist_ok=True)

def new_run_dir() -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    d = RUNS / ts
    d.mkdir(parents=True, exist_ok=True)
    return d

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
