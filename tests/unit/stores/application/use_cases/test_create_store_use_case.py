"""
Unit tests for CreateStoreUseCase.
"""

from unittest.mock import AsyncMock

import pytest

from app.shared.application.ports.unit_of_work import UnitOfWork
from app.stores.application.dto.create_store_command import CreateStoreCommand
from app.stores.application.use_cases.create_store_use_case import (
    CreateStoreUseCase,
)
from app.stores.domain.entities.store import Store
from app.stores.domain.exceptions.store_already_exists_error import (
    StoreAlreadyExistsError,
)
from app.stores.domain.exceptions.store_slug_already_exists_error import (
    StoreSlugAlreadyExistsError,
)
from app.stores.domain.plans.starter_plan import StarterPlan
from app.stores.domain.repositories.store_repository import StoreRepository
from app.users.domain.value_objects.user_id import UserId


@pytest.fixture
def repository() -> AsyncMock:
    """
    Create a mocked StoreRepository.
    """
    return AsyncMock(spec=StoreRepository)


@pytest.fixture
def unit_of_work() -> AsyncMock:
    """
    Create a mocked UnitOfWork.
    """
    return AsyncMock(spec=UnitOfWork)


@pytest.fixture
def use_case(
    repository: AsyncMock,
    unit_of_work: AsyncMock,
) -> CreateStoreUseCase:
    """
    Create the use case under test.
    """
    return CreateStoreUseCase(
        store_repository=repository,
        unit_of_work=unit_of_work,
    )


@pytest.fixture
def command() -> CreateStoreCommand:
    """
    Valid command used by multiple tests.
    """
    return CreateStoreCommand(
        owner_id= UserId.create(),
        name="My Store",
        slug="my-store",
        description="My first store.",
        plan="starter",
    )


async def test_create_store(
    use_case: CreateStoreUseCase,
    repository: AsyncMock,
    unit_of_work: AsyncMock,
    command: CreateStoreCommand,
) -> None:
    """
    A store should be created successfully.
    """
    repository.exists_by_owner_id.return_value = False
    repository.exists_by_slug.return_value = False

    result = await use_case.execute(command)

    repository.save.assert_awaited_once()
    unit_of_work.commit.assert_awaited_once()

    assert result.name == "My Store"
    assert result.slug == "my-store"
    assert result.description == "My first store."
    assert result.plan == "Starter"
    assert result.product_count == 0


async def test_create_store_when_owner_already_has_store(
    use_case: CreateStoreUseCase,
    repository: AsyncMock,
    command: CreateStoreCommand,
) -> None:
    """
    A user cannot own more than one store.
    """
    repository.exists_by_owner_id.return_value = True

    with pytest.raises(StoreAlreadyExistsError):
        await use_case.execute(command)


async def test_create_store_when_slug_exists(
    use_case: CreateStoreUseCase,
    repository: AsyncMock,
    command: CreateStoreCommand,
) -> None:
    """
    Store slugs must be unique.
    """
    repository.exists_by_owner_id.return_value = False
    repository.exists_by_slug.return_value = True

    with pytest.raises(StoreSlugAlreadyExistsError):
        await use_case.execute(command)


async def test_created_store_is_persisted(
    use_case: CreateStoreUseCase,
    repository: AsyncMock,
    command: CreateStoreCommand,
) -> None:
    """
    The repository should receive a Store aggregate.
    """
    repository.exists_by_owner_id.return_value = False
    repository.exists_by_slug.return_value = False

    await use_case.execute(command)

    saved_store = repository.save.await_args.args[0]

    assert isinstance(saved_store, Store)
    assert saved_store.plan.name == StarterPlan().name