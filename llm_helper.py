from pathlib import Path
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

FALLBACK_MODELS = [
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b",
]


def build_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to the project's .env file before making a request."
        )

    configured_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
    candidates = []
    if configured_model:
        candidates.append(configured_model)
    candidates.extend(FALLBACK_MODELS)

    seen = set()
    for model_name in candidates:
        if not model_name or model_name in seen:
            continue
        seen.add(model_name)
        try:
            return ChatGroq(api_key=api_key, model=model_name)
        except Exception:
            continue

    raise RuntimeError(
        "No valid Groq model was available for this API key. "
        "Set GROQ_MODEL to a model available on your Groq account."
    )


llm = build_llm()

if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in a samosa are")
    print(response.content)