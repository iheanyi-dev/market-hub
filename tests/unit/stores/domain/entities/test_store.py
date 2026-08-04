# tests/unit/stores/domain/entities/test_store.py

"""
Unit tests for the Store aggregate.

These tests define the expected behaviour of the Store aggregate before the
implementation is written (TDD).
"""

from datetime import UTC, datetime

import pytest

from app.stores.domain.entities.store import Store
from app.stores.domain.enums.store_status import StoreStatus
from app.stores.domain.exceptions.store_product_limit_exceeded_error import (
    StoreProductLimitExceededError,
)
from app.stores.domain.plans.starter_plan import StarterPlan
from app.stores.domain.value_objects.store_description import StoreDescription
from app.stores.domain.value_objects.store_name import StoreName
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.users.domain.value_objects.user_id import UserId
from app.stores.domain.plans.professional_plan import ProfessionalPlan

def test_create_store() -> None:
    """
    A newly created store should be initialized with sensible defaults.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("My Store"),
        slug=StoreSlug("my-store"),
        description=StoreDescription("My first store."),
        plan=StarterPlan(),
    )

    assert store.owner_id is not None
    assert store.name == StoreName("My Store")
    assert store.slug == StoreSlug("my-store")
    assert store.description == StoreDescription("My first store.")
    assert isinstance(store.plan, StarterPlan)
    assert store.product_count == 0
    assert store.status == StoreStatus.ACTIVE


def test_change_store_name() -> None:
    """
    Changing the store name should update the aggregate.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Old Store"),
        slug=StoreSlug("old-store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    store.change_name(StoreName("New Store"))

    assert store.name == StoreName("New Store")


def test_change_store_description() -> None:
    """
    Changing the description should update the aggregate.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Old description"),
        plan=StarterPlan(),
    )

    store.change_description(
        StoreDescription("New description")
    )

    assert store.description == StoreDescription(
        "New description"
    )


def test_change_plan() -> None:
    """
    The active store plan should be replaceable.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    new_plan = StarterPlan()

    store.change_plan(new_plan)

    assert store.plan == new_plan


def test_increment_product_count() -> None:
    """
    Adding a product should increase the product count.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    store.increment_product_count()

    assert store.product_count == 1


def test_increment_product_count_raises_when_limit_reached() -> None:
    """
    The aggregate should prevent exceeding the plan limit.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    for _ in range(store.plan.max_products):
        store.increment_product_count()

    with pytest.raises(StoreProductLimitExceededError):
        store.increment_product_count()


def test_decrement_product_count() -> None:
    """
    Removing a product should decrease the count.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    store.increment_product_count()
    store.decrement_product_count()

    assert store.product_count == 0


def test_activate_store() -> None:
    """
    A suspended store should become active.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    store.suspend()
    store.activate()

    assert store.status == StoreStatus.ACTIVE


def test_suspend_store() -> None:
    """
    Suspending a store should update its status.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    store.suspend()

    assert store.status == StoreStatus.SUSPENDED


def test_delete_store() -> None:
    """
    Deleting a store should mark it as deleted.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    store.delete()

    assert store.status == StoreStatus.DELETED

def test_upgrade_store_plan() -> None:
    """
    A store should be able to upgrade its plan.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=StarterPlan(),
    )

    new_plan = ProfessionalPlan()

    store.change_plan(new_plan)

    assert store.plan == new_plan

def test_downgrade_store_plan() -> None:
    """
    A store should be able to downgrade when its catalogue
    fits within the new plan.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=ProfessionalPlan(),
    )

    for _ in range(20):
        store.increment_product_count()

    new_plan = StarterPlan()

    store.change_plan(new_plan)

    assert store.plan == new_plan

def test_downgrade_plan_raises_when_product_limit_exceeded() -> None:
    """
    Downgrading should fail if the current catalogue exceeds
    the new plan's limit.
    """
    store = Store.create(
        owner_id=UserId.create(),
        name=StoreName("Store"),
        slug=StoreSlug("store"),
        description=StoreDescription("Description"),
        plan=ProfessionalPlan(),
    )

    for _ in range(21):
        store.increment_product_count()

    with pytest.raises(StoreProductLimitExceededError):
        store.change_plan(StarterPlan())