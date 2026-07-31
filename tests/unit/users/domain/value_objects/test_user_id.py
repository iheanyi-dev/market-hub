"""
Unit tests for the UserId value object.
"""

from uuid import UUID

import pytest

from app.users.domain.value_objects.user_id import UserId


class TestUserId:
    """
    Test suite for the UserId value object.
    """

    def test_create_generates_uuid(self) -> None:
        """
        Creating a UserId should generate a valid UUID.
        """
        user_id = UserId.create()

        assert isinstance(user_id.value, UUID)

    def test_from_string_creates_user_id(self) -> None:
        """
        A valid UUID string should create a UserId.
        """
        original = UserId.create()

        recreated = UserId.from_string(str(original))

        assert recreated == original

    def test_invalid_uuid_raises_value_error(self) -> None:
        """
        An invalid UUID string should raise ValueError.
        """
        with pytest.raises(ValueError):
            UserId.from_string("not-a-valid-uuid")

    def test_string_representation(self) -> None:
        """
        The string representation should match the underlying UUID.
        """
        user_id = UserId.create()

        assert str(user_id) == str(user_id.value)

    def test_equal_user_ids(self) -> None:
        """
        UserIds created from the same UUID should be equal.
        """
        original = UserId.create()

        copy = UserId.from_string(str(original))

        assert original == copy

    def test_different_user_ids_are_not_equal(self) -> None:
        """
        Different UserIds should not be equal.
        """
        assert UserId.create() != UserId.create()