"""
Application use case for changing the authenticated user's
store subscription plan.
"""

from __future__ import annotations

from app.shared.application.ports.unit_of_work import UnitOfWork
from app.stores.application.dto.change_store_plan_command import (
    ChangeStorePlanCommand,
)
from app.stores.application.dto.get_my_store_result import (
    GetMyStoreResult,
)
from app.stores.application.mappers.store_mapper import StoreMapper
from app.stores.domain.exceptions.store_not_found_error import (
    StoreNotFoundError,
)
from app.stores.domain.repositories.store_repository import (
    StoreRepository,
)
from app.stores.domain.plans.store_plan import StorePlan
from app.stores.domain.plans.store_plan_factory import StorePlanFactory

class ChangeStorePlanUseCase:
    """
    Change the authenticated user's store subscription plan.
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
        command: ChangeStorePlanCommand,
    ) -> GetMyStoreResult:
        """
        Change the authenticated user's store plan.

        Args:
            command:
                Application command.

        Raises:
            StoreNotFoundError:
                If the authenticated user does not own a store.

        Returns:
            Updated store.
        """

        store = await self._store_repository.find_by_owner_id(
            command.owner_id,
        )

        if store is None:
            raise StoreNotFoundError()

        store.change_plan(
            StorePlanFactory.create(command.plan),
        )

        await self._store_repository.update(store)

        await self._unit_of_work.commit()

        return StoreMapper.to_result(store)