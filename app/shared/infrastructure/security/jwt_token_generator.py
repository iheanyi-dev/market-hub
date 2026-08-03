"""
JWT token generator implementation.

This module provides the concrete implementation of the TokenGenerator
application port using JSON Web Tokens (JWT).

Responsibilities:
- Generate access tokens.
- Validate access tokens.
- Generate refresh tokens.
- Validate refresh tokens.

The application layer depends only on the TokenGenerator interface and
never directly on the JWT library.
"""

from datetime import UTC, datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.shared.application.ports.token_generator import TokenGenerator
from app.shared.config.settings import settings
from datetime import UTC, datetime, timedelta

class JwtTokenGenerator(TokenGenerator):
    """
    JWT implementation of the TokenGenerator interface.
    """

    def generate_access_token(
        self,
        subject: str,
    ) -> str:
        """
        Generate a signed JWT access token.

        Access tokens are short-lived credentials used to authorize
        protected API requests.

        Args:
            subject:
                Unique identifier of the authenticated user.

        Returns:
            Encoded JWT access token.
        """

        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        payload = {
            "sub": subject,
            "exp": expires_at,
            "type": "access",
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
            token:
                Encoded JWT access token.

        Returns:
            Decoded JWT payload.

        Raises:
            InvalidTokenError:
                If the token is invalid, expired, or is not an
                access token.
        """

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            if payload.get("type") != "access":
                raise InvalidTokenError("Invalid access token.")

            return payload

        except ExpiredSignatureError as exc:
            raise InvalidTokenError("Access token has expired.") from exc

        except InvalidTokenError as exc:
            raise InvalidTokenError("Invalid access token.") from exc

    def generate_refresh_token(
        self,
        subject: str,
    ) -> tuple[str, datetime]:
        """
        Generate a signed JWT refresh token.

        Unlike access tokens, refresh tokens have a much longer lifetime
        and are used to obtain new access tokens without requiring the
        user to authenticate again.

        Args:
            subject:
                Unique identifier of the authenticated user.

        Returns:
            A tuple containing:

            - Encoded refresh token.
            - Refresh token expiration timestamp.
        """

        expires_at = datetime.now(UTC) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )

        payload = {
            "sub": subject,
            "exp": expires_at,
            "type": "refresh",
        }

        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        return token, expires_at

    def decode_refresh_token(
        self,
        token: str,
    ) -> dict:
        """
        Validate and decode a refresh token.

        Args:
            token:
                Encoded JWT refresh token.

        Returns:
            Decoded JWT payload.

        Raises:
            InvalidTokenError:
                If the token is invalid, expired, or is not a
                refresh token.
        """

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            if payload.get("type") != "refresh":
                raise InvalidTokenError("Invalid refresh token.")

            return payload

        except ExpiredSignatureError as exc:
            raise InvalidTokenError("Refresh token has expired.") from exc

        except InvalidTokenError as exc:
            raise InvalidTokenError("Invalid refresh token.") from exc