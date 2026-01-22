# framework/review.py
import pandas as pd
from pathlib import Path

RUBRIC_FIELDS = [
    "expert_name",
    "topic",
    "technical_accuracy_1to5",
    "conceptual_completeness_1to5",
    "pedagogical_clarity_1to5",
    "objective_alignment_1to5",
    "overall_quality_1to5",
    "comments"
]

def save_review_csv(out_path: Path, rows: list[dict]):
    df = pd.DataFrame(rows, columns=RUBRIC_FIELDS)
    df.to_csv(out_path, index=False)
    return df
