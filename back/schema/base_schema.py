"""
Base project schema.
"""

from enum import Enum


class Schema(Enum):
    """Scema for adding function to all scemas."""

    @classmethod
    def get_by_name(cls, name: str):
        """Find member by name."""
        for _ in cls:
            if _.name == name:
                return _
        return None
