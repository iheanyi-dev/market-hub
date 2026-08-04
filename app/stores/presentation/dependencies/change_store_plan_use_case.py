from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_db_session

from app.stores.infrastructure.persistence.repositories.sqlalchemy_store_repository import (
    SqlAlchemyStoreRepository,
)
from app.stores.application.use_cases.change_store_plan_use_case import (
    ChangeStorePlanUseCase
)
from app.shared.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)

def get_change_store_plan_use_case(
    db_session: AsyncSession = Depends(get_db_session),
) -> ChangeStorePlanUseCase:
    """
    Create a ChangeStorePlanUseCase instance.

    Args:
        db_session:
            Injected asynchronous database session.

    Returns:
        Configured ChangeStorePlanUseCase.
    """

    repository = SqlAlchemyStoreRepository(db_session)

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    return ChangeStorePlanUseCase(
        store_repository=repository,
        unit_of_work=unit_of_work,
    )