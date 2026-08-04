"""
Application use case for retrieving a store by its public slug.

Responsibilities:

1. Retrieve a store using its slug.
2. Raise an exception if the store does not exist.
3. Return only the public information that may be exposed
   through the API.
"""

from __future__ import annotations

from app.stores.application.dto.get_store_result import GetStoreResult
from app.stores.application.mappers.store_mapper import StoreMapper
from app.stores.domain.exceptions.store_not_found_error import StoreNotFoundError
from app.stores.domain.repositories.store_repository import StoreRepository
from app.stores.domain.value_objects.store_slug import StoreSlug


class GetStoreBySlugUseCase:
    """
    Retrieve a public store by its slug.
    """

    def __init__(
        self,
        store_repository: StoreRepository,
    ) -> None:
        """
        Initialize the use case.

        Args:
            store_repository:
                Repository used to retrieve stores.
        """
        self._store_repository = store_repository

    async def execute(
        self,
        slug: StoreSlug,
    ) -> GetStoreResult:
        """
        Retrieve a store by its public slug.

        Args:
            slug:
                Store slug value object.

        Raises:
            StoreNotFoundError:
                Raised when no matching store exists.

        Returns:
            Public store information.
        """

        store = await self._store_repository.find_by_slug(slug)
        if store is None:
            raise StoreNotFoundError()

        return StoreMapper.to_get_store_result(store)