"""
Argon2 Password Hasher.

This module contains the infrastructure implementation of the PasswordHasher
port using the Argon2id algorithm.

The domain depends only on the PasswordHasher abstraction and has no knowledge
of Argon2 or any other hashing library.
"""

from argon2 import PasswordHasher as Argon2Hasher
from argon2.exceptions import VerifyMismatchError

from app.users.domain.ports.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    """
    Argon2 implementation of the PasswordHasher contract.

    This class is responsible for hashing plaintext passwords and verifying
    plaintext passwords against stored Argon2 hashes.
    """

    def __init__(self) -> None:
        """
        Initialize the Argon2 password hasher.

        A single PasswordHasher instance is reused because it is designed to
        be thread-safe and avoids unnecessary object creation.
        """
        self._hasher = Argon2Hasher()

    def hash(self, password: str) -> str:
        """
        Hash a plaintext password.

        Args:
            password:
                The plaintext password.

        Returns:
            The generated Argon2 hash.
        """
        return self._hasher.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        """
        Verify a plaintext password against its stored hash.

        Args:
            password:
                Plaintext password supplied by the user.

            password_hash:
                Stored Argon2 password hash.

        Returns:
            True if the password is correct; otherwise False.
        """
        try:
            return self._hasher.verify(password_hash, password)

        except VerifyMismatchError:
            return False