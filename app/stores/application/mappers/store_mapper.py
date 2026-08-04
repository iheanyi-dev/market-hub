"""
Store Mapper.

Maps Store aggregates to application DTOs.
"""

from app.stores.application.dto.create_store_result import (
    CreateStoreResult,
)
from app.stores.domain.entities.store import Store


class StoreMapper:
    """
    Maps Store domain objects to application DTOs.
    """

    @staticmethod
    def to_result(store: Store) -> CreateStoreResult:
        """
        Convert a Store aggregate into a CreateStoreResult.
        """
        return CreateStoreResult(
            id=str(store.id),
            owner_id=str(store.owner_id),
            name=str(store.name),
            slug=str(store.slug),
            description=str(store.description),
            plan=store.plan.code,
            product_count=store.product_count,
            status=store.status.value,
            created_at=store.created_at,
            updated_at=store.updated_at,
        )