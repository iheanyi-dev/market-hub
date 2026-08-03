"""
SHA-256 implementation of the RefreshTokenHasher.

This implementation performs deterministic hashing of refresh tokens using
SHA-256.

Unlike passwords, refresh tokens are high-entropy randomly generated
values, making SHA-256 suitable for this purpose. Password-specific
algorithms such as Argon2 or bcrypt are unnecessary here because refresh
tokens are not user-chosen secrets.
"""

from hashlib import sha256

from app.auth.application.ports.refresh_token_hasher import (
    RefreshTokenHasher,
)


class SHA256RefreshTokenHasher(RefreshTokenHasher):
    """
    SHA-256 implementation of refresh token hashing.
    """

    def hash(
        self,
        token: str,
    ) -> str:
        """
        Hash a refresh token.

        Args:
            token:
                Raw refresh token.

        Returns:
            SHA-256 hexadecimal digest.
        """

        return sha256(token.encode("utf-8")).hexdigest()

    def verify(
        self,
        token: str,
        token_hash: str,
    ) -> bool:
        """
        Verify that a refresh token matches its stored hash.

        Args:
            token:
                Raw refresh token.

            token_hash:
                Stored SHA-256 hash.

        Returns:
            True when the hashes match.
        """

        return self.hash(token) == token_hash