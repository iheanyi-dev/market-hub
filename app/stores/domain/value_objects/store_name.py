"""
StoreName Value Object.

Represents a validated store name.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StoreName:
    """
    Immutable StoreName value object.
    """

    value: str

    @classmethod
    def create(cls, value: str) -> None:
        """
        Validate the store name.
        """
        value = value.strip()

        if not value:
            raise ValueError("Store name cannot be empty.")

        if len(value) < 3:
            raise ValueError("Store name must be at least 3 characters long.")

        if len(value) > 100:
            raise ValueError("Store name cannot exceed 100 characters.")

        return cls(value)
        #object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value