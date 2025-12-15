import argparse
import os
import time

from .selector import choose_random_problem


SOLUTIONS_DIR = "solutions"


def countdown(minutes: int):
    total = minutes * 60
    print("\n⏳ Timer started (Ctrl+C to stop)\n")
    try:
        while total > 0:
            m, s = divmod(total, 60)
            print(f"\rRemaining: {m:02d}:{s:02d}", end="")
            time.sleep(1)
            total -= 1
        print("\n⏰ Time's up!")
    except KeyboardInterrupt:
        print("\n⏹ Timer stopped manually.")


def solution_stub(problem: dict) -> str:
    pid = problem.get("id", "UNKNOWN")
    title = problem.get("title", "")
    category = problem.get("category", "")
    topic = problem.get("topic", "")
    tags = ", ".join(problem.get("tags") or [])
    desc = (problem.get("description", "") or "").strip()

    suggested_imports = []
    if category == "pandas" or topic == "pandas":
        suggested_imports = ["import pandas as pd"]
    elif category in ("single_cell", "spatial") or topic in ("scanpy", "squidpy"):
        suggested_imports = ["import scanpy as sc"]
        if topic == "squidpy":
            suggested_imports.append("import squidpy as sq")
    else:
        suggested_imports = ["# import needed modules"]

    header = f'''"""
{pid}: {title}

Category: {category}
Topic: {topic}
Tags: {tags}

Task:
{desc}
"""

'''
    body = "\n".join(suggested_imports) + "\n\n\n" + \
           "def main():\n" + \
           "    # TODO: implement your solution\n" + \
           "    pass\n\n\n" + \
           "if __name__ == '__main__':\n" + \
           "    main()\n"
    return header + body


def write_solution_template(problem: dict) -> str:
    os.makedirs(SOLUTIONS_DIR, exist_ok=True)
    pid = problem.get("id", "UNKNOWN")
    path = os.path.join(SOLUTIONS_DIR, f"{pid}.py")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(solution_stub(problem))
    return path


def main():
    parser = argparse.ArgumentParser(description="Spatial Coding Challenge Helper")
    parser.add_argument("--mode", choices=["local"], default="local")
    parser.add_argument("--difficulty", type=int, default=1)
    parser.add_argument("--topic", type=str, default=None)
    parser.add_argument("--category", type=str, default=None, help="basic_coding / pandas / single_cell / spatial")
    parser.add_argument("--timer", action="store_true", help="Start countdown timer after showing problem")
    parser.add_argument("--scaffold", action="store_true", help="Create solution template under solutions/")

    args = parser.parse_args()

    problem = choose_random_problem(difficulty=args.difficulty, topic=args.topic, category=args.category)

    if not problem:
        print("⚠ 조건에 맞는 문제가 없습니다.")
        return

    print("=" * 60)
    print(f"[{problem['id']}] {problem['title']}")
    print(f"📂 Category: {problem.get('category')}")
    print(f"🎯 Difficulty: {problem.get('difficulty')}")
    print(f"⏱ Recommended time: {problem.get('est_time_min', '?')} min")
    print("=" * 60)
    print(problem["description"])
    print("=" * 60)

    if args.scaffold:
        path = write_solution_template(problem)
        print(f"🧱 Template created: {path}")

    if args.timer and problem.get("est_time_min"):
        countdown(int(problem["est_time_min"]))


if __name__ == "__main__":
    main()
