import logging
from contextlib import asynccontextmanager
import redis.asyncio as aioredis
from fastapi import FastAPI

from core.config.settings import settings

logger = logging.getLogger(__name__)

# Instância global do cliente Redis
redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    """Gerencia a inicialização e o encerramento limpo do cliente Redis."""
    logger.info("Conexão com Redis inicializada.")
    yield
    logger.info("Fechando conexão com Redis...")
    await redis_client.aclose()
    logger.info("Conexão com Redis encerrada com sucesso.")
