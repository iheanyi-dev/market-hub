"""
User Aggregate Root.

This module defines the User aggregate, which is responsible for maintaining
the consistency and business rules of a user account.

The User aggregate is the entry point for all user-related domain operations.
External code should modify a User only through the behaviors exposed by this
class.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.users.domain.enums.user_role import UserRole
from app.users.domain.enums.user_status import UserStatus
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.domain.value_objects.user_id import UserId


class User:
    """
    Represents a user within the domain.

    A User is the aggregate root of the Users bounded context. It owns its
    state and ensures that changes occur only through well-defined behaviors.
    """

    def __init__(
        self,
        user_id: UserId,
        full_name: FullName,
        email: Email,
        password_hash: str,
        role: UserRole,
        status: UserStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        """
        Initialize a User aggregate.

        This constructor should not be called directly. Use the ``create()``
        factory method to ensure new users are created with valid defaults.

        Args:
            user_id:
                The unique identifier of the user.

            full_name:
                The user's validated full name.

            email:
                The user's validated email address.

            password_hash:
                The user's hashed password.

            role:
                The user's role.

            status:
                The user's account status.

            created_at:
                Timestamp indicating when the user was created.

            updated_at:
                Timestamp indicating when the user was last modified.
        """
        self._id = user_id
        self._full_name = full_name
        self._email = email
        self._password_hash = password_hash
        self._role = role
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(
        cls,
        full_name: FullName,
        email: Email,
        password_hash: str,
    ) -> "User":
        """
        Create a new User aggregate.

        New users are automatically assigned:
            - A generated UserId
            - CUSTOMER role
            - ACTIVE status
            - Creation and modification timestamps

        Args:
            full_name:
                A validated FullName value object.

            email:
                A validated Email value object.

            password_hash:
                A hashed password.

        Returns:
            A newly created User aggregate.
        """
        now = datetime.now(UTC)

        return cls(
            user_id=UserId.create(),
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def reconstitute(
            cls,
            user_id: UserId,
            full_name: FullName,
            email: Email,
            password_hash: str,
            role: UserRole,
            status: UserStatus,
            created_at: datetime,
            updated_at: datetime,
        ) -> "User":
        """
        Reconstruct an existing User aggregate from persisted data.

        This factory is intended for infrastructure code when loading a
        previously persisted user from storage.

        Args:
            user_id:
                The user's unique identifier.

            full_name:
                The user's full name.

            email:
                The user's email.

            password_hash:
                The stored password hash.

            role:
                The user's role.

            status:
                The user's account status.

            created_at:
                Account creation timestamp.

            updated_at:
                Last modification timestamp.

            Returns:
                A reconstructed User aggregate.
        """
        return cls(
            user_id=user_id,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

    @property
    def id(self) -> UserId:
        """
        Return the user's unique identifier.
        """
        return self._id

    @property
    def full_name(self) -> FullName:
        """
        Return the user's full name.
        """
        return self._full_name

    @property
    def email(self) -> Email:
        """
        Return the user's email address.
        """
        return self._email

    @property
    def password_hash(self) -> str:
        """
        Return the user's password hash.

        Note:
            This is the stored password hash, never the plaintext password.
        """
        return self._password_hash

    @property
    def role(self) -> UserRole:
        """
        Return the user's current role.
        """
        return self._role

    @property
    def status(self) -> UserStatus:
        """
        Return the user's current account status.
        """
        return self._status

    @property
    def created_at(self) -> datetime:
        """
        Return the timestamp when the user was created.
        """
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """
        Return the timestamp when the user was last modified.
        """
        return self._updated_at

    def change_name(self, full_name: FullName) -> None:
        """
        Change the user's full name.

        If the supplied name is identical to the current one, no state change
        occurs and the modification timestamp remains unchanged.

        Args:
            full_name:
                A validated FullName value object.
        """
        if self._full_name == full_name:
            return

        self._full_name = full_name
        self._touch()

    def change_email(self, email: Email) -> None:
        """
        Change the user's email address.

        If the supplied email is identical to the current one, no state change
        occurs and the modification timestamp remains unchanged.

        Args:
            email:
                A validated Email value object.
        """
        if self._email == email:
            return

        self._email = email
        self._touch()

    def change_password_hash(self, password_hash: str) -> None:
        """
        Replace the user's password hash.

        If the supplied hash matches the current one, no state change occurs.

        Args:
            password_hash:
                The newly generated password hash.
        """
        if self._password_hash == password_hash:
            return

        self._password_hash = password_hash
        self._touch()

    def activate(self) -> None:
        """
        Activate the user account.
        """
        self._status = UserStatus.ACTIVE
        self._touch()

    def deactivate(self) -> None:
        """
        Deactivate the user account.
        """
        self._status = UserStatus.INACTIVE
        self._touch()

    def suspend(self) -> None:
        """
        Suspend the user account.

        A suspended account cannot authenticate until reactivated by
        an administrator or another domain process.
        """
        self._status = UserStatus.SUSPENDED
        self._touch()

    def promote_to_vendor(self) -> None:
        """
        Promote the user to the VENDOR role.
        """
        self._role = UserRole.VENDOR
        self._touch()

    def promote_to_admin(self) -> None:
        """
        Promote the user to the ADMIN role.
        """
        self._role = UserRole.ADMIN
        self._touch()

    def _touch(self) -> None:
        """
        Update the modification timestamp.

        Every state-changing operation should call this method to ensure
        the aggregate accurately records when it was last modified.
        """
        self._updated_at = datetime.now(UTC)

    def __repr__(self) -> str:
        """
        Return a developer-friendly representation of the aggregate.

        Sensitive information such as the password hash is intentionally
        omitted.
        """
        return (
            f"User("
            f"id={self._id}, "
            f"full_name={self._full_name}, "
            f"email={self._email}, "
            f"role={self._role.value}, "
            f"status={self._status.value}"
            f")"
        )