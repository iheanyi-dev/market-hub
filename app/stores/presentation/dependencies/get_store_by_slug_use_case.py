"""
Dependency provider for CreateStoreUseCase.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_db_session

from app.stores.infrastructure.persistence.repositories.sqlalchemy_store_repository import (
    SqlAlchemyStoreRepository,
)

from app.stores.application.use_cases.get_store_by_slug_use_case import (
    GetStoreBySlugUseCase,
)


def get_store_by_slug_use_case(
    db_session: AsyncSession = Depends(get_db_session),
) -> GetStoreBySlugUseCase:
    """
    Create the GetStoreBySlugUseCase dependency.
    """

    repository = SqlAlchemyStoreRepository(db_session)

    return GetStoreBySlugUseCase(repository)