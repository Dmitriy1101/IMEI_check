"""
psycopg2 and asyncpg queries for sql actions.
"""

from back.config import settings


class AuthQuery:
    """All auth querys text."""

    @staticmethod
    def get_all_permissions() -> str:
        """Check all base permissions."""

        return f"select * from {settings.DB_SCHEMA}.api_permission_codes;"

    @staticmethod
    def insert_hash_key() -> str:
        """
        Add new hash token with account name in db query.
            1: service_name, 2: token_hash
        """

        return f"""
        insert into {settings.DB_SCHEMA}.api_token (service_name, token_hash) 
        values (%s, %s);
        """

    @staticmethod
    def insert_new_permission() -> str:
        """
        Use service name, table name and marketplace name for creation new permission.
            1: service_name, 2: endpoint_name, 3: parameter
        """

        return f"""
        insert into {settings.DB_SCHEMA}.api_permission_token (token_hash, permission_codes)
        values
        (
        (select n.token_hash from {settings.DB_SCHEMA}.api_token n where n.service_name = %s), 
        (select apc.lable from {settings.DB_SCHEMA}.api_permission_codes apc
        where apc.endpoint_name = %s and apc.parameter = %s)
        );
        """

    @staticmethod
    def select_hash_token() -> str:
        """
        Find tokens by permission.
            1: endpoint_name, 2: parameter
        """

        return f"""
        select at2.token_hash from {settings.DB_SCHEMA}.api_token at2 
        left join {settings.DB_SCHEMA}.api_permission_token apt on apt.token_hash = at2.token_hash 
        left join {settings.DB_SCHEMA}.api_permission_codes apc on apc.lable = apt.permission_codes 
        where apc.endpoint_name = %s and apc.parameter = %s;
        """

    @staticmethod
    def check_permission() -> str:
        """
        asyncpg request.
        Check permission by hash token and marketplace. If permission granted return tablename.
            1: endpoint_name, 2: parameter, 3: token_hash
        """

        return f"""
        select apc.endpoint_name from {settings.DB_SCHEMA}.api_token at2 
        left join {settings.DB_SCHEMA}.api_permission_token apt on apt.token_hash = at2.token_hash 
        left join {settings.DB_SCHEMA}.api_permission_codes apc on apc.lable = apt.permission_codes 
        where apc.endpoint_name = $1 and apc.parameter = $2 and apt.token_hash = $3;
        """
