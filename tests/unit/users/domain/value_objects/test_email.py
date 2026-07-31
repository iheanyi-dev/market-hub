"""
Unit tests for the Email value object.

These tests define the expected behavior of the Email class before
its implementation (TDD - Red phase).
"""

from dataclasses import FrozenInstanceError

import pytest

from app.users.domain.exceptions.invalid_email_error import InvalidEmailError
from app.users.domain.value_objects.email import Email


class TestEmail:
    """
    Test suite for the Email value object.
    """

    def test_should_create_email_with_valid_address(self) -> None:
        """
        Should successfully create an Email from a valid address.
        """
        email = Email("john@gmail.com")

        assert email.value == "john@gmail.com"

    def test_should_normalize_email(self) -> None:
        """
        Should trim whitespace and convert the email to lowercase.
        """
        email = Email("  John@GMAIL.com  ")

        assert email.value == "john@gmail.com"

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "",
            "abc",
            "john",
            "@gmail.com",
            "john@",
            "john@gmail",
            "john.com",
        ],
    )
    def test_should_raise_exception_for_invalid_email(
        self,
        invalid_email: str,
    ) -> None:
        """
        Should reject invalid email formats.
        """
        with pytest.raises(InvalidEmailError):
            Email(invalid_email)

    def test_should_compare_emails_by_value(self) -> None:
        """
        Email objects with the same normalized value should be equal.
        """
        first = Email("JOHN@gmail.com")
        second = Email("john@gmail.com")

        assert first == second

    def test_should_be_immutable(self) -> None:
        """
        Email objects should be immutable.
        """
        email = Email("john@gmail.com")

        with pytest.raises(FrozenInstanceError):
            email.value = "new@gmail.com"

    def test_should_return_email_as_string(self) -> None:
        """
        String conversion should return the normalized email address.
        """
        email = Email("john@gmail.com")

        assert str(email) == "john@gmail.com"