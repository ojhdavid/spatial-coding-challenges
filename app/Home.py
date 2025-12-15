import json
import os
import time
import hashlib
from datetime import date
from typing import Dict, Any, List, Optional

import streamlit as st

from src.loader import load_all_problems  # repo에 존재하는 함수


PROGRESS_PATH = "progress.json"
SOLUTIONS_DIR = "solutions"


# ----------------------------
# Utilities
# ----------------------------
def safe_load_json(path: str, default: Dict[str, Any]) -> Dict[str, Any]:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def safe_write_json(path: str, data: Dict[str, Any]) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def norm(s: Optional[str]) -> str:
    return (s or "").strip()


def contains_seed_xenium(p: Dict[str, Any]) -> bool:
    text = " ".join([
        str(p.get("title", "")),
        str(p.get("description", "")),
        " ".join(p.get("tags") or []),
    ]).lower()
    keywords = ["seed", "xenium", "metastasis", "ln", "lymph node", "postn", "cxcr4", "hif1a"]
    return any(k in text for k in keywords)


def get_categories(problems: List[Dict[str, Any]]) -> List[str]:
    cats = sorted({p.get("category", "uncategorized") for p in problems})
    return cats


def get_topics(problems: List[Dict[str, Any]]) -> List[str]:
    topics = sorted({p.get("topic", "unknown") for p in problems})
    return topics


def filter_problems(
    problems: List[Dict[str, Any]],
    difficulty: Optional[int] = None,
    category: Optional[str] = None,
    topic: Optional[str] = None,
    seed_only: bool = False,
) -> List[Dict[str, Any]]:
    out = []
    for p in problems:
        if difficulty is not None and p.get("difficulty") != difficulty:
            continue
        if category and p.get("category") != category:
            continue
        if topic and p.get("topic") != topic:
            continue
        if seed_only and not contains_seed_xenium(p):
            continue
        out.append(p)
    return out


def stable_daily_choice(problems: List[Dict[str, Any]], salt: str) -> Dict[str, Any]:
    # same day => same problem (deterministic)
    if not problems:
        return {}
    key = f"{date.today().isoformat()}::{salt}"
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    idx = int(h[:8], 16) % len(problems)
    return problems[idx]


def solution_stub(problem: Dict[str, Any]) -> str:
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


def ensure_solution_file(problem: Dict[str, Any]) -> str:
    os.makedirs(SOLUTIONS_DIR, exist_ok=True)
    pid = problem.get("id", "UNKNOWN")
    path = os.path.join(SOLUTIONS_DIR, f"{pid}.py")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(solution_stub(problem))
    return path


# ----------------------------
# Timer (reduced flicker)
# ----------------------------
# ----------------------------
# Timer (fragment-based)
# ----------------------------
def timer_init():
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
        st.session_state.timer_end = 0.0
        st.session_state.timer_total = 0


def timer_start(minutes: int):
    timer_init()
    st.session_state.timer_running = True
    st.session_state.timer_total = int(minutes * 60)
    st.session_state.timer_end = time.time() + st.session_state.timer_total


def timer_reset():
    timer_init()
    st.session_state.timer_running = False
    st.session_state.timer_end = 0.0
    st.session_state.timer_total = 0


@st.fragment(run_every="1s")
def timer_fragment():
    """
    Only this fragment re-runs every second.
    The rest of the page should remain stable.
    """
    timer_init()

    box = st.container(border=True)  # timer card

    if not st.session_state.timer_running:
        with box:
            st.markdown("⏱ **Timer:** Not running")
        return

    remaining = int(st.session_state.timer_end - time.time())
    if remaining <= 0:
        st.session_state.timer_running = False
        with box:
            st.success("⏰ Time's up!")
        return

    m, s = divmod(max(0, remaining), 60)
    total = st.session_state.timer_total or 1
    progress = 1.0 - (remaining / total)

    with box:
        st.markdown(f"⏳ **Remaining:** `{m:02d}:{s:02d}`")
        st.progress(min(max(progress, 0.0), 1.0))




# ----------------------------
# Progress
# ----------------------------
def progress_default() -> Dict[str, Any]:
    return {"solved": [], "attempts": []}


def mark_solved(progress: Dict[str, Any], problem_id: str):
    if problem_id not in progress["solved"]:
        progress["solved"].append(problem_id)


def log_attempt(progress: Dict[str, Any], problem_id: str, notes: str = ""):
    progress["attempts"].append({
        "id": problem_id,
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "notes": notes
    })


