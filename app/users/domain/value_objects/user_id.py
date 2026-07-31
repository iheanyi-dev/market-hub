"""
User Identifier Value Object.

This module defines the UserId value object used to uniquely identify
a user within the domain.

A UserId wraps a UUID and provides validation and value semantics.
"""

from __future__ import annotations

from uuid import UUID, uuid4


class UserId:
    """
    Represents the unique identifier of a user.

    Instances of this class are immutable and compare by value.
    """

    def __init__(self, value: UUID) -> None:
        """
        Initialize a UserId.

        Args:
            value:
                A UUID representing the user's identifier.
        """
        self._value = value

    @classmethod
    def create(cls) -> "UserId":
        """
        Generate a new unique user identifier.

        Returns:
            A newly generated UserId.
        """
        return cls(uuid4())

    @classmethod
    def from_string(cls, value: str) -> "UserId":
        """
        Create a UserId from its string representation.

        Args:
            value:
                UUID string.

        Returns:
            A UserId instance.

        Raises:
            ValueError:
                If the supplied string is not a valid UUID.
        """
        return cls(UUID(value))

    @property
    def value(self) -> UUID:
        """
        Return the underlying UUID.
        """
        return self._value

    def __str__(self) -> str:
        """
        Return the string representation of the identifier.
        """
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        """
        Compare two UserId objects by value.
        """
        if not isinstance(other, UserId):
            return NotImplemented

        return self._value == other._value

    def __hash__(self) -> int:
        """
        Return the hash of the identifier.

        This allows UserId to be used in sets and as dictionary keys.
        """
        return hash(self._value)

    def __repr__(self) -> str:
        """
        Return the developer-friendly representation.
        """
        return f"UserId('{self._value}')"