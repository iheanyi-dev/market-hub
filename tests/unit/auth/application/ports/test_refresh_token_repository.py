from inspect import isabstract

from app.auth.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)


def test_refresh_token_repository_is_abstract() -> None:
    """RefreshTokenRepository should be an abstract class."""

    assert isabstract(RefreshTokenRepository)