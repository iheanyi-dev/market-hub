"""
Register User Use Case.

This module implements the business workflow for registering a new user.
"""

from __future__ import annotations

from app.users.application.dto.register_user_command import (
    RegisterUserCommand,
)
from app.users.application.dto.register_user_result import (
    RegisterUserResult,
)
from app.users.application.exceptions.email_already_exists_error import (
    EmailAlreadyExistsError,
)
from app.users.application.mappers.user_mapper import UserMapper
from app.users.application.ports.user_repository import UserRepository
from app.users.domain.entities.user import User
from app.users.domain.ports.password_hasher import PasswordHasher
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.domain.value_objects.password import Password


class RegisterUserUseCase:
    """
    Register a new user.
    """

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        """
        Initialize the use case.

        Args:
            repository:
                User persistence implementation.

            password_hasher:
                Password hashing implementation.
        """
        self._repository = repository
        self._password_hasher = password_hasher

    async def execute(
        self,
        command: RegisterUserCommand,
    ) -> User:
        """
        Register a new user.

        Args:
            command:
                Registration data.

        Returns:
            The newly created User aggregate.

        Raises:
            EmailAlreadyExistsError:
                If the email address is already registered.
        """

        # Validate the incoming registration data.
        full_name = FullName.create(command.full_name)
        email = Email.create(command.email)
        password = Password.create(command.password)

        # Ensure the email address is unique.
        if await self._repository.exists_by_email(email):
            raise EmailAlreadyExistsError(
                f"A user with email '{email.value}' already exists."
            )

        # Hash the validated password.
        password_hash = await self._password_hasher.hash(
            password.value
        )

        # Create the User aggregate.
        user = User.create(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
        )

        # Persist the aggregate.
        await self._repository.save(user)

        return UserMapper.to_register_result(user)