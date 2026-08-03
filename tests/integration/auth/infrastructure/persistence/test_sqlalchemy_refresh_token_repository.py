"""
Integration tests for the SQLAlchemy implementation of the
RefreshTokenRepository.

These tests verify that refresh tokens can be:

1. Saved.
2. Retrieved by their hash.
3. Updated after being revoked.

Unlike unit tests, these tests interact with the real database.
"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.auth.domain.entities.refresh_token import RefreshToken
from app.auth.infrastructure.persistence.repositories.sqlalchemy_refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.domain.entities.user import User

from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)




@pytest.mark.asyncio
async def test_save_refresh_token(db_session) -> None:
    """
    Verify that a refresh token can be persisted.
    """
    user_repository = SqlAlchemyUserRepository(db_session)

    repository = SqlAlchemyRefreshTokenRepository(db_session)

    user = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john1@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(user)

    refresh_token = RefreshToken.create(
        user_id=user.id.value,
        token_hash="hashed_refresh_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    await repository.save(refresh_token)

    stored_token = await repository.get_by_token_hash(
        "hashed_refresh_token"
    )

    assert stored_token is not None
    assert stored_token.token_hash == "hashed_refresh_token"


@pytest.mark.asyncio
async def test_get_refresh_token_by_hash(db_session) -> None:
    """
    Verify that a refresh token can be retrieved using its hash.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyRefreshTokenRepository(db_session)

    user = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john2@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(user)

    refresh_token = RefreshToken.create(
        user_id=user.id.value,
        token_hash="hashed_refresh_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    await repository.save(refresh_token)

    result = await repository.get_by_token_hash("hashed_refresh_token")

    assert result is not None
    assert result.id == refresh_token.id


@pytest.mark.asyncio
async def test_update_refresh_token(db_session) -> None:
    """
    Verify that updates made to a refresh token
    are correctly persisted.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyRefreshTokenRepository(db_session)

    user = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john3@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(user)

    refresh_token = RefreshToken.create(
        user_id=user.id.value,
        token_hash="hashed_refresh_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    await repository.save(refresh_token)

    refresh_token.revoke()

    await repository.update(refresh_token)

    updated_token = await repository.get_by_token_hash("hashed_refresh_token")

    assert updated_token is not None
    assert updated_token.is_revoked is True