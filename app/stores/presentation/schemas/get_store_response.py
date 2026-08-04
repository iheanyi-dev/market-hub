"""
Response schema for the public Get Store endpoint.

This schema represents the public information returned when
retrieving a store using its slug.

Sensitive or internal fields such as the store ID and owner ID
are intentionally omitted.
"""

from pydantic import BaseModel, ConfigDict


class GetStoreResponse(BaseModel):
    """
    Public store response.
    """

    model_config = ConfigDict(frozen=True, from_attributes=True)

    name: str
    slug: str
    description: str | None
    plan: str
    product_count: int