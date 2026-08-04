"""
SQLAlchemy implementation of StoreRepository.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.stores.domain.entities.store import Store
from app.stores.domain.repositories.store_repository import StoreRepository
from app.stores.domain.value_objects.store_id import StoreId
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.stores.infrastructure.persistence.mappers.store_persistence_mapper import (
    StorePersistenceMapper,
)
from app.stores.infrastructure.persistence.models.store_model import StoreModel
from app.users.domain.value_objects.user_id import UserId
from app.stores.domain.exceptions.store_not_found_error import (
    StoreNotFoundError
)


class SqlAlchemyStoreRepository(StoreRepository):
    """
    SQLAlchemy implementation of StoreRepository.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, store: Store) -> None:
        """
        Persist a new Store.
        """
        self._session.add(
            StorePersistenceMapper.to_model(store)
        )

    async def update(
    self,
    store: Store,
    ) -> None:
        """
        Persist updates made to an existing store.

        Args:
            store:
                Updated Store aggregate.

        Raises:
            StoreNotFoundError:
                If the store no longer exists.
        """

        statement = select(StoreModel).where(
            StoreModel.id == store.id.value,
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            raise StoreNotFoundError()

        StorePersistenceMapper.update_model(
            model=model,
            store=store,
        )

        await self._session.flush()

    async def find_by_id(
        self,
        store_id: StoreId,
    ) -> Store | None:
        """
        Retrieve a Store by its identifier.
        """
        model = await self._session.get(
            StoreModel,
            store_id.value,
        )

        if model is None:
            return None

        return StorePersistenceMapper.to_domain(model)

    async def find_by_owner_id(
        self,
        owner_id: UserId,
    ) -> Store | None:
        """
        Retrieve a Store by its owner.
        """
        result = await self._session.execute(
            select(StoreModel).where(
                StoreModel.owner_id == owner_id.value
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return StorePersistenceMapper.to_domain(model)

    async def find_by_slug(
        self,
        slug: StoreSlug,
    ) -> Store | None:
        """
        Retrieve a Store by its slug.
        """
        result = await self._session.execute(
            select(StoreModel).where(
                StoreModel.slug == slug.value
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return StorePersistenceMapper.to_domain(model)

    async def exists_by_owner_id(
        self,
        owner_id: UserId,
    ) -> bool:
        """
        Determine whether a user already owns a store.
        """
        result = await self._session.execute(
            select(StoreModel.id).where(
                StoreModel.owner_id == owner_id.value
            )
        )

        return result.scalar_one_or_none() is not None

    async def exists_by_slug(
        self,
        slug: StoreSlug,
    ) -> bool:
        """
        Determine whether a slug already exists.
        """
        result = await self._session.execute(
            select(StoreModel.id).where(
                StoreModel.slug == slug.value
            )
        )

        return result.scalar_one_or_none() is not None