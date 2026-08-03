# """
# Application use case responsible for authenticating a user.

# The use case validates the supplied credentials, generates an access
# token for authenticated users, and returns the authentication result.
# """

# from app.users.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
# from app.shared.application.ports.token_generator import TokenGenerator
# from app.shared.application.ports.unit_of_work import UnitOfWork
# from app.users.application.dto.login_user_command import LoginUserCommand
# from app.users.application.dto.login_user_result import LoginUserResult
# from app.users.application.exceptions.invalid_credentials_exception import (
#     InvalidCredentialsException,
# )
# from app.users.application.ports.user_repository import UserRepository


# class LoginUserUseCase:
#     """
#     Authenticate a registered user.
#     """

#     def __init__(
#         self,
#         user_repository: UserRepository,
#         password_hasher: Argon2PasswordHasher,
#         token_generator: TokenGenerator,
#         unit_of_work: UnitOfWork,
#     ) -> None:
#         """
#         Initialize the use case.

#         Args:
#             user_repository: User persistence interface.
#             password_hasher: Password verification service.
#             token_generator: JWT generation service.
#             unit_of_work: Coordinates persistence operations.
#         """
#         self._user_repository = user_repository
#         self._password_hasher = password_hasher
#         self._token_generator = token_generator
#         self._unit_of_work = unit_of_work

#     async def execute(
#         self,
#         command: LoginUserCommand,
#     ) -> LoginUserResult:
#         """
#         Authenticate a user.

#         Args:
#             command: Login request.

#         Raises:
#             InvalidCredentialsException:
#                 Raised when the email or password is invalid.

#         Returns:
#             Authentication result containing the generated access token.
#         """

#         user = await self._user_repository.get_by_email(command.email)

#         if user is None:
#             raise InvalidCredentialsException()

#         password_matches = self._password_hasher.verify(
#             password=command.password,
#             password_hash=user.password_hash,
#         )

#         if not password_matches:
#             raise InvalidCredentialsException()

#         access_token = self._token_generator.generate_access_token(
#             subject=str(user.id),
#         )

#         return LoginUserResult(
#             access_token=access_token,
#         )


"""
Application use case responsible for authenticating a user.

Responsibilities:
    - Validate user credentials.
    - Generate an access token.
    - Generate a refresh token.
    - Persist the refresh token.
    - Commit the authentication transaction.
"""

from __future__ import annotations

from app.auth.application.ports.refresh_token_hasher import (
    RefreshTokenHasher,
)
from app.auth.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.auth.domain.entities.refresh_token import RefreshToken
from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.application.ports.unit_of_work import UnitOfWork
from app.users.application.dto.login_user_command import LoginUserCommand
from app.users.application.dto.login_user_result import LoginUserResult
from app.users.application.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.users.application.ports.user_repository import UserRepository
from app.users.domain.ports.password_hasher import PasswordHasher
from app.users.domain.value_objects.email import Email



class LoginUserUseCase:
    """
    Authenticate an existing user.

    A successful authentication issues both an access token and a
    refresh token. The refresh token is hashed before being persisted
    so that plaintext refresh tokens are never stored in the database.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        refresh_token_hasher: RefreshTokenHasher,
        token_generator: TokenGenerator,
        unit_of_work: UnitOfWork,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_repository:
                User persistence interface.

            refresh_token_repository:
                Refresh token persistence interface.

            password_hasher:
                Password verification service.

            refresh_token_hasher:
                Refresh token hashing service.

            token_generator:
                JWT token generation service.

            unit_of_work:
                Coordinates database transactions.
        """

        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository
        self._password_hasher = password_hasher
        self._refresh_token_hasher = refresh_token_hasher
        self._token_generator = token_generator
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: LoginUserCommand,
    ) -> LoginUserResult:
        """
        Authenticate a user.

        Workflow:
            1. Locate the user.
            2. Verify the supplied password.
            3. Generate an access token.
            4. Generate a refresh token.
            5. Hash the refresh token.
            6. Persist the refresh token.
            7. Commit the transaction.
            8. Return both tokens.

        Raises:
            InvalidCredentialsException:
                Raised when authentication fails.

        Returns:
            LoginUserResult.
        """
        email = Email.create(command.email)

        # Retrieve the user by email.
        user = await self._user_repository.get_by_email(
            email,
        )

        if user is None:
            raise InvalidCredentialsException()

        # Verify the supplied password.
        password_matches = self._password_hasher.verify(
            password=command.password,
            password_hash=user.password_hash,
        )

        if not password_matches:
            raise InvalidCredentialsException()

        # Generate JWT access token.
        access_token = self._token_generator.generate_access_token(
            subject=str(user.id),
        )

        # Generate refresh token and its expiration.
        refresh_token, expires_at = (
            self._token_generator.generate_refresh_token(
                subject=str(user.id),
            )
        )

        # Hash the refresh token before persistence.
        token_hash = self._refresh_token_hasher.hash(
            refresh_token,
        )

        # Create the refresh token aggregate.
        refresh_token_entity = RefreshToken.create(
            user_id=user.id.value,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        try:
            # Persist the refresh token.
            await self._refresh_token_repository.save(
                refresh_token_entity
            )

            # Commit the transaction.
            await self._unit_of_work.commit()

        except Exception:
            await self._unit_of_work.rollback()
            raise

        return LoginUserResult(
            access_token=access_token,
            refresh_token=refresh_token,
        )