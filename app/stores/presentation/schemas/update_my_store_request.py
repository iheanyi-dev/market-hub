"""
Request schema for the Update My Store endpoint.

Only mutable store attributes are accepted.

The following fields are intentionally excluded because they are managed
elsewhere in the system:

- slug
- plan
- product_count
- owner
"""

from pydantic import BaseModel, ConfigDict, Field


class UpdateMyStoreRequest(BaseModel):
    """
    Request payload for updating a store.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    name: str = Field(
        min_length=3,
        max_length=100,
        description="Store name.",
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Store description.",
    )