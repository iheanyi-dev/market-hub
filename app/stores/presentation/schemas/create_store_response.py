"""
Create Store Response.

Defines the response returned after creating a store.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateStoreResponse(BaseModel):
    """
    Response model returned after a successful store creation.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

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