from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_db_session
from app.shared.infrastructure.database.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


def get_unit_of_work(
    session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyUnitOfWork:
    """
    Provide a SQLAlchemy Unit of Work.
    """
    return SqlAlchemyUnitOfWork(session)