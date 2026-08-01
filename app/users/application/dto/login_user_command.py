"""
Command object for user authentication.

This DTO carries the data required to authenticate a user from the
presentation layer to the application layer.
"""

from dataclasses import dataclass

from app.users.domain.value_objects.email import Email


@dataclass(frozen=True, slots=True)
class LoginUserCommand:
    """
    Represents a request to authenticate a user.
    """

    email: Email
    password: str