"""
Unit tests for GetMyStoreUseCase.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from app.stores.application.use_cases.get_my_store_use_case import (
    GetMyStoreUseCase,
)
from app.stores.domain.entities.store import Store
from app.stores.domain.exceptions.store_not_found_error import (
    StoreNotFoundError,
)
from app.stores.domain.plans.store_plan_factory import (
    StorePlanFactory,
)
from app.stores.domain.value_objects.store_description import (
    StoreDescription,
)
from app.stores.domain.value_objects.store_name import StoreName
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.users.domain.value_objects.user_id import UserId


@pytest.fixture
def repository() -> AsyncMock:
    """
    Create a mocked store repository.
    """
    return AsyncMock()


@pytest.fixture
def use_case(
    repository: AsyncMock,
) -> GetMyStoreUseCase:
    """
    Create the use case.
    """
    return GetMyStoreUseCase(repository)


@pytest.fixture
def store() -> Store:
    """
    Create a sample store.
    """
    return Store.reconstitute(
        store_id=Store.create(
            owner_id=UserId.create(),
            name=StoreName.create("My Store"),
            slug=StoreSlug.create("my-store"),
            description=StoreDescription.create(
                "Description",
            ),
            plan=StorePlanFactory.create("starter"),
        ).id,
        owner_id=UserId.create(),
        name=StoreName.create("My Store"),
        slug=StoreSlug.create("my-store"),
        description=StoreDescription.create(
            "Description",
        ),
        plan=StorePlanFactory.create("starter"),
        product_count=0,
        status=Store.create(
            owner_id=UserId.create(),
            name=StoreName.create("Dummy"),
            slug=StoreSlug.create("dummy"),
            description=StoreDescription.create("Dummy"),
            plan=StorePlanFactory.create("starter"),
        ).status,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_get_my_store(
    use_case: GetMyStoreUseCase,
    repository: AsyncMock,
    store: Store,
) -> None:
    """
    Verify that a user's store can be retrieved.
    """

    repository.find_by_owner_id.return_value = store

    result = await use_case.execute(
        store.owner_id,
    )

    assert result.id == store.id.value
    assert result.owner_id == store.owner_id.value
    assert result.name == "My Store"
    assert result.slug == "my-store"


@pytest.mark.asyncio
async def test_store_not_found(
    use_case: GetMyStoreUseCase,
    repository: AsyncMock,
) -> None:
    """
    Verify an exception is raised when the user
    does not own a store.
    """

    repository.find_by_owner_id.return_value = None

    with pytest.raises(StoreNotFoundError):
        await use_case.execute(
            UserId.create(),
        )