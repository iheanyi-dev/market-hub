"""
Contract for generating and validating authentication tokens.

The application layer depends on this abstraction and is independent
of the underlying token implementation (e.g. JWT).
"""

from abc import ABC, abstractmethod


class TokenGenerator(ABC):
    """
    Defines the operations required for token management.
    """

    @abstractmethod
    def generate_access_token(
        self,
        subject: str,
    ) -> str:
        """
        Generate an access token.

        Args:
            subject: Unique identifier of the authenticated user.

        Returns:
            Encoded access token.
        """
        raise NotImplementedError

    @abstractmethod
    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Decode and validate an access token.

        Args:
            token: Encoded JWT.

        Returns:
            Decoded token payload.

        Raises:
            Exception:
                If the token is invalid or expired.
        """
        raise NotImplementedError