"""
Integration tests for the refresh token endpoint.
"""

from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient

from app.auth.domain.entities.refresh_token import RefreshToken
from app.auth.infrastructure.persistence.repositories.sqlalchemy_refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)
from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from app.users.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher
)


@pytest.mark.asyncio
async def test_refresh_token_returns_new_tokens(
    async_client: AsyncClient,
    db_session,
) -> None:
    """
    A valid refresh token should produce a new access token
    and a new refresh token.
    """

    # Arrange
    user_repository = SqlAlchemyUserRepository(db_session)
    refresh_repository = SqlAlchemyRefreshTokenRepository(db_session)

    hasher = Argon2PasswordHasher()
    password_hash = hasher.hash("Hashed@password123")
    user = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("refresh@example.com"),
        password_hash=password_hash,
    )

    await user_repository.save(user)

    login = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "Hashed@password123"
        }
    )

    assert login.status_code == 200
    assert "refresh_token" in async_client.cookies

    refresh = await async_client.post(
        "/api/v1/auth/refresh",
    )
   
    assert refresh.status_code == 200

    body = refresh.json()

    assert "access_token" in body