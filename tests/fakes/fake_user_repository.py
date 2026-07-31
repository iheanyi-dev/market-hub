"""
Fake User Repository.

This in-memory repository is used for unit testing application use cases.
"""

from app.users.application.ports.user_repository import UserRepository
from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email


class FakeUserRepository(UserRepository):
    """
    In-memory implementation of the UserRepository contract.
    """

    def __init__(self) -> None:
        """
        Initialize an empty repository.
        """
        self._users: list[User] = []

    async def save(self, user: User) -> None:
        """
        Store a user in memory.
        """
        self._users.append(user)

    async def exists_by_email(self, email: Email) -> bool:
        """
        Determine whether a user with the supplied email exists.
        """
        return any(user.email == email for user in self._users)

    async def get_by_email(self, email: Email) -> User | None:
        """
        Retrieve a user by email.
        """
        for user in self._users:
            if user.email == email:
                return user

        return None