from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    Sequence,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from back.config import settings
from back.db.base import Base


class ApiToken(Base):
    """Table storing authentication tokens."""

    __tablename__ = "api_token"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    service_name = Column(String(40), nullable=False, unique=True)
    token_hash = Column(LargeBinary, primary_key=True, nullable=False)
    definition = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now, nullable=True)

    permissions = relationship("ApiPermissionToken", back_populates="token")


class ApiPermissionCodes(Base):
    """Table storing types of API access parameters."""

    __tablename__ = "api_permission_codes"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    lable = Column(
        Integer,
        Sequence("api_permission_codes_lable_seq"),
        primary_key=True,
        nullable=False,
        unique=True,
    )
    endpoint_name = Column(String(20), nullable=False)
    parameter = Column(String(10), nullable=False)
    definition = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("endpoint_name", "parameter", name="perm_key"),
        {"schema": settings.DB_SCHEMA},
    )

    tokens = relationship("ApiPermissionToken", back_populates="permission_code")


class ApiPermissionToken(Base):
    """TABLE linking access type to authentication token."""

    __tablename__ = "api_permission_token"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    token_hash = Column(
        LargeBinary,
        ForeignKey(f"{settings.DB_SCHEMA}.api_token.token_hash"),
        primary_key=True,
        nullable=False,
    )

    permission_codes = Column(
        Integer,
        ForeignKey(f"{settings.DB_SCHEMA}.api_permission_codes.lable"),
        primary_key=True,
        nullable=False,
    )

    token = relationship("ApiToken", back_populates="permissions")
    permission_code = relationship("ApiPermissionCodes", back_populates="tokens")
