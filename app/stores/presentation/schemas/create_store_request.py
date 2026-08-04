"""
Create Store Request.

Defines the request body for creating a store.
"""

from pydantic import BaseModel, ConfigDict, Field


class CreateStoreRequest(BaseModel):
    """
    Request model for creating a store.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    slug: str = Field(
        min_length=3,
        max_length=100,
    )

    description: str = Field(
        default="",
        max_length=1000,
    )

    plan: str = Field(
        min_length=1,
        max_length=50,
    )