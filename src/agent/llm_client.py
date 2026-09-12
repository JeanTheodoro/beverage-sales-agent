from openai import AsyncOpenAI
from core.config.settings import settings

class LLMClient:
    _instance: AsyncOpenAI | None = None

    @classmethod
    def get_client(cls) -> AsyncOpenAI:
        if cls._instance is None:
            cls._instance = AsyncOpenAI(
                                api_key=settings.OPENAI_API_KEY,
                                base_url=settings.OPENAI_BASE_URL,
                            )
        return cls._instance
