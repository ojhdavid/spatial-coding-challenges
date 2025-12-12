# Spatial Coding Challenges (for Spatial Transcriptomics)

This repository is a **personal training ground** for practicing
Python coding in the context of **spatial transcriptomics** (Xenium, Visium, etc.).

The idea is:

- Not to become a full-time software engineer,
- But to become a **“scientist-type coder”** who can:
  - design analysis workflows,
  - read and modify code,
  - and run reproducible spatial pipelines independently.

---

## 🎯 Goals

- Build muscle memory for:
  - `pandas` (data wrangling)
  - `scanpy` (single-cell / spatial analysis)
  - `squidpy` (spatial statistics)
- Practice **no-AI coding sessions** (30 min / week)
- Gradually collect my own **reusable code blocks** (templates)
- Use tasks that are directly relevant to:
  - LUAD
  - SEED (Stromal-Enriched Metastatic Decider) niches
  - Xenium / Visium-based spatial analysis

---

## 🗂 Repository Structure

```text
spatial-coding-challenges/
├─ README.md
├─ requirements.txt
├─ problems/
│  ├─ level1_basics.yaml      # 기초 pandas / scanpy 과제
│  ├─ level2_qc.yaml          # QC / preprocessing 과제 (추가 예정)
│  ├─ level3_spatial.yaml     # spatial / niche 분석 과제 (추가 예정)
│  └─ ...                     # 앞으로 점점 늘려갈 예정
├─ src/
│  ├─ __init__.py
│  ├─ loader.py               # YAML 문제 로드
│  ├─ selector.py             # 난이도/주제별 문제 선택
│  └─ cli.py                  # 터미널용 인터페이스
├─ ai/
│  ├─ __init__.py
│  └─ gpt_client.py           # GPT 기반 문제 생성 (선택)
└─ config.py                  # OpenAI API 설정 (환경변수 사용)
