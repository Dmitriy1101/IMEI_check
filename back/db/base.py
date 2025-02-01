"""
Main database connection objects:
    WORK_DB: connection url string
    get_engine: return engine
    MainBase: main database object needed to orm creation.

"""

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from back.config import settings

DATABASE: str = (
    f"postgresql+asyncpg://{settings.DATABASE_USER}:\
{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:\
{settings.DATABASE_PORT}/{settings.DATABASE_DB}"
)

DB_DICT = {
    "host": settings.DATABASE_HOST,
    "port": settings.DATABASE_PORT,
    "user": settings.DATABASE_USER,
    "password": settings.DATABASE_PASSWORD,
    "dbname": settings.DATABASE_DB,
}

ASYNC_DB = {
    "host": settings.DATABASE_HOST,
    "port": settings.DATABASE_PORT,
    "user": settings.DATABASE_USER,
    "password": settings.DATABASE_PASSWORD,
    "database": settings.DATABASE_DB,
}


def get_engine() -> Engine:
    """return async db engine"""

    return create_async_engine(DATABASE, pool_size=5, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=get_engine(), class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_session():
    """Return async session."""

    async with AsyncSessionLocal() as session:
        yield session
