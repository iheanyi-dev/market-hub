"""
Unit tests for the RegisterUserUseCase.
"""

import pytest

from app.users.application.dto.register_user_command import RegisterUserCommand
from app.users.application.exceptions.email_already_exists_error import (
    EmailAlreadyExistsError,
)
from app.users.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from tests.fakes.fake_password_hasher import FakePasswordHasher
from uuid import UUID

class TestRegisterUserUseCase:
    """
    Test suite for the RegisterUserUseCase.
    """

    @pytest.mark.asyncio
    async def test_register_user_success(
        self,
        user_repository,
    ) -> None:
        """
        A new user should be successfully registered.
        """
        use_case = RegisterUserUseCase(
            repository=user_repository,
            password_hasher=FakePasswordHasher(),
        )

        command = RegisterUserCommand(
            full_name="John Doe",
            email="john@example.com",
            password="StrongPass@123",
        )

        result = await use_case.execute(command)

        assert result.full_name == "John Doe"
        assert result.email == "john@example.com"
        assert UUID(result.id)

    @pytest.mark.asyncio
    async def test_duplicate_email_raises_exception(
        self,
        user_repository,
    ) -> None:
        """
        Registering two users with the same email should fail.
        """
        use_case = RegisterUserUseCase(
            repository=user_repository,
            password_hasher=FakePasswordHasher(),
        )

        command = RegisterUserCommand(
            full_name="John Doe",
            email="john@example.com",
            password="StrongPass@123",
        )

        assert await use_case.execute(command)

        with pytest.raises(EmailAlreadyExistsError):
            await use_case.execute(command)