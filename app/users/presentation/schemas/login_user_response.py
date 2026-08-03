"""
Response returned after successful authentication.
"""

from pydantic import BaseModel


class LoginUserResponse(BaseModel):
    """
    Response returned after a successful login.

    The refresh token is intentionally omitted because it is
    delivered via an HttpOnly cookie.
    """

    access_token: str
    token_type: str = "bearer"