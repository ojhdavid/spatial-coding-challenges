from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def generate_spatial_coding_problem(difficulty: int, topic: str, context: str = "") -> str:
    if client is None:
        return "OPENAI_API_KEY is not set."

    prompt = f'''
You are a tutor generating spatial transcriptomics coding problems.
Difficulty: {difficulty}
Topic: {topic}
Context: {context}

Create one Korean coding problem (no solution), about 30 minutes difficulty.
'''
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text
