"""
Request schema for user authentication.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginUserRequest(BaseModel):
    """
    Represents the request body required to authenticate a user.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    email: EmailStr = Field(
        description="Registered email address.",
        examples=["john@example.com"],
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password.",
        examples=["Password123!"],
    )