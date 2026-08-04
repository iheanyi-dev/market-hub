"""
Application DTO returned by the Get Store By Slug use case.

This DTO contains only the public information that should be exposed
when a store is retrieved using its public slug.

Internal identifiers such as the store ID and owner ID are deliberately
excluded to avoid leaking implementation details.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetStoreResult:
    """
    Public representation of a store.

    Attributes:
        name:
            Human-readable store name.

        slug:
            Public URL slug.

        description:
            Optional store description.

        plan:
            Current subscription plan.

        product_count:
            Number of products currently owned by the store.
    """

    name: str
    slug: str
    description: str | None
    plan: str
    product_count: int