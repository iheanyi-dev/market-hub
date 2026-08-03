"""
Application contract for authentication token management.

The application layer depends only on this abstraction and remains
independent of the JWT implementation.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class TokenGenerator(ABC):
    """
    Defines the operations required for authentication token management.
    """

    @abstractmethod
    def generate_access_token(
        self,
        subject: str,
    ) -> str:
        """
        Generate a signed JWT access token.
        """
        raise NotImplementedError

    @abstractmethod
    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Decode and validate an access token.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_refresh_token(
        self,
        subject: str,
    ) -> tuple[str, datetime]:
        """
        Generate a refresh token.

        Returns:
            A tuple containing:

            - The encoded refresh token.
            - The expiration timestamp.
        """
        raise NotImplementedError

    @abstractmethod
    def decode_refresh_token(
        self,
        token: str,
    ) -> dict:
        """
        Decode and validate a refresh token.
        """
        raise NotImplementedError