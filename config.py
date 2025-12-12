import os

# 나중에 OpenAI API 쓸 때 ENV에서 읽도록 설계
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4.1-mini"  # 나중에 네가 쓰는 모델 이름으로 바꿔도 됨
