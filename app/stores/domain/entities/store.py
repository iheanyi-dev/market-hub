# app/stores/domain/entities/store.py

"""
Store Aggregate Root.

This module defines the Store aggregate, which is responsible for maintaining
the consistency and business rules of a store.

The Store aggregate is the entry point for all store-related domain operations.
External code should modify a Store only through the behaviors exposed by this
class.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.stores.domain.enums.store_status import StoreStatus
from app.stores.domain.plans.store_plan import StorePlan
from app.stores.domain.value_objects.store_description import StoreDescription
from app.stores.domain.value_objects.store_id import StoreId
from app.stores.domain.value_objects.store_name import StoreName
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.users.domain.value_objects.user_id import UserId


class Store:
    """
    Represents a store within the domain.

    A Store is the aggregate root of the Stores bounded context. It owns its
    state and ensures that changes occur only through well-defined behaviors.
    """

    def __init__(
        self,
        store_id: StoreId,
        owner_id: UserId,
        name: StoreName,
        slug: StoreSlug,
        description: StoreDescription,
        plan: StorePlan,
        product_count: int,
        status: StoreStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        """
        Initialize a Store aggregate.

        This constructor should not be called directly. Use the ``create()``
        factory method to create new stores.
        """
        self._id = store_id
        self._owner_id = owner_id
        self._name = name
        self._slug = slug
        self._description = description
        self._plan = plan
        self._product_count = product_count
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        name: StoreName,
        slug: StoreSlug,
        description: StoreDescription,
        plan: StorePlan,
    ) -> "Store":
        """
        Create a new Store aggregate.

        Newly created stores are initialized with:
            - A generated StoreId
            - ACTIVE status
            - Zero products
            - Creation and modification timestamps
        """
        now = datetime.now(UTC)

        return cls(
            store_id=StoreId.create(),
            owner_id=owner_id,
            name=name,
            slug=slug,
            description=description,
            plan=plan,
            product_count=0,
            status=StoreStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def reconstitute(
        cls,
        store_id: StoreId,
        owner_id: UserId,
        name: StoreName,
        slug: StoreSlug,
        description: StoreDescription,
        plan: StorePlan,
        product_count: int,
        status: StoreStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> "Store":
        """
        Reconstruct an existing Store aggregate from persisted data.
        """
        return cls(
            store_id=store_id,
            owner_id=owner_id,
            name=name,
            slug=slug,
            description=description,
            plan=plan,
            product_count=product_count,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

    @property
    def id(self) -> StoreId:
        return self._id

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

    @property
    def name(self) -> StoreName:
        return self._name

    @property
    def slug(self) -> StoreSlug:
        return self._slug

    @property
    def description(self) -> StoreDescription:
        return self._description

    @property
    def plan(self) -> StorePlan:
        return self._plan

    @property
    def product_count(self) -> int:
        return self._product_count

    @property
    def status(self) -> StoreStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def change_name(self, name: StoreName) -> None:
        """
        Change the store name.
        """
        if self._name == name:
            return

        self._name = name
        self._touch()

    def change_description(
        self,
        description: StoreDescription,
    ) -> None:
        """
        Change the store description.
        """
        if self._description == description:
            return

        self._description = description
        self._touch()

    def change_plan(self, plan: StorePlan) -> None:
        """
        Change the active store plan.
        """
        if self._plan == plan:
            return

        # Ensure the current catalogue fits into the new plan.
        plan.ensure_can_add_product(self._product_count - 1)

        self._plan = plan
        self._touch()

    def activate(self) -> None:
        """
        Activate the store.
        """
        if self._status == StoreStatus.ACTIVE:
            return

        self._status = StoreStatus.ACTIVE
        self._touch()

    def suspend(self) -> None:
        """
        Suspend the store.
        """
        if self._status == StoreStatus.SUSPENDED:
            return

        self._status = StoreStatus.SUSPENDED
        self._touch()

    def delete(self) -> None:
        """
        Soft-delete the store.
        """
        if self._status == StoreStatus.DELETED:
            return

        self._status = StoreStatus.DELETED
        self._touch()

    def increment_product_count(self) -> None:
        """
        Increase the number of products in the store.

        The assigned StorePlan determines whether another product
        may be added.
        """
        self._plan.ensure_can_add_product(self._product_count)

        self._product_count += 1
        self._touch()

    def decrement_product_count(self) -> None:
        """
        Decrease the number of products.

        Product count is never allowed to become negative.
        """
        if self._product_count == 0:
            return

        self._product_count -= 1
        self._touch()

    def _touch(self) -> None:
        """
        Update the modification timestamp.
        """
        self._updated_at = datetime.now(UTC)

    def update(
    self,
    *,
    name: StoreName,
    description: StoreDescription | None,
    ) -> None:
        """
        Update the mutable attributes of the store.

        This behavior encapsulates all business rules related to
        modifying store information. Only mutable attributes may be
        updated.

        Args:
            name:
                The new store name.

            description:
                The new store description.
        """

        self._name = name
        self._description = description

        self._touch()

    def __repr__(self) -> str:
        """
        Return a developer-friendly representation.
        """
        return (
            f"Store("
            f"id={self._id}, "
            f"owner_id={self._owner_id}, "
            f"name={self._name}, "
            f"slug={self._slug}, "
            f"status={self._status.value}, "
            f"product_count={self._product_count}"
            f")"
        )
    