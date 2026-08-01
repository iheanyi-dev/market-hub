from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_db_session
from app.shared.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


async def get_unit_of_work(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    """
    Provide a Unit of Work backed by the current database session.
    """
    yield SqlAlchemyUnitOfWork(session)