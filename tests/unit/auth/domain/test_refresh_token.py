from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.auth.domain.entities.refresh_token import RefreshToken


def test_create_refresh_token() -> None:
    """A refresh token should be created successfully."""

    token = RefreshToken(
        id=uuid4(),
        user_id=uuid4(),
        token_hash="hashed_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    assert token.token_hash == "hashed_token"
    assert token.is_revoked is False


def test_refresh_token_is_not_expired() -> None:
    """A valid refresh token should not be expired."""

    token = RefreshToken(
        id=uuid4(),
        user_id=uuid4(),
        token_hash="hashed_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    assert token.is_expired() is False


def test_refresh_token_is_expired() -> None:
    """An expired refresh token should report as expired."""

    token = RefreshToken(
        id=uuid4(),
        user_id=uuid4(),
        token_hash="hashed_token",
        expires_at=datetime.now(UTC) - timedelta(seconds=1),
    )

    assert token.is_expired() is True


def test_revoke_refresh_token() -> None:
    """Revoking a refresh token should mark it as revoked."""

    token = RefreshToken(
        id=uuid4(),
        user_id=uuid4(),
        token_hash="hashed_token",
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )

    token.revoke()

    assert token.is_revoked is True