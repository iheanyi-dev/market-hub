"""
Fake Password Hasher.

This fake implementation is used during unit testing.
"""

from app.users.domain.ports.password_hasher import PasswordHasher


class FakePasswordHasher(PasswordHasher):
    """
    Fake implementation of the PasswordHasher port.
    """

    async def hash(self, password: str) -> str:
        """
        Return a deterministic password hash.
        """
        return f"hashed::{password}"

    async def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verify the supplied password.
        """
        return password_hash == f"hashed::{password}"