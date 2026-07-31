"""
Password Value Object.

This module implements the Password value object for the domain layer.

Responsibilities:
    - Validate passwords against the domain password policy.
    - Represent a valid plaintext password during domain operations.

This value object intentionally does NOT hash passwords. Hashing is an
infrastructure concern handled by a PasswordHasher implementation.
"""

from __future__ import annotations

import re

from app.users.domain.exceptions.invalid_password_error import (
    InvalidPasswordError,
)
from app.users.domain.exceptions.weak_password_error import (
    WeakPasswordError,
)


class Password:
    """
    Represents a validated plaintext password.

    The Password value object exists only to enforce the application's
    password policy. It should be short-lived and used during operations
    such as user registration or password changes.

    Password hashing is delegated to a PasswordHasher implementation in
    the infrastructure layer.
    """

    # Password policy
    _MIN_LENGTH = 8
    _MAX_LENGTH = 128

    def __init__(self, value: str) -> None:
        """
        Initialize a Password value object.

        This constructor assumes the password has already been validated.
        Use the `create()` factory method instead of calling the constructor
        directly.

        Args:
            value:
                A validated plaintext password.
        """
        self._value = value

    @classmethod
    def create(cls, password: str) -> "Password":
        """
        Validate and create a Password value object.

        Args:
            password:
                The plaintext password.

        Returns:
            A validated Password value object.

        Raises:
            InvalidPasswordError:
                If the password contains leading or trailing whitespace.

            WeakPasswordError:
                If the password violates the password policy.
        """
        cls._validate(password)

        return cls(password)

    @staticmethod
    def _validate(password: str) -> None:
        """
        Validate the supplied password against the application's password policy.

        Validation rules:
            - No leading or trailing whitespace
            - Minimum length
            - Maximum length
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character
        """

        if password != password.strip():
            raise InvalidPasswordError(
                "Password must not contain leading or trailing spaces."
            )

        if len(password) < Password._MIN_LENGTH:
            raise WeakPasswordError(
                f"Password must contain at least {Password._MIN_LENGTH} characters."
            )

        if len(password) > Password._MAX_LENGTH:
            raise WeakPasswordError(
                f"Password cannot exceed {Password._MAX_LENGTH} characters."
            )

        if not re.search(r"[A-Z]", password):
            raise WeakPasswordError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise WeakPasswordError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise WeakPasswordError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[^\w\s]", password):
            raise WeakPasswordError(
                "Password must contain at least one special character."
            )

    @property
    def value(self) -> str:
        """
        Return the validated plaintext password.

        This property is intended for immediate use by the application layer,
        where it is passed to a PasswordHasher. The plaintext password should
        never be persisted or logged.
        """
        return self._value

    def __eq__(self, other: object) -> bool:
        """
        Compare two Password value objects.

        Two Password objects are equal when their validated plaintext values
        are identical.
        """
        if not isinstance(other, Password):
            return NotImplemented

        return self._value == other._value

    def __repr__(self) -> str:
        """
        Return a safe string representation.

        The plaintext password is intentionally hidden to prevent accidental
        exposure in logs or debugging output.
        """
        return "Password(****)"