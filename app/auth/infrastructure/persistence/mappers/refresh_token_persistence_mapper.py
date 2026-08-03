"""
Refresh Token Persistence Mapper.

This module is responsible for converting between the domain
RefreshToken entity and the SQLAlchemy RefreshTokenModel.

The mapper acts as an anti-corruption layer between the
domain and persistence layers, ensuring the domain remains
independent of SQLAlchemy.
"""

from app.auth.domain.entities.refresh_token import RefreshToken
from app.auth.infrastructure.persistence.models.refresh_token_model import (
    RefreshTokenModel,
)


class RefreshTokenPersistenceMapper:
    """
    Maps RefreshToken domain entities to persistence models and
    vice versa.

    The domain layer should never work directly with SQLAlchemy
    models. Likewise, the persistence layer should not contain
    business logic.
    """

    @staticmethod
    def to_model(entity: RefreshToken) -> RefreshTokenModel:
        """
        Convert a domain RefreshToken entity into its SQLAlchemy model.

        Args:
            entity: The domain refresh token.

        Returns:
            A SQLAlchemy RefreshTokenModel ready for persistence.
        """
        return RefreshTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            is_revoked=entity.is_revoked,
            expires_at=entity.expires_at,
        )

    @staticmethod
    def to_domain(model: RefreshTokenModel) -> RefreshToken:
        """
        Convert a SQLAlchemy RefreshTokenModel into a domain entity.

        Args:
            model: The SQLAlchemy refresh token model.

        Returns:
            A RefreshToken domain entity.
        """
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            is_revoked=model.is_revoked,
            expires_at=model.expires_at,
        )