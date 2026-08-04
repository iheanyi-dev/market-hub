"""
StoreDescription Value Object.

Represents a validated store description.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StoreDescription:
    """
    Immutable StoreDescription value object.
    """

    value: str

    MAX_LENGTH = 1000

    @classmethod
    def create(cls, value: str) -> 'StoreDescription':
        """
        Validate the description.
        """
        value = value.strip()

        if len(value) > cls.MAX_LENGTH:
            raise ValueError(
                f"Store description cannot exceed {cls.MAX_LENGTH} characters."
            )

        return cls(value)
        #object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value