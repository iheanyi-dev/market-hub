# from app.auth.application.dto.refresh_token_command import RefreshTokenCommand
# from app.auth.application.dto.refresh_token_result import RefreshTokenResult
# from app.auth.application.exceptions.invalid_refresh_token_error import (
#     InvalidRefreshTokenError,
# )
# from app.auth.application.ports.refresh_token_repository import (
#     RefreshTokenRepository,
# )
# from app.auth.domain.entities.refresh_token import RefreshToken


# class RefreshTokenUseCase:
#     """
#     Use case responsible for rotating refresh tokens and issuing
#     a new access token.

#     Workflow:
#         1. Hash the incoming refresh token.
#         2. Retrieve the stored refresh token.
#         3. Validate that it exists, is not revoked and not expired.
#         4. Revoke the current refresh token.
#         5. Generate a new refresh token.
#         6. Persist the new refresh token.
#         7. Generate a new access token.
#         8. Return the new token pair.
#     """

#     def __init__(
#         self,
#         repository: RefreshTokenRepository,
#         token_service,
#     ) -> None:
#         """
#         Initialize the use case.

#         Args:
#             repository: Repository for refresh token persistence.
#             token_service: Service responsible for hashing tokens and
#                            generating JWTs.
#         """
#         self._repository = repository
#         self._token_service = token_service

#     async def execute(
#         self,
#         command: RefreshTokenCommand,
#     ) -> RefreshTokenResult:
#         """
#         Refresh an access token using a valid refresh token.

#         Args:
#             command: Refresh token request.

#         Returns:
#             A newly generated access token and refresh token.

#         Raises:
#             InvalidRefreshTokenError:
#                 - Refresh token does not exist.
#                 - Refresh token has expired.
#                 - Refresh token has already been revoked.
#         """

#         # Hash the raw refresh token received from the client.
#         token_hash = self._token_service.hash_refresh_token(
#             command.refresh_token
#         )

#         # Retrieve the stored refresh token.
#         refresh_token = await self._repository.get_by_token_hash(
#             token_hash
#         )

#         # Reject unknown refresh tokens.
#         if refresh_token is None:
#             raise InvalidRefreshTokenError()

#         # Reject revoked refresh tokens.
#         if refresh_token.is_revoked:
#             raise InvalidRefreshTokenError()

#         # Reject expired refresh tokens.
#         if refresh_token.is_expired():
#             raise InvalidRefreshTokenError()

#         # Revoke the current refresh token.
#         refresh_token.revoke()

#         # Persist the revoked state.
#         await self._repository.update(refresh_token)

#         # Generate a new refresh token.
#         new_refresh_token = (
#             self._token_service.create_refresh_token(
#                 refresh_token.user_id
#             )
#         )

#         # Hash the newly generated refresh token before storage.
#         new_token_hash = self._token_service.hash_refresh_token(
#             new_refresh_token
#         )

#         # Create a new refresh token entity.
#         #
#         # NOTE:
#         # The expires_at value will be supplied once the JWT service
#         # exposes the refresh token expiry policy.
#         new_refresh_token_entity = RefreshToken.create(
#             user_id=refresh_token.user_id,
#             token_hash=new_token_hash,
#             expires_at=refresh_token.expires_at,  # Temporary placeholder
#         )

#         # Persist the new refresh token.
#         await self._repository.save(new_refresh_token_entity)

#         # Generate a new access token.
#         access_token = self._token_service.create_access_token(
#             refresh_token.user_id
#         )

#         # Return the new token pair to the client.
#         return RefreshTokenResult(
#             access_token=access_token,
#             refresh_token=new_refresh_token,
#         )


"""
Application use case responsible for refreshing JWT tokens.

Responsibilities:
    - Validate the supplied refresh token.
    - Ensure the token exists in persistence.
    - Ensure the token has not been revoked.
    - Ensure the token has not expired.
    - Rotate the refresh token.
    - Generate a new access token.
    - Persist the rotated refresh token.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from jwt import InvalidTokenError

from app.auth.application.dto.refresh_token_command import (
    RefreshTokenCommand,
)
from app.auth.application.dto.refresh_token_result import (
    RefreshTokenResult,
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
from app.auth.domain.entities.refresh_token import RefreshToken
from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.application.ports.unit_of_work import UnitOfWork


class RefreshTokenUseCase:
    """
    Refresh an authenticated user's tokens.

    The use case implements refresh-token rotation. Every successful
    refresh invalidates the previous refresh token and issues a new one.
    """

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        refresh_token_hasher: RefreshTokenHasher,
        token_generator: TokenGenerator,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._repository = refresh_token_repository
        self._hasher = refresh_token_hasher
        self._token_generator = token_generator
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: RefreshTokenCommand,
    ) -> RefreshTokenResult:
        """
        Refresh authentication tokens.

        Raises:
            InvalidRefreshTokenError:
                If the supplied refresh token is invalid,
                revoked or expired.
        """

        #
        # Decode JWT.
        #
        try:
            payload = self._token_generator.decode_refresh_token(
                command.refresh_token,
            )

        except InvalidTokenError:
            raise InvalidRefreshTokenError()

        #
        # Hash the supplied token.
        #
        token_hash = self._hasher.hash(
            command.refresh_token,
        )

        #
        # Retrieve persisted token.
        #
        stored_token = await self._repository.get_by_token_hash(
            token_hash,
        )

        if stored_token is None:
            raise InvalidRefreshTokenError()

        #
        # Ensure token has not been revoked.
        #
        if stored_token.is_revoked:
            raise InvalidRefreshTokenError()

        #
        # Ensure token has not expired.
        #
        if stored_token.expires_at <= datetime.now(UTC):
            raise InvalidRefreshTokenError()

        #
        # Revoke previous refresh token.
        #
        stored_token.revoke()

        #
        # Generate new tokens.
        #
        access_token = (
            self._token_generator.generate_access_token(
                subject=payload["sub"],
            )
        )

        refresh_token, expires_at = (
            self._token_generator.generate_refresh_token(
                subject=payload["sub"],
            )
        )

        #
        # Hash new refresh token.
        #
        new_hash = self._hasher.hash(
            refresh_token,
        )

        #
        # Create rotated refresh token.
        #
        new_refresh_token = RefreshToken.create(
            user_id=UUID(payload["sub"]),
            token_hash=new_hash,
            expires_at=expires_at,
        )

        try:

            #
            # Persist revocation.
            #
            await self._repository.update(
                stored_token,
            )

            #
            # Persist new token.
            #
            await self._repository.save(
                new_refresh_token,
            )

            #
            # Commit transaction.
            #
            await self._unit_of_work.commit()

        except Exception:

            await self._unit_of_work.rollback()
            raise

        return RefreshTokenResult(
            access_token=access_token,
            refresh_token=refresh_token,
        )