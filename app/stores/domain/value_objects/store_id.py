"""
StoreId Value Object.

Represents the unique identifier of a Store.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class StoreId:
    """
    Immutable Store identifier.
    """

    value: UUID

    @classmethod
    def create(cls) -> "StoreId":
        """
        Create a new StoreId.
        """
        return cls(uuid4())

    @classmethod
    def from_string(cls, value: str) -> "StoreId":
        """
        Create a StoreId from its string representation.
        """
        return cls(UUID(value))

    def __str__(self) -> str:
        """
        Return the UUID as a string.
        """
        return str(self.value)