"""
Security dependency providers.
"""

from app.users.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)

from app.shared.infrastructure.security.jwt_token_generator import (
    JwtTokenGenerator,
)

from app.shared.application.ports.token_generator import TokenGenerator

def get_password_hasher() -> Argon2PasswordHasher:
    """
    Provide the password hasher.
    """

    return Argon2PasswordHasher()


def get_token_generator() -> TokenGenerator:
    """
    Return the application's token generator.
    """
    return JwtTokenGenerator()