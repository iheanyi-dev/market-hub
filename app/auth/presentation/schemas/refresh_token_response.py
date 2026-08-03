"""
Response returned after a successful refresh.
"""

from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    Response returned after refreshing an access token.

    The refresh token is delivered via an HttpOnly cookie.
    """

    access_token: str
    token_type: str = "bearer"