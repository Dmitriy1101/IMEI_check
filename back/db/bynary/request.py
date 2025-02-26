import secrets
from datetime import datetime
from typing import Any

import bcrypt
from fastapi import HTTPException
from psycopg2.errors import NotNullViolation, UniqueViolation

from back.db.decorator import async_bynary_conn, bynary_conn
from back.db.sql import AuthQuery
from back.db.utils import generate_token_id
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


@async_bynary_conn
async def has_permission(
    token: str, acsess_type: AccessType, code: str, __conn=None
) -> bool:
    """
    Check token permission by enpoint name and param code.
    Raise HTTPException if acsess denied.
    """
    logger.info("Check permissions.")
    query: str = AuthQuery.check_permission()
    endpoint: str = acsess_type.value
    data = await __conn.fetch(query, endpoint, code, generate_token_id(token=token))
    for d in data:
        if bcrypt.checkpw(token.encode(), d[0]):
            logger.info("Service '%s' is here.", d[1])
            return True
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
    cur.execute(
        query,
        (
            service_name,
            generate_token_id(token=key),
            bcrypt.hashpw(key.encode(), bcrypt.gensalt()),
            datetime.utcnow(),
        ),
    )
    __conn.commit()
    cur.close()
    return key


@bynary_conn
def add_permission(
    service_name: str, acsess_type: AccessType, code: str, __conn=None
) -> bool:
    """Add new permission by service name. Return True if sucsess."""

    query: str = AuthQuery.insert_new_permission()
    cur = __conn.cursor()
    try:
        cur.execute(query, (service_name, acsess_type.value, code))
        __conn.commit()
        return True
    except NotNullViolation as e:
        logger.exception(e)
        logger.exception(
            "parameter code error check permissions parameter codes for this acsess_type."
        )
        __conn.rollback()
        return False
    except UniqueViolation as e:
        logger.exception(e)
        logger.exception(
            "Permission for '%s' to endpoint: '%s' and code: '%s' already exists.",
            service_name,
            acsess_type.value,
            code,
        )
        __conn.rollback()
        return True
    finally:
        cur.close()
