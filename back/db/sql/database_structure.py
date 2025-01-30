from back.config import settings
from back.logging import logger


class BuildDatabaseRequests:
    """Database structure build."""

    @staticmethod
    def create_schema() -> str:
        """Check and create scema if not exists"""

        logger.info("The creation of the database schema.")
        return f"""
			CREATE SCHEMA IF NOT EXISTS {settings.DB_SCHEMA};
			"""

    @staticmethod
    def create_token_table() -> str:
        """Create token database table."""

        logger.info("The creation of the 'api_token' table in to database.")
        return f"""
			CREATE TABLE IF NOT EXISTS {settings.DB_SCHEMA}.api_token (
				service_name varchar(40) NOT NULL,
				token_hash bytea NOT NULL,
				definition varchar NULL,
				created_at timestamp DEFAULT now() NULL,
				CONSTRAINT api_token_pkey PRIMARY KEY (token_hash),
				CONSTRAINT api_token_service_name_key UNIQUE (service_name)
			);
			"""

    @staticmethod
    def create_permission_token_table() -> str:
        """create tocen and permission relation table."""

        logger.info("The creation of the 'api_permission_token' table in to database.")
        return f"""
			CREATE TABLE IF NOT EXISTS {settings.DB_SCHEMA}.api_permission_token (
				token_hash bytea NOT NULL,
				permission_codes serial4 NOT NULL,
				CONSTRAINT token_perm_key PRIMARY KEY (token_hash, permission_codes),
				CONSTRAINT api_permission_token_permission_codes_fkey FOREIGN KEY (permission_codes) REFERENCES {settings.DB_SCHEMA}.api_permission_codes(lable),
				CONSTRAINT api_permission_token_token_hash_fkey FOREIGN KEY (token_hash) REFERENCES {settings.DB_SCHEMA}.api_token(token_hash)
			);
			"""

    @staticmethod
    def create_permission_type_table() -> str:
        """Create database structure"""

        logger.info("The creation of the 'api_permission_codes' table in to database.")
        return f"""
			CREATE TABLE IF NOT EXISTS {settings.DB_SCHEMA}.api_permission_codes (
				lable serial4 NOT NULL,
				endpoint_name varchar(20) NOT NULL,
				parameter varchar(10) NOT NULL,
				definition varchar NOT NULL,
				CONSTRAINT api_permission_codes_lable_key UNIQUE (lable),
				CONSTRAINT perm_key PRIMARY KEY (endpoint_name, parameter)
			);
			"""

    @staticmethod
    def check_database_shema() -> str:
        """Check for existence of the scheme"""

        logger.info("TChecking if a schema exists in a database.")
        return f"""
        SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{settings.DB_SCHEMA}'
        ;
        """

    @staticmethod
    def check_database_tables() -> str:
        """ChCheck for existence of tables"""

        logger.info("Checking if a tables exists in a database.")
        return f"""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = '{settings.DB_SCHEMA}'
        AND table_name IN ('api_token', 'api_permission_codes', 'api_permission_token');
        ;
        """

    @staticmethod
    def insert_test_token() -> str:
        """insert test token into database."""

        logger.info("TChecking if a schema exists in a database.")
        return f"""
        insert into {settings.DB_SCHEMA}.api_token (service_name, token_hash) 
        values ('test', %s);
        """

    @staticmethod
    def insert_test_permission() -> str:
        """Imei check permission for autocreate."""

        return f"""
        insert into {settings.DB_SCHEMA}.api_permission_codes 
        (endpoint_name, "parameter", definition) values
        ('imei_check', 'ALL', 'test white list');
        """

    @staticmethod
    def insert_test_access() -> str:
        """
        Use service name, table name and marketplace name for creation new permission.
        """

        return f"""
        insert into {settings.DB_SCHEMA}.api_permission_token (token_hash, permission_codes)
        values
        (
        (select n.token_hash from {settings.DB_SCHEMA}.api_token n where n.service_name = 'test'), 
        (select apc.lable from {settings.DB_SCHEMA}.api_permission_codes apc
        where apc.endpoint_name = 'imei_check' and apc.parameter = 'ALL')
        );
        """
