"""
Table codes needed for permissions.
"""

from back.schema.base_schema import Schema


class AccessType(Schema):
    """This is database table code witch using for permission to the table."""

    IMEI_CHECK = "imei_check"
