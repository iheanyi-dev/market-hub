"""
Request schema for the refresh token endpoint.
"""

from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    """
    Request body for refreshing an access token.
    """

    refresh_token: str = Field(
        ...,
        description="Valid refresh token issued during login.",
    )