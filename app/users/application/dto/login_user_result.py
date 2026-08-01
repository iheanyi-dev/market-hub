"""
Result returned after a successful user authentication.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginUserResult:
    """
    Represents the result of a successful authentication.
    """

    access_token: str
    token_type: str = "bearer"