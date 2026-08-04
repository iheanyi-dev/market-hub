"""
Application command for updating a store.

This DTO transports the validated data from the presentation layer
to the application layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class UpdateMyStoreCommand:
    """
    Command for updating a store.
    """

    owner_id: UUID
    name: str
    description: str | None