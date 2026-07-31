"""
Unit tests for the UserStatus enumeration.
"""

from app.users.domain.enums.user_status import UserStatus


class TestUserStatus:
    """
    Test suite for the UserStatus enum.
    """

    def test_active_status(self) -> None:
        """
        Verify the ACTIVE enum value.
        """
        assert UserStatus.ACTIVE.value == "active"

    def test_inactive_status(self) -> None:
        """
        Verify the INACTIVE enum value.
        """
        assert UserStatus.INACTIVE.value == "inactive"

    def test_suspended_status(self) -> None:
        """
        Verify the SUSPENDED enum value.
        """
        assert UserStatus.SUSPENDED.value == "suspended"

    def test_deleted_status(self) -> None:
        """
        Verify the DELETED enum value.
        """
        assert UserStatus.DELETED.value == "deleted"

    def test_enum_member_count(self) -> None:
        """
        Ensure the expected number of statuses exists.
        """
        assert len(UserStatus) == 4