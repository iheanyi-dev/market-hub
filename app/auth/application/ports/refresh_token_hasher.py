"""
Application contract for hashing refresh tokens.

The application layer depends only on this abstraction and is completely
independent of the hashing algorithm used by the infrastructure layer.

Refresh tokens are never stored in plaintext. Instead, a one-way hash of
the token is persisted in the database. During authentication, the
incoming token is hashed again and compared with the stored hash.
"""

from abc import ABC, abstractmethod


class RefreshTokenHasher(ABC):
    """
    Defines the operations required for refresh token hashing.
    """

    @abstractmethod
    def hash(
        self,
        token: str,
    ) -> str:
        """
        Produce a deterministic hash of a refresh token.

        Args:
            token:
                Raw refresh token.

        Returns:
            Hexadecimal hash of the refresh token.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(
        self,
        token: str,
        token_hash: str,
    ) -> bool:
        """
        Verify that a refresh token matches a stored hash.

        Args:
            token:
                Raw refresh token supplied by the client.

            token_hash:
                Stored hash retrieved from persistence.

        Returns:
            True if both hashes match, otherwise False.
        """
        raise NotImplementedError