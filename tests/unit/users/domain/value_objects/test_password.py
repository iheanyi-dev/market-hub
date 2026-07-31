"""
Unit tests for the Password Value Object.

These tests define the expected behaviour of the Password value object before
its implementation. This follows the Red-Green-Refactor cycle of Test-Driven
Development (TDD).
"""

import pytest

from app.users.domain.exceptions.invalid_password_error import InvalidPasswordError
from app.users.domain.exceptions.weak_password_error import WeakPasswordError
from app.users.domain.value_objects.password import Password


class TestPassword:
    """
    Test suite for the Password value object.
    """
    def test_create_valid_password(self) -> None:
        """
        A valid password should successfully create a Password object.
        """
        password = Password.create("StrongPass@123")

        assert password is not None

    def test_password_too_short(self) -> None:
        """
        Passwords shorter than the minimum required length should be rejected.
        """
        with pytest.raises(WeakPasswordError):
            Password.create("Ab1@")

    def test_password_without_uppercase(self) -> None:
        """
        Passwords must contain at least one uppercase letter.
        """
        with pytest.raises(WeakPasswordError):
            Password.create("strongpass@123")

    def test_password_without_lowercase(self) -> None:
        """
        Passwords must contain at least one lowercase letter.
        """
        with pytest.raises(WeakPasswordError):
            Password.create("STRONGPASS@123")

    def test_password_without_digit(self) -> None:
        """
        Passwords must contain at least one numeric digit.
        """
        with pytest.raises(WeakPasswordError):
            Password.create("StrongPass@")

    def test_password_without_special_character(self) -> None:
        """
        Passwords must contain at least one special character.
        """
        with pytest.raises(WeakPasswordError):
            Password.create("StrongPass123")

    def test_password_with_leading_space(self) -> None:
        """
        Leading whitespace is rejected to avoid accidental user input and
        inconsistencies during authentication.
        """
        with pytest.raises(InvalidPasswordError):
            Password.create(" StrongPass@123")

    def test_password_with_trailing_space(self) -> None:
        """
        Trailing whitespace is rejected for the same reason as leading
        whitespace.
        """
        with pytest.raises(InvalidPasswordError):
            Password.create("StrongPass@123 ")

