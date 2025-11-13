from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_async_engine(
    settings.database_url,
    future=True
    #echo = True # Логирование sql
    #connect_args = {"check_same_thread"} для lite
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autocommit = False,
    autoflush=False
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)