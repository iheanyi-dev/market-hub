"""
Store Repository Contract.

Defines the persistence operations required by the Store aggregate.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.stores.domain.entities.store import Store
from app.stores.domain.value_objects.store_id import StoreId
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.users.domain.value_objects.user_id import UserId


class StoreRepository(ABC):
    """
    Contract for Store persistence.
    """

    @abstractmethod
    async def save(self, store: Store) -> None:
        """
        Persist a Store aggregate.
        """

    @abstractmethod
    async def update(self, store: Store) -> None:
        """
        Persist changes made to a Store aggregate.
        """

    @abstractmethod
    async def find_by_id(self, store_id: StoreId) -> Store | None:
        """
        Retrieve a Store by its identifier.
        """

    @abstractmethod
    async def find_by_owner_id(
        self,
        owner_id: UserId,
    ) -> Store | None:
        """
        Retrieve a Store by its owner.
        """

    @abstractmethod
    async def find_by_slug(
        self,
        slug: StoreSlug,
    ) -> Store | None:
        """
        Retrieve a Store by its slug.
        """

    @abstractmethod
    async def exists_by_owner_id(
        self,
        owner_id: UserId,
    ) -> bool:
        """
        Determine whether a user already owns a Store.
        """

    @abstractmethod
    async def exists_by_slug(
        self,
        slug: StoreSlug,
    ) -> bool:
        """
        Determine whether a slug is already in use.
        """