# ----------------------------
# UI
# ----------------------------
def main():
    st.set_page_config(page_title="Spatial Coding Challenges", layout="wide")

    problems = load_all_problems()
    categories = get_categories(problems)
    topics = get_topics(problems)

    progress = safe_load_json(PROGRESS_PATH, progress_default())

    st.title("Spatial Coding Challenges")
    st.caption("Category/Difficulty selector • Today's problem • Timer • Progress • Solution template")

    with st.sidebar:
        st.header("Filters")
        difficulty = st.selectbox("Difficulty", options=[1, 2, 3], index=0)
        category = st.selectbox("Category", options=categories, index=0)
        topic = st.selectbox("Topic (optional)", options=["(any)"] + topics, index=0)
        seed_only = st.checkbox("Highlight SEED/Xenium context only", value=False)

        st.divider()
        st.header("Timer")
        if st.button("Reset timer"):
            timer_reset()

        st.divider()
        st.header("Progress")
        st.write(f"✅ Solved: **{len(progress.get('solved', []))}**")
        if st.button("Save progress.json now"):
            safe_write_json(PROGRESS_PATH, progress)
            st.success("Saved progress.json")

    topic_filter = None if topic == "(any)" else topic
    filtered = filter_problems(problems, difficulty=difficulty, category=category, topic=topic_filter, seed_only=seed_only)

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.subheader("Problem picker")

        if not filtered:
            st.warning("No problems found for selected filters.")
            return

        # Today's problem (stable)
        today_problem = stable_daily_choice(filtered, salt=f"{difficulty}:{category}:{topic_filter}:{seed_only}")

        if st.button("🎯 Load Today's problem"):
            st.session_state.selected_id = today_problem.get("id")

        labels = []
        id_to_problem = {}
        solved_set = set(progress.get("solved", []))

        for p in filtered:
            pid = p.get("id", "")
            tag = "✅" if pid in solved_set else "⬜"
            seed = "🌱" if contains_seed_xenium(p) else ""
            labels.append(f"{tag} {seed} {pid} — {p.get('title')}")
            id_to_problem[pid] = p

        # choose selected
        if "selected_id" not in st.session_state:
            st.session_state.selected_id = filtered[0].get("id")

        # find index
        ids = [p.get("id") for p in filtered]
        try:
            current_idx = ids.index(st.session_state.selected_id)
        except ValueError:
            current_idx = 0

        idx = st.selectbox("Select a problem", options=list(range(len(filtered))), index=current_idx, format_func=lambda i: labels[i])
        selected = filtered[idx]
        st.session_state.selected_id = selected.get("id")

        st.divider()
        st.subheader("Selected info")
        st.write(f"**ID:** {selected.get('id')}")
        st.write(f"**Category:** {selected.get('category')}")
        st.write(f"**Topic:** {selected.get('topic')}")
        st.write(f"**Est. time:** {selected.get('est_time_min', '?')} min")

        # badges
        tags = selected.get("tags") or []
        if tags:
            st.markdown("**Tags:** " + " ".join([f"`{t}`" for t in tags]))
        if contains_seed_xenium(selected):
            st.info("🌱 SEED/Xenium-related context detected (keywords/tags).")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⏱ Start timer (est. time)"):
                mins = int(selected.get("est_time_min", 0) or 0)
                if mins <= 0:
                    st.warning("No est_time_min found.")
                else:
                    timer_start(mins)
        with c2:
            if st.button("🧱 Create solution template"):
                path = ensure_solution_file(selected)
                st.success(f"Created: {path}")

        timer_fragment()

        st.divider()
        st.subheader("Mark progress")
        notes = st.text_input("Attempt notes (optional)", value="")
        if st.button("📝 Log attempt"):
            log_attempt(progress, selected.get("id"), notes=notes)
            safe_write_json(PROGRESS_PATH, progress)
            st.success("Attempt logged to progress.json")

        if st.button("✅ Mark solved"):
            mark_solved(progress, selected.get("id"))
            safe_write_json(PROGRESS_PATH, progress)
            st.success("Marked solved in progress.json")

    with col_right:
        st.subheader("Problem description")
        st.markdown(f"### {selected.get('title')}")
        st.code((selected.get("description", "") or "").strip())

        st.divider()

        # ✅ 명확한 답안 입력 영역
        st.subheader("✍️ Solution editor")
        st.caption("여기에 코드를 작성한 뒤, 아래 Save 버튼을 누르면 solutions/ 폴더에 저장됩니다.")

        pid = selected.get("id", "UNKNOWN")
        editor_key = f"solution_text_{pid}"

        # 문제별로 입력 유지
        if editor_key not in st.session_state:
            st.session_state[editor_key] = ""

        st.text_area(
            label="Your solution (Python)",
            key=editor_key,
            height=320,
            placeholder="예) pandas로 groupby 해서 평균 계산...\n\n# 여기에 코드를 작성하세요.",
        )

        cA, cB = st.columns([1, 1])
        with cA:
            if st.button("💾 Save to solutions/", use_container_width=True):
                os.makedirs("solutions", exist_ok=True)
                path = os.path.join("solutions", f"{pid}.py")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(st.session_state[editor_key])
                st.success(f"Saved: {path}")

        with cB:
            if st.button("🧱 Create template (if missing)", use_container_width=True):
                path = ensure_solution_file(selected)
                st.success(f"Template ready: {path}")



if __name__ == "__main__":
    main()
