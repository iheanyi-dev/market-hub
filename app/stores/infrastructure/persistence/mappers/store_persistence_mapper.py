"""
Store Persistence Mapper.

Maps between the Store domain aggregate and the SQLAlchemy StoreModel.
"""

from app.stores.domain.entities.store import Store
from app.stores.domain.enums.store_status import StoreStatus
from app.stores.domain.plans.store_plan_factory import StorePlanFactory
from app.stores.domain.value_objects.store_description import (
    StoreDescription,
)
from app.stores.domain.value_objects.store_id import StoreId
from app.stores.domain.value_objects.store_name import StoreName
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.stores.infrastructure.persistence.models.store_model import (
    StoreModel,
)
from app.users.domain.value_objects.user_id import UserId


class StorePersistenceMapper:
    """
    Maps between Store aggregates and StoreModel.
    """

    @staticmethod
    def to_model(store: Store) -> StoreModel:
        """
        Convert a Store aggregate into a StoreModel.
        """
        return StoreModel(
            id=store.id.value,
            owner_id=store.owner_id.value,
            name=store.name.value,
            slug=store.slug.value,
            description=store.description.value,
            plan=store.plan.code,
            product_count=store.product_count,
            status=store.status.value,
            created_at=store.created_at,
            updated_at=store.updated_at,
        )

    @staticmethod
    def to_domain(model: StoreModel) -> Store:
        """
        Convert a StoreModel into a Store aggregate.
        """
        return Store.reconstitute(
            store_id=StoreId(model.id),
            owner_id=UserId(model.owner_id),
            name=StoreName(model.name),
            slug=StoreSlug(model.slug),
            description=StoreDescription(model.description),
            plan=StorePlanFactory.create(model.plan),
            product_count=model.product_count,
            status=StoreStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )