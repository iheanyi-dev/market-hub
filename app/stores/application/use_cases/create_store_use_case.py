"""
Create Store Use Case.
"""

from app.shared.application.ports.unit_of_work import UnitOfWork
from app.stores.application.dto.create_store_command import (
    CreateStoreCommand,
)
from app.stores.application.dto.create_store_result import (
    CreateStoreResult,
)
from app.stores.application.mappers.store_mapper import StoreMapper
from app.stores.domain.entities.store import Store
from app.stores.domain.exceptions.store_already_exists_error import (
    StoreAlreadyExistsError,
)
from app.stores.domain.exceptions.store_slug_already_exists_error import (
    StoreSlugAlreadyExistsError,
)
from app.stores.domain.plans.store_plan_factory import StorePlanFactory
from app.stores.domain.repositories.store_repository import StoreRepository
from app.stores.domain.value_objects.store_description import (
    StoreDescription,
)
from app.stores.domain.value_objects.store_name import StoreName
from app.stores.domain.value_objects.store_slug import StoreSlug


class CreateStoreUseCase:
    """
    Creates a new store.
    """

    def __init__(
        self,
        store_repository: StoreRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._store_repository = store_repository
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        command: CreateStoreCommand,
    ) -> CreateStoreResult:
        """
        Create a new store.

        Raises:
            StoreAlreadyExistsError:
                If the owner already has a store.

            StoreSlugAlreadyExistsError:
                If the slug is already in use.
        """
        owner_id = command.user_id
        slug = StoreSlug(command.slug)

        if await self._store_repository.exists_by_owner_id(owner_id):
            raise StoreAlreadyExistsError()

        if await self._store_repository.exists_by_slug(slug):
            raise StoreSlugAlreadyExistsError()

        plan = StorePlanFactory.create(command.plan)

        store = Store.create(
            owner_id=owner_id,
            name=StoreName(command.name),
            slug=slug,
            description=StoreDescription(command.description),
            plan=plan,
        )

        await self._store_repository.save(store)
        await self._unit_of_work.commit()

        return StoreMapper.to_result(store)