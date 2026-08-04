"""
Create Store Result.

Returned after successfully creating a store.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class CreateStoreResult:
    """
    Output of CreateStoreUseCase.
    """

    id: str
    owner_id: str
    name: str
    slug: str
    description: str
    plan: str
    product_count: int
    status: str
    created_at: datetime
    updated_at: datetime