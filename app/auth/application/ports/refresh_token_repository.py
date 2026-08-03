from abc import ABC, abstractmethod

from app.auth.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):
    """
    Contract for refresh token persistence.
    """

    @abstractmethod
    async def save(self, refresh_token: RefreshToken) -> None:
        """
        Persist a refresh token.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Retrieve a refresh token by its hash.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        refresh_token: RefreshToken,
    ) -> None:
        """
        Persist changes to a refresh token.
        """
        raise NotImplementedError

