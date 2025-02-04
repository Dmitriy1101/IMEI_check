"""test auth data

Revision ID: cbd160e38a2e
Revises: cc8ac5d2bfd7
Create Date: 2025-02-01 20:03:12.188799

"""

import hashlib
from datetime import datetime
from typing import Sequence, Union

import bcrypt
import sqlalchemy as sa

from alembic import op
from back.config import settings
from back.db.utils import generate_token_id

# revision identifiers, used by Alembic.
revision: str = "cbd160e38a2e"
down_revision: Union[str, None] = "cc8ac5d2bfd7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        f"""
        insert into {settings.DB_SCHEMA}.api_permission_codes 
        (endpoint_name, "parameter", definition) values
        ('imei_check', 'ALL', 'test white list');
    """
    )
    test_token_hash = bcrypt.hashpw(settings.TEST_TOKEN.encode(), bcrypt.gensalt())
    token_id = generate_token_id(token=settings.TEST_TOKEN)
    insert_query = sa.text(
        """
        INSERT INTO test_back.api_token (service_name, token_id, token_hash, definition, created_at)
        VALUES (:service_name, :token_id, :token_hash, :definition, :created_at)
    """
    )
    op.execute(
        insert_query.bindparams(
            sa.bindparam("service_name", "tester"),
            sa.bindparam("token_id", token_id),
            sa.bindparam("token_hash", test_token_hash),
            sa.bindparam("definition", "Test token"),
            sa.bindparam("created_at", datetime.utcnow()),
        )
    )
    op.execute(
        f"""
        insert into {settings.DB_SCHEMA}.api_permission_token (token_id, permission_codes)
        values
        (
        (select n.token_id from {settings.DB_SCHEMA}.api_token n where n.service_name = 'tester'), 
        (select apc.lable from {settings.DB_SCHEMA}.api_permission_codes apc
        where apc.endpoint_name = 'imei_check' and apc.parameter = 'ALL')
        );
    """
    )


def downgrade() -> None:
    op.execute(
        f"""
        delete from {settings.DB_SCHEMA}.api_permission_token apt 
        where apt.token_id = (select n.token_id from {settings.DB_SCHEMA}.api_token n 
        where n.service_name = 'tester')
        and apt.permission_codes = (select apc.lable from {settings.DB_SCHEMA}.api_permission_codes apc
        where apc.endpoint_name = 'imei_check' and apc.parameter = 'ALL');
    """
    )
    op.execute(
        f"""
        delete from {settings.DB_SCHEMA}.api_token n
        where n.service_name  = 'tester';
    """
    )
    op.execute(
        f"""
        delete from {settings.DB_SCHEMA}.api_permission_codes apc
        where apc.endpoint_name = 'imei_check' and apc.parameter = 'ALL';
    """
    )
