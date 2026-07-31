"""
Unit tests for the UserRole enumeration.
"""

from app.users.domain.enums.user_role import UserRole


class TestUserRole:
    """
    Test suite for the UserRole enum.
    """

    def test_customer_role(self) -> None:
        """
        Verify the CUSTOMER enum value.
        """
        assert UserRole.CUSTOMER.value == "customer"

    def test_vendor_role(self) -> None:
        """
        Verify the VENDOR enum value.
        """
        assert UserRole.VENDOR.value == "vendor"

    def test_admin_role(self) -> None:
        """
        Verify the ADMIN enum value.
        """
        assert UserRole.ADMIN.value == "admin"

    def test_enum_member_count(self) -> None:
        """
        Ensure the expected number of roles exists.
        """
        assert len(UserRole) == 3