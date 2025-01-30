"""
Database structure utilities.
"""

from back.db.bynary.request import database_request
from back.db.sql import BuildDatabaseRequests as Builder
from back.logging import logger


async def crete_database_structure() -> None:
    """Checking the database structure and creating it if it does not exist."""

    scema = await database_request(sql_request=Builder.check_database_shema())
    tables = await database_request(sql_request=Builder.check_database_tables())
    if scema and len(tables) == 3:
        logger.info("The database structure has already been created.")
        return
    logger.info("The creation of the database structure has begun.")
    await database_request(sql_request=Builder.create_schema())
    await database_request(sql_request=Builder.create_token_table())
    await database_request(sql_request=Builder.create_permission_type_table())
    await database_request(sql_request=Builder.create_permission_token_table())
