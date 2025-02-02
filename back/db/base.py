"""
Main database connection objects:
    WORK_DB: connection url string
    get_engine: return engine
    MainBase: main database object needed to orm creation.

"""

from sqlalchemy import Engine, create_engine
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

Base = declarative_base()


def get_engine() -> Engine:
    """return db engine"""

    return create_engine(DATABASE, pool_size=5, echo=True)


def get_async_engine() -> Engine:
    """return async db engine"""

    return create_async_engine(DATABASE, pool_size=5, echo=True)


async def get_async_session():
    """Return async session."""

    async_session = sessionmaker(
        bind=get_async_engine(), class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
