"""
Application use case for updating the authenticated user's store.

Responsibilities:
1. Retrieve the authenticated user's store.
2. Update mutable store attributes.
3. Persist the changes.
4. Return the updated store.
"""

from __future__ import annotations

from app.shared.application.ports.unit_of_work import UnitOfWork
from app.stores.application.dto.get_my_store_result import GetMyStoreResult
from app.stores.application.dto.update_my_store_command import (
    UpdateMyStoreCommand,
)
from app.stores.application.mappers.store_mapper import StoreMapper
from app.stores.domain.exceptions.store_not_found_error import (
    StoreNotFoundError,
)
from app.stores.domain.repositories.store_repository import (
    StoreRepository,
)
from app.stores.domain.value_objects.store_name import StoreName


class UpdateMyStoreUseCase:
    """
    Update the authenticated user's store.
    """

    def __init__(
        self,
        store_repository: StoreRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        """
        Initialize the use case.

        Args:
            store_repository:
                Repository used to retrieve and persist stores.

            unit_of_work:
                Coordinates committing the transaction.
        """

        self._store_repository = store_repository
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: UpdateMyStoreCommand,
    ) -> GetMyStoreResult:
        """
        Update the authenticated user's store.

        Args:
            command:
                Validated update command.

        Raises:
            StoreNotFoundError:
                If the authenticated user does not own a store.

        Returns:
            The updated store.
        """

        store = await self._store_repository.find_by_owner_id(
            command.owner_id,
        )

        if store is None:
            raise StoreNotFoundError()

        store.update(
            name=StoreName.create(command.name),
            description=command.description,
        )

        await self._store_repository.update(store)

        await self._unit_of_work.commit()

        return StoreMapper.to_result(store)