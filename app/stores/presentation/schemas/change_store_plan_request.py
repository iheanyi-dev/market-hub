"""
Request schema for the Change Store Plan endpoint.
"""

from pydantic import BaseModel, ConfigDict, Field


class ChangeStorePlanRequest(BaseModel):
    """
    Request payload for changing a store's subscription plan.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    plan: str = Field(
        description="Store plan code.",
    )