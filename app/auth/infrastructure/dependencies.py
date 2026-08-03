"""
Dependency providers for the authentication module.

This module wires together the infrastructure and application layers.

Responsibilities:
- Construct authentication use cases.
- Instantiate infrastructure services.
- Inject repositories and shared services.
- Keep FastAPI routers free from construction logic.

Each dependency provider returns a fully configured use case instance.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.application.ports.refresh_token_hasher import (
    RefreshTokenHasher,
)
from app.auth.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.auth.application.use_cases.refresh_token_use_case import (
    RefreshTokenUseCase,
)
from app.auth.infrastructure.persistence.repositories.sqlalchemy_refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)
from app.auth.infrastructure.security.sha256_refresh_token_hasher import (
    SHA256RefreshTokenHasher,
)
from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.application.ports.unit_of_work import UnitOfWork
from app.shared.database.session import (
    get_db_session,
)
from app.shared.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)
from app.shared.infrastructure.security.jwt_token_generator import (
    JwtTokenGenerator,
)
from app.auth.application.use_cases.logout_use_case import (
    LogoutUseCase,
)

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.application.use_cases.get_current_user_use_case import (
    GetCurrentUserUseCase,
)
from app.users.presentation.dependencies import get_user_repository
from app.users.application.ports.user_repository import UserRepository
security = HTTPBearer()



def get_refresh_token_repository(
    session: AsyncSession = Depends(get_db_session),
) -> RefreshTokenRepository:
    """
    Create the refresh token repository.

    Args:
        session:
            Active SQLAlchemy database session.

    Returns:
        RefreshTokenRepository implementation.
    """

    return SqlAlchemyRefreshTokenRepository(session)


def get_refresh_token_hasher() -> RefreshTokenHasher:
    """
    Create the refresh token hasher.

    Returns:
        SHA-256 refresh token hasher.
    """

    return SHA256RefreshTokenHasher()


def get_token_generator() -> TokenGenerator:
    """
    Create the JWT token generator.

    Returns:
        JWT token generator implementation.
    """

    return JwtTokenGenerator()


def get_unit_of_work(
    session: AsyncSession = Depends(get_db_session),
) -> UnitOfWork:
    """
    Create the Unit of Work.

    Args:
        session:
            Active SQLAlchemy database session.

    Returns:
        SQLAlchemy Unit of Work.
    """

    return SqlAlchemyUnitOfWork(session)


def get_refresh_token_use_case(
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository,
    ),
    refresh_token_hasher: RefreshTokenHasher = Depends(
        get_refresh_token_hasher,
    ),
    token_generator: TokenGenerator = Depends(
        get_token_generator,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> RefreshTokenUseCase:
    """
    Construct the RefreshTokenUseCase.

    FastAPI automatically resolves all required dependencies and
    injects them into the use case.

    Returns:
        Fully configured RefreshTokenUseCase.
    """

    return RefreshTokenUseCase(
        refresh_token_repository=refresh_token_repository,
        refresh_token_hasher=refresh_token_hasher,
        token_generator=token_generator,
        unit_of_work=unit_of_work,
    )




def get_logout_use_case(
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository,
    ),
    refresh_token_hasher: RefreshTokenHasher = Depends(
        get_refresh_token_hasher,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> LogoutUseCase:
    """
    Construct the LogoutUseCase.
    """

    return LogoutUseCase(
        refresh_token_repository=refresh_token_repository,
        refresh_token_hasher=refresh_token_hasher,
        unit_of_work=unit_of_work,
    )

def get_current_user_use_case(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    token_generator: TokenGenerator = Depends(
        get_token_generator,
    ),
) -> GetCurrentUserUseCase:
    """
    Construct GetCurrentUserUseCase.
    """

    return GetCurrentUserUseCase(
        user_repository=user_repository,
        token_generator=token_generator,
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    use_case: GetCurrentUserUseCase = Depends(
        get_current_user_use_case,
    ),
):
    """
    Resolve the authenticated user from the Bearer token.
    """
    return await use_case.execute(
        credentials.credentials,
    )