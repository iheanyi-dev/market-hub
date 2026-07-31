"""
Unit tests for the FullName value object.
"""

import pytest

from app.users.domain.exceptions.invalid_full_name_error import (
    InvalidFullNameError,
)
from app.users.domain.value_objects.full_name import FullName


class TestFullName:
    """
    Test suite for the FullName value object.
    """

    def test_create_valid_full_name(self) -> None:
        """
        A valid full name should create a FullName value object.
        """
        full_name = FullName.create("John Doe")

        assert full_name.value == "John Doe"

    def test_trim_leading_and_trailing_spaces(self) -> None:
        """
        Leading and trailing whitespace should be removed.
        """
        full_name = FullName.create("   John Doe   ")

        assert full_name.value == "John Doe"

    def test_empty_name_raises_exception(self) -> None:
        """
        An empty name is not allowed.
        """
        with pytest.raises(InvalidFullNameError):
            FullName.create("")

    def test_whitespace_only_name_raises_exception(self) -> None:
        """
        A name containing only whitespace is not allowed.
        """
        with pytest.raises(InvalidFullNameError):
            FullName.create("     ")

    def test_name_too_short_raises_exception(self) -> None:
        """
        Names shorter than two characters should be rejected.
        """
        with pytest.raises(InvalidFullNameError):
            FullName.create("J")

    def test_name_too_long_raises_exception(self) -> None:
        """
        Names longer than one hundred characters should be rejected.
        """
        with pytest.raises(InvalidFullNameError):
            FullName.create("J" * 101)

    def test_equal_names_are_equal(self) -> None:
        """
        Two FullName objects with the same value should be equal.
        """
        first = FullName.create("John Doe")
        second = FullName.create("John Doe")

        assert first == second

    def test_different_names_are_not_equal(self) -> None:
        """
        Different FullName objects should not be equal.
        """
        first = FullName.create("John Doe")
        second = FullName.create("Jane Doe")

        assert first != second