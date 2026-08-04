"""
Get My Store Result.

Represents the data returned when retrieving
the authenticated user's store.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class GetMyStoreResult:
    """
    Result returned by GetMyStoreUseCase.
    """

    id: UUID
    owner_id: UUID
    name: str
    slug: str
    description: str
    plan: str
    product_count: int
    status: str
    created_at: datetime
    updated_at: datetime