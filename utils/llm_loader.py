import os
from langchain_openai import ChatOpenAI

def load_llm():
    """Load LLM with defaults set for Mistral via OpenAI-compatible API."""

    provider = os.getenv("MODEL_PROVIDER", "openai")
    model = os.getenv("MODEL_NAME", "mistral-large-2411")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("BASE_URL", "https://api.mistral.ai/v1")

    if provider != "openai":
        raise ValueError(f"Unsupported provider: {provider}")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url
    )