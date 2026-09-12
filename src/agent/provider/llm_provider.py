import instructor

from langfuse.openai import AsyncOpenAI

from core.config.settings import settings


class LLMProvider:

    def __init__(self):

        self.provider = settings.LLM_PROVIDER.lower()

        if self.provider == "groq":

            self.model = settings.GROQ_MODEL
            self.base_url = "https://api.groq.com/openai/v1"

            raw_client = AsyncOpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url=self.base_url,
            )

            self.client = instructor.apatch(
                raw_client,
                mode=instructor.Mode.JSON,
            )

        elif self.provider == "openai":

            self.model = settings.OPENAI_MODEL
            self.base_url = "https://api.openai.com/v1"

            raw_client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
            )

            self.client = instructor.apatch(
                raw_client,
                mode=instructor.Mode.TOOLS,
            )

        else:

            raise ValueError(
                f"Provedor LLM desconhecido: {self.provider}"
            )


llm_provider = LLMProvider()