"""
Application use case responsible for retrieving the currently
authenticated user.

Responsibilities:
    - Decode the JWT access token.
    - Retrieve the authenticated user.
    - Ensure the user exists.
"""

from __future__ import annotations

from uuid import UUID

from jwt import InvalidTokenError

from app.shared.application.ports.token_generator import TokenGenerator
from app.users.application.exceptions.user_not_found_exception import (
    UserNotFoundException,
)
from app.users.application.ports.user_repository import UserRepository
from app.users.domain.entities.user import User


class GetCurrentUserUseCase:
    """
    Retrieve the currently authenticated user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        token_generator: TokenGenerator,
    ) -> None:
        self._user_repository = user_repository
        self._token_generator = token_generator

    async def execute(
        self,
        access_token: str,
    ) -> User:
        """
        Retrieve the authenticated user.

        Args:
            access_token:
                Bearer JWT.

        Returns:
            User.

        Raises:
            InvalidTokenError
            UserNotFoundException
        """

        payload = self._token_generator.decode_access_token(
            access_token,
        )

        user_id = UUID(payload["sub"])

        user = await self._user_repository.get_by_id(
            user_id,
        )

        if user is None:
            raise UserNotFoundException()

        return user