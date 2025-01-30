"""
Work decorators using to create db connection.
"""

import logging
from typing import Any, Callable

import asyncpg
import psycopg2
from sqlalchemy.orm import Session

from back.db.base import ASYNC_DB, DB_DICT, get_engine

log: logging.Logger = logging.getLogger("Connection decorator")


def orm_conn(f: Callable) -> Callable:
    """
    EN: Main database connection object. To use this decorator,
    decorated function must hav session parameter: "__session: Session = None"
    RU: Основной объект подключения к базе данных. Чтобы использовать этот декоратор,
    декорированная функция должна иметь параметр сеанса: «__session: Session = None»
    """

    def inner(*args, **kwargs) -> Any:
        log.info("Base connection started.")
        with Session(get_engine()) as session, session.begin():
            data = f(__session=session, *args, **kwargs)
        log.info("Base connection ended.")
        return data

    return inner


def bynary_conn(f) -> Callable:
    """
    Database bynary connector, use psycopg2.
    Function must have '__conn=None' arg.
    """

    def inner(*args, **kwargs) -> Any:
        log.info("Base connection started.")
        conn = psycopg2.connect(**DB_DICT)
        d = f(__conn=conn, *args, **kwargs)
        conn.close()
        log.info("Base connection ended.")
        return d

    return inner


def async_bynary_conn(f) -> Callable:
    """
    Async bynary database connector, use asyncpg.
    Function must have '__conn=None' arg.
    """

    async def inner(*args, **kwargs) -> Any:
        conn = await asyncpg.connect(**ASYNC_DB)
        d = await f(__conn=conn, *args, **kwargs)
        await conn.close()
        return d

    return inner
