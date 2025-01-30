"""
Main database connection objects:
    WORK_DB: connection url string
    get_engine: return engine
    MainBase: main database object needed to orm creation.

"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase

from back.config import settings

DB: str = (
    f"postgresql+psycopg2://{settings.DATABASE_USER}:\
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
    """return db engine"""
    return create_engine(DB, pool_size=5, echo=True)


class MainBase(DeclarativeBase):
    """Main orm database obj."""
