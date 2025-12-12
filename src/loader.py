import os
import yaml
from typing import List, Dict

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), "..", "problems")

def load_all_problems() -> List[Dict]:
    problems = []
    for fname in os.listdir(PROBLEMS_DIR):
        if fname.endswith(".yaml"):
            path = os.path.join(PROBLEMS_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or []
                problems.extend(data)
    return problems
