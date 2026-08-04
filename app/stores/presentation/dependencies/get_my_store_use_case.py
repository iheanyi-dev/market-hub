"""
Dependency provider for CreateStoreUseCase.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.application.ports.unit_of_work import UnitOfWork
from app.shared.database.session import get_db_session

from app.stores.infrastructure.persistence.repositories.sqlalchemy_store_repository import (
    SqlAlchemyStoreRepository,
)

from app.stores.application.use_cases.get_my_store_use_case import (
    GetMyStoreUseCase
)



async def get_get_my_store_use_case(
    session: AsyncSession = Depends(get_db_session),
) -> GetMyStoreUseCase:
    """
    Create a GetMyStoreUseCase instance.
    """
    repository = SqlAlchemyStoreRepository(session)

    return GetMyStoreUseCase(
        store_repository=repository,
    )