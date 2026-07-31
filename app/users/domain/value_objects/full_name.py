"""
FullName Value Object.

This module defines the FullName value object.

A FullName represents a validated person's name within the domain.
"""

from __future__ import annotations

from app.users.domain.exceptions.invalid_full_name_error import (
    InvalidFullNameError,
)


class FullName:
    """
    Represents a validated person's full name.

    Instances of this class are immutable and compare by value.
    """

    _MIN_LENGTH = 2
    _MAX_LENGTH = 100

    def __init__(self, value: str) -> None:
        """
        Initialize a FullName.

        Use the ``create()`` factory method instead of calling this
        constructor directly.

        Args:
            value:
                A validated full name.
        """
        self._value = value

    @classmethod
    def create(cls, value: str) -> "FullName":
        """
        Validate and create a FullName value object.

        Args:
            value:
                The supplied full name.

        Returns:
            A validated FullName object.

        Raises:
            InvalidFullNameError:
                If the supplied name violates the domain rules.
        """
        value = value.strip()

        if not value:
            raise InvalidFullNameError(
                "Full name cannot be empty."
            )

        if len(value) < cls._MIN_LENGTH:
            raise InvalidFullNameError(
                f"Full name must contain at least {cls._MIN_LENGTH} characters."
            )

        if len(value) > cls._MAX_LENGTH:
            raise InvalidFullNameError(
                f"Full name cannot exceed {cls._MAX_LENGTH} characters."
            )

        return cls(value)

    @property
    def value(self) -> str:
        """
        Return the validated full name.
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """
        Compare two FullName value objects.
        """
        if not isinstance(other, FullName):
            return NotImplemented

        return self._value == other._value

    def __hash__(self) -> int:
        """
        Return the hash of the value object.
        """
        return hash(self._value)

    def __str__(self) -> str:
        """
        Return the string representation of the full name.
        """
        return self._value

    def __repr__(self) -> str:
        """
        Return the developer-friendly representation.
        """
        return f"FullName('{self._value}')"