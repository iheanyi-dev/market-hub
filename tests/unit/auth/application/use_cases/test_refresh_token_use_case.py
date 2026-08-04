
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.auth.application.dto.refresh_token_command import (
    RefreshTokenCommand,
)
from app.auth.application.exceptions.invalid_refresh_token_error import (
    InvalidRefreshTokenError,
)
from app.auth.application.use_cases.refresh_token_use_case import (
    RefreshTokenUseCase,
)
from app.auth.domain.entities.refresh_token import RefreshToken
from jwt import InvalidTokenError

@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def hasher():
    return Mock()


@pytest.fixture
def token_generator():
    return Mock()


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    return uow


@pytest.fixture
def use_case(
    repository,
    hasher,
    token_generator,
    unit_of_work,
):
    return RefreshTokenUseCase(
        refresh_token_repository=repository,
        refresh_token_hasher=hasher,
        token_generator=token_generator,
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_refresh_token_success(
    use_case,
    repository,
    hasher,
    token_generator,
    unit_of_work,
):
    user_id = uuid4()

    old = RefreshToken.create(
        user_id=user_id,
        token_hash="old_hash",
        expires_at=datetime.now(UTC)
        + timedelta(days=10),
    )

    command = RefreshTokenCommand(
        refresh_token="old_token",
    )

    token_generator.decode_refresh_token.return_value = {
        "sub": str(user_id),
    }

    hasher.hash.side_effect = [
        "old_hash",
        "new_hash",
    ]

    repository.get_by_token_hash.return_value = old

    token_generator.generate_access_token.return_value = (
        "new_access"
    )

    token_generator.generate_refresh_token.return_value = (
        "new_refresh",
        datetime.now(UTC) + timedelta(days=30),
    )

    result = await use_case.execute(command)

    assert result.access_token == "new_access"
    assert result.refresh_token == "new_refresh"

    repository.update.assert_awaited_once()
    repository.save.assert_awaited_once()
    unit_of_work.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_invalid_token(
    use_case,
    token_generator,
):
    command = RefreshTokenCommand(
        refresh_token="invalid",
    )

    token_generator.decode_refresh_token.side_effect = InvalidTokenError()

    with pytest.raises(
        InvalidRefreshTokenError,
    ):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_token_not_found(
    use_case,
    repository,
    hasher,
    token_generator,
):
    command = RefreshTokenCommand(
        refresh_token="token",
    )

    token_generator.decode_refresh_token.return_value = {
        "sub": str(uuid4()),
    }

    hasher.hash.return_value = "hash"

    repository.get_by_token_hash.return_value = None

    with pytest.raises(
        InvalidRefreshTokenError,
    ):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_revoked_token(
    use_case,
    repository,
    hasher,
    token_generator,
):
    token = RefreshToken.create(
        user_id=uuid4(),
        token_hash="hash",
        expires_at=datetime.now(UTC)
        + timedelta(days=10),
    )

    token.revoke()

    command = RefreshTokenCommand(
        refresh_token="token",
    )

    token_generator.decode_refresh_token.return_value = {
        "sub": str(token.user_id),
    }

    hasher.hash.return_value = "hash"

    repository.get_by_token_hash.return_value = token

    with pytest.raises(
        InvalidRefreshTokenError,
    ):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_expired_token(
    use_case,
    repository,
    hasher,
    token_generator,
):
    token = RefreshToken.create(
        user_id=uuid4(),
        token_hash="hash",
        expires_at=datetime.now(UTC)
        - timedelta(minutes=1),
    )

    command = RefreshTokenCommand(
        refresh_token="token",
    )

    token_generator.decode_refresh_token.return_value = {
        "sub": str(token.user_id),
    }

    hasher.hash.return_value = "hash"

    repository.get_by_token_hash.return_value = token

    with pytest.raises(
        InvalidRefreshTokenError,
    ):
        await use_case.execute(command)