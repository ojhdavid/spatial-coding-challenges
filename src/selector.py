import random
from typing import List, Dict, Optional

from .loader import load_problems


def filter_problems(
    difficulty: Optional[int] = None,
    topic: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> List[Dict]:
    problems = load_problems()
    filtered: List[Dict] = []

    for p in problems:
        if difficulty is not None and p.get("difficulty") != difficulty:
            continue
        if topic is not None and p.get("topic") != topic:
            continue
        if category is not None and p.get("category") != category:
            continue
        if tags:
            p_tags = p.get("tags") or []
            if not any(tag in p_tags for tag in tags):
                continue
        filtered.append(p)

    return filtered


def choose_random_problem(
    difficulty: Optional[int] = None,
    topic: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Optional[Dict]:
    candidates = filter_problems(
        difficulty=difficulty,
        topic=topic,
        category=category,
        tags=tags,
    )
    if not candidates:
        return None
    return random.choice(candidates)
