"""
Response schema returned after successful authentication.
"""

from pydantic import BaseModel, ConfigDict, Field


class LoginUserResponse(BaseModel):
    """
    Represents the response returned after a successful login.
    """

    model_config = ConfigDict(
        frozen=True,
    )

    access_token: str = Field(
        description="JWT access token.",
    )

    token_type: str = Field(
        description="Authentication scheme.",
        examples=["bearer"],
    )