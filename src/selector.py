import random
from typing import List, Dict, Optional
from .loader import load_all_problems

def filter_problems(difficulty: Optional[int] = None, topic: Optional[str] = None, tags: Optional[List[str]] = None):
    problems = load_all_problems()
    filtered = []
    for p in problems:
        if difficulty is not None and p.get("difficulty") != difficulty:
            continue
        if topic is not None and p.get("topic") != topic:
            continue
        if tags:
            if not any(tag in p.get("tags", []) for tag in tags):
                continue
        filtered.append(p)
    return filtered

def choose_random_problem(difficulty: Optional[int] = None, topic: Optional[str] = None, tags: Optional[List[str]] = None):
    candidates = filter_problems(difficulty, topic, tags)
    if not candidates:
        return None
    return random.choice(candidates)
