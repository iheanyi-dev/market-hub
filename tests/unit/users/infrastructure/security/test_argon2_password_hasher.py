"""
Unit tests for the Argon2 password hasher.
"""

from app.users.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)


class TestArgon2PasswordHasher:
    """
    Test suite for the Argon2 password hasher.
    """

    def test_hash_returns_different_value(self) -> None:
        """
        Hashing should never return the original plaintext password.
        """
        hasher = Argon2PasswordHasher()

        raw_password = "StrongPass@123"

        password_hash = hasher.hash(raw_password)

        assert password_hash != raw_password

    def test_verify_returns_true_for_valid_password(self) -> None:
        """
        Verification should succeed for the correct password.
        """
        hasher = Argon2PasswordHasher()

        raw_password = "StrongPass@123"

        password_hash = hasher.hash(raw_password)

        assert hasher.verify(raw_password, password_hash) is True

    def test_verify_returns_false_for_invalid_password(self) -> None:
        """
        Verification should fail for an incorrect password.
        """
        hasher = Argon2PasswordHasher()

        password_hash = hasher.hash("StrongPass@123")

        assert hasher.verify("WrongPassword@123", password_hash) is False