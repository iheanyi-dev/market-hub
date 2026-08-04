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
from app.shared.infrastructure.security.jwt_token_generator import (
    JwtTokenGenerator
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

    hasher = JwtTokenGenerator()
    password_hash = JwtTokenGenerator.
    user = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("refresh@example.com"),
        password_hash="Hashed@password123",
    )

    await user_repository.save(user)

    details = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "Hashed@password123"
        },
    )

    response = await async_client.post(
            "/api/v1/auth/refresh",
            headers={
                "Cookie": details.cookies,
            },
        )


    # await user_repository.save(user)

    refresh_token = RefreshToken.create(
        user_id=user.id.value,
        token_hash="hashed_refresh_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    # await refresh_repository.save(refresh_token)

    # # Act
    # response = await async_client.post(
    #     "/api/v1/auth/refresh",
    #     json={
    #         "refresh_token": "refresh_token",
    #     },
    # )

    # Assert
    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    #assert "refresh_token" in body