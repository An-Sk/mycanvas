import os
from langchain_openai import ChatOpenAI
from typing import Dict, Optional
from dotenv import load_dotenv
from utils.logger import logger, MyLoggerCallback


def load_llm() -> ChatOpenAI:
    """Load LLM with support for multiple providers (OpenRouter, OpenAI, Mistral)."""
    load_dotenv()
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("MODEL_NAME", "mistral-large-2411")

    provider_configs: Dict[str, Dict[str, Optional[str]]] = {
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": None
        },
        "openrouter": {
            "api_key": os.getenv("OPENROUTER_API_KEY"),
            "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        },
        "mistral": {
            "api_key": os.getenv("MISTRAL_API_KEY", os.getenv("MISTRAL_API_KEY")),
            "base_url": os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
        },
        "moonshotai": {
            "api_key": os.getenv("MOONSHOTAI_API_KEY", os.getenv("MOONSHOTAI_API_KEY")),
            "base_url": os.getenv("MOONSHOTAI_BASE_URL", "https://api.moonshot.ai/v1")
        }
    }

    if provider not in provider_configs:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: {list(provider_configs.keys())}")

    config = provider_configs[provider]
    api_key = config["api_key"]
    base_url = config["base_url"]

    #print(api_key, model)

    if not api_key:
        raise ValueError(f"API key for provider '{provider}' is not set. Please check your environment variables.")


    logger.debug("Loaded LLM %s with provider=%s", model, provider)

    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        max_retries=3,
        callbacks=[MyLoggerCallback()]
    )

    return llm