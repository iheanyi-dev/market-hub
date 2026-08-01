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
from app.shared.application.ports.unit_of_work import UnitOfWork


def get_register_user_use_case(
    repository: SqlAlchemyUserRepository = Depends(
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