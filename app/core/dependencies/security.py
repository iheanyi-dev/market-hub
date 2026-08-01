"""
Security dependency providers.
"""

from app.users.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)


def get_password_hasher() -> Argon2PasswordHasher:
    """
    Provide the password hasher.
    """

    return Argon2PasswordHasher()