from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # =========================
    # APPLICATION
    # =========================

    APP_NAME: str = "delivery-ai-api"
    API_PREFIX: str = "/api/v1"

    # =========================
    # LANGFUSE
    # =========================
    
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_BASE_URL: str


    # =========================
    # SUPABASE
    # =========================

    SUPABASE_DATABASE_URL: str


    # =========================
    # GROQ
    # =========================

    GROQ_MODEL: str
    GROQ_API_KEY: str

    # =========================
    # OPENAI
    # ====

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    OPENAI_MODEL: str

    # =========================
    # PROVIDER
    # ====
    LLM_PROVIDER: str

    # =========================
    # REDIS
    # ====
    REDIS_URL:str

    # =========================
    # EMAIL
    # ====
    
    EMAIL_ORIGEM: str = ""
    SENHA_APP: str = ""
    EMAIL_DESTINO: str = ""
    
    @property
    def SUPABASE_DATABASE_URL_NO_ASYNC(self) -> str:
        """Gera a URL síncrona automaticamente removendo o +asyncpg."""
        return self.SUPABASE_DATABASE_URL.replace("+asyncpg", "")


settings = Settings()
