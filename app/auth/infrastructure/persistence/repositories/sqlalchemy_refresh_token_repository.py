"""
SQLAlchemy implementation of the RefreshTokenRepository.

This repository is responsible only for persisting and retrieving
RefreshToken domain entities. It contains no business logic.

Responsibilities:
    - Save a new refresh token.
    - Retrieve a refresh token by its hash.
    - Update an existing refresh token.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.auth.domain.entities.refresh_token import RefreshToken
from app.auth.infrastructure.persistence.mappers.refresh_token_persistence_mapper import (
    RefreshTokenPersistenceMapper,
)
from app.auth.infrastructure.persistence.models.refresh_token_model import (
    RefreshTokenModel,
)


class SqlAlchemyRefreshTokenRepository(RefreshTokenRepository):
    """
    SQLAlchemy implementation of the RefreshTokenRepository.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository.

        Args:
            session: Active SQLAlchemy asynchronous session.
        """
        self._session = session

    async def save(self, refresh_token: RefreshToken) -> None:
        """
        Persist a new refresh token.

        Args:
            refresh_token: Domain refresh token to persist.
        """
        model = RefreshTokenPersistenceMapper.to_model(refresh_token)

        self._session.add(model)

        # Flush synchronizes the pending INSERT with the database
        # without committing the current transaction.
        await self._session.flush()

    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Retrieve a refresh token using its hash.

        Args:
            token_hash: SHA-256 hash of the refresh token.

        Returns:
            The corresponding RefreshToken entity if found,
            otherwise None.
        """
        statement = select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return RefreshTokenPersistenceMapper.to_domain(model)

    async def update(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Persist changes made to an existing refresh token.

        This method updates the database record using the current
        state of the supplied domain entity.

        Args:
            refresh_token: Updated domain refresh token.
        """
        statement = select(RefreshTokenModel).where(
            RefreshTokenModel.id == refresh_token.id
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return

        # Synchronize the ORM model with the current
        # state of the domain entity.
        model.user_id = refresh_token.user_id
        model.token_hash = refresh_token.token_hash
        model.is_revoked = refresh_token.is_revoked
        model.expires_at = refresh_token.expires_at

        # Flush the UPDATE without committing the transaction.
        await self._session.flush()