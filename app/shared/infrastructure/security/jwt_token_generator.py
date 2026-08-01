"""
JWT token provider implementation.

This module is responsible for generating and validating JSON Web Tokens
used for authenticating users.
"""

from datetime import UTC, datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.config.settings import settings


class JwtTokenGenerator(TokenGenerator):
    """
    JWT implementation of the TokenProvider interface.
    """

    def generate_access_token(
        self,
        subject: str,
    ) -> str:
        """
        Generate a signed JWT access token.

        Args:
            subject: Unique identifier of the authenticated user.

        Returns:
            Encoded JWT access token.
        """

        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        payload = {
            "sub": subject,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Validate and decode an access token.

        Args:
            token: Encoded JWT.

        Returns:
            Decoded JWT payload.

        Raises:
            InvalidTokenError:
                If the token is invalid or has expired.
        """

        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

        except ExpiredSignatureError as exc:
            raise InvalidTokenError("Token has expired.") from exc

        except InvalidTokenError as exc:
            raise InvalidTokenError("Invalid token.") from exc