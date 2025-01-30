import hashlib
import secrets
from typing import Any

from fastapi import HTTPException

from back.config import settings
from back.db.decorator import async_bynary_conn, bynary_conn
from back.db.sql import AuthQuery
from back.db.sql import BuildDatabaseRequests as Builder
from back.logging import logger
from back.schema import AccessType


@async_bynary_conn
async def database_request(sql_request: str, __conn=None) -> Any:
    """
    Run SQL database request.
    :param sql_request: str value contained SQL request
    :return Any: SQL request result
    """

    logger.info("run sql database code.")
    logger.debug("Executing SQL code:\n%s", sql_request)
    data = await __conn.fetch(sql_request)
    return data


@bynary_conn
def create_database_structure(__conn=None) -> None:
    """
    Run SQL database request.
    :param sql_request: str value contained SQL request
    :return Any: SQL request result
    """

    logger.info("Checking database structure.")
    cur = __conn.cursor()

    scema = cur.execute(Builder.check_database_shema())
    tables = cur.execute(Builder.check_database_tables())

    if scema and len(tables) == 3:
        logger.info("The database structure has already been created.")
        __conn.commit()
        return cur.close()

    logger.info("The creation of the database structure has begun.")
    cur.execute(Builder.create_schema())
    cur.execute(Builder.create_token_table())
    cur.execute(Builder.create_permission_type_table())
    cur.execute(Builder.create_permission_token_table())
    if _ := settings.TEST_TOKEN:
        cur.execute(Builder.insert_test_token(), (hashlib.sha256(_.encode()).digest(),))
        cur.execute(Builder.insert_test_permission())
        cur.execute(Builder.insert_test_access())
    __conn.commit()
    cur.close()


@async_bynary_conn
async def has_permission(
    token: str, acsess_type: AccessType, code: str, __conn=None
) -> bool:
    """
    Check token permission by table name and marketplace or param code.
    Raise HTTPException if acsess denied.
    """
    logger.info("Check permissions.")
    token_hash: bytes = hashlib.sha256(token.encode()).digest()
    query: str = AuthQuery.check_permission()
    table: str = acsess_type.value
    data = await __conn.fetch(query, table, code, token_hash)
    if len(data) == 1:
        logger.info(data)
        return dict(data[0])["table_name"] == table
    else:
        raise HTTPException(status_code=403, detail="Acsess denied...")


@bynary_conn
def permissions(__conn=None) -> list:
    """Get all permissions types."""

    cur = __conn.cursor()
    logger.info("Search permissions types.")
    cur.execute(AuthQuery.get_all_permissions())
    return cur.fetchall()


@bynary_conn
def gen_key(service_name: str, __conn=None) -> str:
    """Create new hash key in database by service name, return key."""

    key: str = secrets.token_urlsafe(60)
    query: str = AuthQuery.insert_hash_key()
    cur = __conn.cursor()
    cur.execute(query, (service_name, hashlib.sha256(key.encode()).digest()))
    __conn.commit()
    cur.close()
    return key
