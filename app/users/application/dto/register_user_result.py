"""
Register User Result.

This module defines the data returned after a successful user registration.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RegisterUserResult:
    """
    Represents a successfully registered user.

    Attributes:
        id:
            The user's unique identifier.

        full_name:
            The user's full name.

        email:
            The user's email address.

        role:
            The assigned user role.

        status:
            The current account status.

        created_at:
            When the account was created.

        updated_at:
            When the account was last modified.
    """

    id: str
    full_name: str
    email: str
    role: str
    status: str
    created_at: datetime
    updated_at: datetime