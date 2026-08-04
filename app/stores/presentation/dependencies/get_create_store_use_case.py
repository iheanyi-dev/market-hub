"""
Dependency provider for CreateStoreUseCase.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.application.ports.unit_of_work import UnitOfWork
from app.shared.database.session import get_db_session
from app.shared.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)
from app.stores.application.use_cases.create_store_use_case import (
    CreateStoreUseCase,
)
from app.stores.infrastructure.persistence.repositories.sqlalchemy_store_repository import (
    SqlAlchemyStoreRepository,
)


async def get_create_store_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> CreateStoreUseCase:
    """
    Create a CreateStoreUseCase instance.
    """
    repository = SqlAlchemyStoreRepository(session)

    unit_of_work: UnitOfWork = SqlAlchemyUnitOfWork(session)

    return CreateStoreUseCase(
        store_repository=repository,
        unit_of_work=unit_of_work,
    )