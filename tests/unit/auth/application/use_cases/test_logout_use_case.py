import pytest
from unittest.mock import AsyncMock, Mock

from app.auth.application.dto.refresh_token_command import (
    RefreshTokenCommand,
)
from app.auth.application.exceptions.invalid_refresh_token_error import (
    InvalidRefreshTokenError,
)
from app.auth.application.use_cases.logout_use_case import (
    LogoutUseCase,
)
from app.auth.domain.entities.refresh_token import RefreshToken

from datetime import datetime, timedelta, UTC
from uuid import uuid4


@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def hasher():
    return Mock()


@pytest.fixture
def unit_of_work():
    return AsyncMock()


@pytest.fixture
def use_case(
    repository,
    hasher,
    unit_of_work,
):
    return LogoutUseCase(
        refresh_token_repository=repository,
        refresh_token_hasher=hasher,
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_logout_success(
    use_case,
    repository,
    hasher,
    unit_of_work,
):
    token = RefreshToken.create(
        user_id=uuid4(),
        token_hash="hash",
        expires_at=datetime.now(UTC)
        + timedelta(days=30),
    )

    hasher.hash.return_value = "hash"

    repository.get_by_token_hash.return_value = token

    await use_case.execute(
        RefreshTokenCommand(
            refresh_token="token",
        )
    )

    assert token.is_revoked

    repository.update.assert_awaited_once()
    unit_of_work.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_logout_invalid_token(
    use_case,
    repository,
    hasher,
):
    hasher.hash.return_value = "hash"

    repository.get_by_token_hash.return_value = None

    with pytest.raises(
        InvalidRefreshTokenError,
    ):
        await use_case.execute(
            RefreshTokenCommand(
                refresh_token="invalid",
            )
        )