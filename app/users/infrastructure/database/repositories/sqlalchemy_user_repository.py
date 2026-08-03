"""
SQLAlchemy implementation of the UserRepository.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.application.ports.user_repository import UserRepository
from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.infrastructure.database.mappers.user_persistence_mapper import (
    UserPersistenceMapper,
)
from app.shared.database.models.user_model import UserModel
from uuid import UUID

class SqlAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of the UserRepository contract.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """
        Initialize the repository.

        Args:
            session:
                SQLAlchemy asynchronous database session.
        """
        self._session = session

    async def save(
        self,
        user: User,
    ) -> None:
        """
        Persist a user.
        """
        model = UserPersistenceMapper.to_model(user)

        self._session.add(model)

        await self._session.flush()

    async def exists_by_email(
        self,
        email: Email,
    ) -> bool:
        """
        Determine whether a user exists with the supplied email.
        """
        statement = (
            select(UserModel.id)
            .where(UserModel.email == email.value)
            .limit(1)
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def get_by_email(
        self,
        email: Email,
    ) -> User | None:
        """
        Retrieve a user by email.
        """
        statement = (
            select(UserModel)
            .where(UserModel.email == email.value)
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserPersistenceMapper.to_domain(model)

    async def get_by_id(self, id: UUID) -> User | None:
        """
            Retrieve a user by email.
        """
        statement = (
            select(UserModel)
            .where(UserModel.id == id)
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None
        return UserPersistenceMapper.to_domain(model)
