"""
Unit tests for the User aggregate.
"""

from app.users.domain.entities.user import User
from app.users.domain.enums.user_role import UserRole
from app.users.domain.enums.user_status import UserStatus
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.user_id import UserId
from app.users.domain.value_objects.full_name import FullName


class TestUser:
    """
    Test suite for the User aggregate.
    """

    def test_create_user(self) -> None:
        """
        Creating a user should initialize all required properties.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        assert isinstance(user.id, UserId)
        assert user.full_name == FullName.create('John Doe')
        assert user.email == Email.create("john@example.com")
        assert user.password_hash == "hashed-password"
        assert user.role == UserRole.CUSTOMER
        assert user.status == UserStatus.ACTIVE

    def test_activate_user(self) -> None:
        """
        Activating a user should change the account status to ACTIVE.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        user.deactivate()
        user.activate()

        assert user.status == UserStatus.ACTIVE

    def test_deactivate_user(self) -> None:
        """
        Deactivating a user should change the account status to INACTIVE.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        user.deactivate()

        assert user.status == UserStatus.INACTIVE

    def test_suspend_user(self) -> None:
        """
        Suspending a user should change the account status to SUSPENDED.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        user.suspend()

        assert user.status == UserStatus.SUSPENDED
    def test_changing_to_same_name_does_not_update_timestamp(self) -> None:
        """
        Changing to the same name should not modify the aggregate.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        previous_updated_at = user.updated_at

        user.change_name(
            FullName.create("John Doe")
        )

        assert user.updated_at == previous_updated_at
    def test_changing_to_same_email_does_not_update_timestamp(self) -> None:
        """
        Changing to the same email should not modify the aggregate.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        previous_updated_at = user.updated_at

        user.change_email(
            Email.create("john@example.com")
        )

        assert user.updated_at == previous_updated_at

    def test_changing_to_same_password_hash_does_not_update_timestamp(self) -> None:
        """
        Changing to the same password hash should not modify the aggregate.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        previous_updated_at = user.updated_at

        user.change_password_hash("hashed-password")

        assert user.updated_at == previous_updated_at

    def test_promote_to_vendor(self) -> None:
        """
        Promoting a customer should change the role to VENDOR.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        user.promote_to_vendor()

        assert user.role == UserRole.VENDOR

    def test_promote_to_admin(self) -> None:
        """
        Promoting a user should change the role to ADMIN.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        user.promote_to_admin()

        assert user.role == UserRole.ADMIN
    def test_change_name(self) -> None:
        """
        Changing a user's name should replace the existing FullName value object.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        new_name = FullName.create("Jane Smith")

        user.change_name(new_name)

        assert user.full_name == new_name
    def test_updated_at_changes_when_name_changes(self) -> None:
        """
        Changing the user's name should update the modification timestamp.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        previous_updated_at = user.updated_at

        user.change_name(
            FullName.create("Jane Smith")
        )

        assert user.updated_at > previous_updated_at

    def test_change_email(self) -> None:
        """
        Changing a user's email should replace the existing Email value object.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        new_email = Email.create("jane@example.com")

        user.change_email(new_email)

        assert user.email == new_email

    def test_change_password_hash(self) -> None:
        """
        Changing the password should replace the stored password hash.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="old-hash",
        )

        user.change_password_hash("new-hash")

        assert user.password_hash == "new-hash"