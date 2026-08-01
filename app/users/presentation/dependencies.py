"""
Presentation dependency providers.

This module wires together the presentation layer with the application
and infrastructure layers using FastAPI's dependency injection system.
"""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_db_session

from app.users.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.users.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserRepository:
    """
    Provide the user repository.
    """

    return SQLAlchemyUserRepository(session)


def get_password_hasher() -> Argon2PasswordHasher:
    """
    Provide the password hasher.
    """

    return Argon2PasswordHasher()


async def get_register_user_use_case(
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository,
    ),
    password_hasher: Argon2PasswordHasher = Depends(
        get_password_hasher,
    ),
) -> RegisterUserUseCase:
    """
    Provide the RegisterUserUseCase.
    """

    return RegisterUserUseCase(
        repository=repository,
        password_hasher=password_hasher,
    )