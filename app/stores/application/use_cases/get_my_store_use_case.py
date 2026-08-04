"""
Get My Store Use Case.

Retrieves the authenticated user's store.
"""

from app.stores.application.dto.get_my_store_result import (
    GetMyStoreResult,
)
from app.stores.domain.exceptions.store_not_found_error import (
    StoreNotFoundError,
)
from app.stores.domain.repositories.store_repository import (
    StoreRepository,
)
from app.users.domain.value_objects.user_id import UserId


class GetMyStoreUseCase:
    """
    Retrieves the store belonging to an authenticated user.
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
        user_id: UserId,
    ) -> GetMyStoreResult:
        """
        Retrieve the authenticated user's store.

        Args:
            user_id:
                Identifier of the authenticated user.

        Returns:
            Details of the user's store.

        Raises:
            StoreNotFoundError:
                If the user does not own a store.
        """

        store = await self._store_repository.find_by_owner_id(
            user_id
        )

        if store is None:
            raise StoreNotFoundError()

        return GetMyStoreResult(
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