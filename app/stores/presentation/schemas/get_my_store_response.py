"""
Response schema for retrieving the authenticated user's store.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GetMyStoreResponse(BaseModel):
    """
    Response returned for GET /stores/me.
    """

    model_config = ConfigDict(from_attributes=True)

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