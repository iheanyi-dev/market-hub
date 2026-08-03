"""
Result returned after a successful user authentication.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginUserResult:
    """
    Represents the result of a successful authentication.

    After a successful login, the client receives both a short-lived
    access token and a long-lived refresh token.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"