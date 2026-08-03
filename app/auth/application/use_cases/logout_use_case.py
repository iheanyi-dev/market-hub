"""
Application use case responsible for logging out an authenticated user.

Responsibilities:
    - Locate the refresh token.
    - Verify that it exists.
    - Revoke it.
    - Commit the transaction.

The presentation layer is responsible for deleting the HttpOnly cookie.
"""

from __future__ import annotations

from app.auth.application.dto.refresh_token_command import (
    RefreshTokenCommand,
)
from app.auth.application.exceptions.invalid_refresh_token_error import (
    InvalidRefreshTokenError,
)
from app.auth.application.ports.refresh_token_hasher import (
    RefreshTokenHasher,
)
from app.auth.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.shared.application.ports.unit_of_work import UnitOfWork


class LogoutUseCase:
    """
    Logout an authenticated user.

    Logging out consists of revoking the persisted refresh token.
    """

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        refresh_token_hasher: RefreshTokenHasher,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = refresh_token_repository
        self._hasher = refresh_token_hasher
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: RefreshTokenCommand,
    ) -> None:
        """
        Revoke a refresh token.

        Raises:
            InvalidRefreshTokenError:
                If the refresh token does not exist.
        """

        token_hash = self._hasher.hash(
            command.refresh_token,
        )

        refresh_token = await self._repository.get_by_token_hash(
            token_hash
        )

        if refresh_token is None:
            raise InvalidRefreshTokenError()

        refresh_token.revoke()

        try:
            await self._repository.update(
                refresh_token,
            )

            await self._unit_of_work.commit()

        except Exception:
            await self._unit_of_work.rollback()
            raise