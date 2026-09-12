from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config.settings import settings

# Cria o engine assíncrono para o PostgreSQL
async_engine = create_async_engine(
    settings.SUPABASE_DATABASE_URL,
    echo=False, future=True
)

# Fábrica de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency do FastAPI para injetar sessões de banco de dados assíncronas."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()