"""
Use case dependency providers.
"""

from fastapi import Depends

from app.core.dependencies.repositories import (
    get_user_repository,
)
from app.core.dependencies.security import (
    get_password_hasher,
)
from app.users.application.use_cases.register_user_use_case import (
    RegisterUserUseCase,
)
from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from app.users.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)

from app.core.dependencies.unit_of_work import (
    get_unit_of_work,
)
from app.shared.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.auth.infrastructure.dependencies import (
    get_refresh_token_hasher, get_refresh_token_repository
)
from app.shared.application.ports.unit_of_work import UnitOfWork
from app.auth.application.ports.refresh_token_hasher import (
    RefreshTokenHasher
)
from app.auth.application.ports.refresh_token_repository import (
    RefreshTokenRepository
)
from app.core.dependencies.security import get_token_generator
# from app.core.dependencies.shared import (
#     get_password_hasher,
#     get_unit_of_work,
# )
from app.users.application.use_cases.login_user_use_case import (
    LoginUserUseCase,
)
from app.users.domain.ports.password_hasher import PasswordHasher
from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.application.ports.unit_of_work import UnitOfWork
from app.users.application.ports.user_repository import UserRepository

def get_register_user_use_case(
    repository: UserRepository = Depends(
        get_user_repository,
    ),
    password_hasher: Argon2PasswordHasher = Depends(
        get_password_hasher,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> RegisterUserUseCase:
    """
    Provide RegisterUserUseCase.
    """

    return RegisterUserUseCase(
        repository=repository,
        password_hasher=password_hasher,
        unit_of_work=unit_of_work,
    )


"""
Login use case dependency.
"""

def get_login_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_generator: TokenGenerator = Depends(get_token_generator),
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
    refresh_token_hasher: RefreshTokenHasher = Depends(
        get_refresh_token_hasher
    )
) -> LoginUserUseCase:
    """
    Create and return the login use case.
    """

    return LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_generator=token_generator,
        unit_of_work=unit_of_work,
        refresh_token_repository=refresh_token_repository,
        refresh_token_hasher=refresh_token_hasher
    )