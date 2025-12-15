import argparse
import time

from .selector import choose_random_problem
from ai.gpt_client import generate_spatial_coding_problem


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


def main():
    parser = argparse.ArgumentParser(
        description="Spatial Coding Challenge Helper"
    )
    parser.add_argument("--mode", choices=["local", "gpt"], default="local")
    parser.add_argument("--difficulty", type=int, default=1)
    parser.add_argument("--topic", type=str, default=None)
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="basic_coding / pandas / single_cell / spatial",
    )
    parser.add_argument(
        "--timer",
        action="store_true",
        help="Start countdown timer after showing problem",
    )
    parser.add_argument("--context", type=str, default="")

    args = parser.parse_args()

    if args.mode == "local":
        problem = choose_random_problem(
            difficulty=args.difficulty,
            topic=args.topic,
            category=args.category,
        )

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

        if args.timer and problem.get("est_time_min"):
            countdown(problem["est_time_min"])

    else:  # GPT mode
        topic = args.topic or "scanpy"
        text = generate_spatial_coding_problem(
            difficulty=args.difficulty,
            topic=topic,
            context=args.context,
        )
        print(text)


if __name__ == "__main__":
    main()
