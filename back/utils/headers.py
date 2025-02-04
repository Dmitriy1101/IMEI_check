"""
Main utils.
"""

from fastapi.security import APIKeyHeader

header_key = APIKeyHeader(name="token")
