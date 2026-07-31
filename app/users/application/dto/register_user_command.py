"""
Register User Command.

This module defines the input required to register a new user.

The command is a simple data carrier used by the application layer to
transfer data into the RegisterUserUseCase. It contains no business logic.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    """
    Represents the data required to register a new user.

    Attributes:
        full_name:
            The user's full name.

        email:
            The user's email address.

        password:
            The user's plaintext password.
    """

    full_name: str
    email: str
    password: str