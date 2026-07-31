"""
Password Hasher Port.

This module defines the contract for password hashing.

The domain should never depend on a concrete hashing implementation such as
Argon2 or bcrypt. Instead, it depends on this abstraction, allowing the
infrastructure layer to provide the actual implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """
    Contract for password hashing services.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """
        Hash a plaintext password.

        Args:
            password: The plaintext password.

        Returns:
            The hashed password.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """
        Verify a plaintext password against a stored hash.

        Args:
            password: Plaintext password.
            password_hash: Stored password hash.

        Returns:
            True if the password matches.
        """
        raise NotImplementedError