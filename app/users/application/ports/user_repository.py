"""
User Repository Port.

This module defines the contract for persisting and retrieving users.

The application layer depends on this abstraction rather than a concrete
database implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from uuid import UUID

class UserRepository(ABC):
    """
    Defines the contract for user persistence.
    """

    @abstractmethod
    async def save(self, user: User) -> None:
        """
        Persist a user.

        Args:
            user:
                The user aggregate to persist.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """
        Determine whether a user already exists with the given email.

        Args:
            email:
                The email to search for.

        Returns:
            True if a matching user exists; otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        """
        Retrieve a user by email.

        Args:
            email:
                The user's email.

        Returns:
            A User if found; otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> User | None:
        """
        Retrieve a user by id.

        Args:
            id:
                The user's id.

        Returns:
            A User if found; otherwise None.
        """
        raise NotImplementedError