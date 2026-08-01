"""
Application use case responsible for authenticating a user.

The use case validates the supplied credentials, generates an access
token for authenticated users, and returns the authentication result.
"""

from app.users.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.application.ports.unit_of_work import UnitOfWork
from app.users.application.dto.login_user_command import LoginUserCommand
from app.users.application.dto.login_user_result import LoginUserResult
from app.users.application.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.users.application.ports.user_repository import UserRepository


class LoginUserUseCase:
    """
    Authenticate a registered user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: Argon2PasswordHasher,
        token_generator: TokenGenerator,
        unit_of_work: UnitOfWork,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_repository: User persistence interface.
            password_hasher: Password verification service.
            token_generator: JWT generation service.
            unit_of_work: Coordinates persistence operations.
        """
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_generator = token_generator
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: LoginUserCommand,
    ) -> LoginUserResult:
        """
        Authenticate a user.

        Args:
            command: Login request.

        Raises:
            InvalidCredentialsException:
                Raised when the email or password is invalid.

        Returns:
            Authentication result containing the generated access token.
        """

        user = await self._user_repository.get_by_email(command.email)

        if user is None:
            raise InvalidCredentialsException()

        password_matches = self._password_hasher.verify(
            password=command.password,
            password_hash=user.password_hash,
        )

        if not password_matches:
            raise InvalidCredentialsException()

        access_token = self._token_generator.generate_access_token(
            subject=str(user.id),
        )

        return LoginUserResult(
            access_token=access_token,
        )