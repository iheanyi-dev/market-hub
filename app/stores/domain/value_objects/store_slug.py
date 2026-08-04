"""
StoreSlug Value Object.

Represents a validated, URL-friendly store slug.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_RESERVED_SLUGS = {
    "admin",
    "api",
    "auth",
    "login",
    "logout",
    "register",
    "support",
    "www",
}


@dataclass(frozen=True, slots=True)
class StoreSlug:
    """
    Immutable StoreSlug value object.
    """

    value: str

    @classmethod
    def create(cls, value:str) -> None:
        """
        Validate the slug.
        """
        value = value.strip().lower()

        if not value:
            raise ValueError("Store slug cannot be empty.")

        if len(value) < 3:
            raise ValueError("Store slug must be at least 3 characters long.")

        if len(value) > 100:
            raise ValueError("Store slug cannot exceed 100 characters.")

        if value in _RESERVED_SLUGS:
            raise ValueError(f'"{value}" is a reserved slug.')

        if not _SLUG_PATTERN.fullmatch(value):
            raise ValueError(
                "Store slug may contain only lowercase letters, numbers and hyphens."
            )

        return cls(value)
        #object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value