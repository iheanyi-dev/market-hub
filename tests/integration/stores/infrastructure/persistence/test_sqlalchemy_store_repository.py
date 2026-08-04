"""
Integration tests for the SQLAlchemy implementation of StoreRepository.

These tests verify that stores can be:

1. Persisted.
2. Retrieved by their identifier.
3. Retrieved by their owner.
4. Retrieved by their slug.
5. Checked for existence by owner.
6. Checked for existence by slug.
7. Updated.

Unlike unit tests, these tests interact with the real database.
"""

import pytest

from app.stores.domain.entities.store import Store
from app.stores.domain.plans.starter_plan import StarterPlan
from app.stores.domain.value_objects.store_description import (
    StoreDescription,
)
from app.stores.domain.value_objects.store_name import StoreName
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.stores.infrastructure.persistence.repositories.sqlalchemy_store_repository import (
    SqlAlchemyStoreRepository,
)
from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


@pytest.mark.asyncio
async def test_save_store(db_session) -> None:
    """
    Verify that a store can be persisted.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyStoreRepository(db_session)

    owner = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john1@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(owner)

    store = Store.create(
        owner_id=owner.id,
        name=StoreName.create("My Store"),
        slug=StoreSlug.create("my-store"),
        description=StoreDescription.create("My first store."),
        plan=StarterPlan(),
    )

    await repository.save(store)

    stored_store = await repository.find_by_id(store.id)

    assert stored_store is not None
    assert stored_store.id == store.id
    assert stored_store.owner_id == owner.id


@pytest.mark.asyncio
async def test_find_store_by_owner_id(db_session) -> None:
    """
    Verify that a store can be retrieved using its owner.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyStoreRepository(db_session)

    owner = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john2@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(owner)

    store = Store.create(
        owner_id=owner.id,
        name=StoreName.create("Tech Store"),
        slug=StoreSlug.create("tech-store"),
        description=StoreDescription.create("Technology products."),
        plan=StarterPlan(),
    )

    await repository.save(store)

    result = await repository.find_by_owner_id(owner.id)

    assert result is not None
    assert result.id == store.id
    assert result.owner_id == owner.id


@pytest.mark.asyncio
async def test_find_store_by_slug(db_session) -> None:
    """
    Verify that a store can be retrieved using its slug.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyStoreRepository(db_session)

    owner = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john3@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(owner)

    store = Store.create(
        owner_id=owner.id,
        name=StoreName.create("Fashion Store"),
        slug=StoreSlug.create("fashion-store"),
        description=StoreDescription.create("Fashion products."),
        plan=StarterPlan(),
    )

    await repository.save(store)

    result = await repository.find_by_slug(
        StoreSlug.create("fashion-store")
    )

    assert result is not None
    assert result.id == store.id
    assert result.slug == StoreSlug.create("fashion-store")


@pytest.mark.asyncio
async def test_exists_by_owner_id(db_session) -> None:
    """
    Verify that the repository can determine whether
    a user already owns a store.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyStoreRepository(db_session)

    owner = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john4@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(owner)

    store = Store.create(
        owner_id=owner.id,
        name=StoreName.create("Book Store"),
        slug=StoreSlug.create("book-store"),
        description=StoreDescription.create("Books."),
        plan=StarterPlan(),
    )

    await repository.save(store)

    exists = await repository.exists_by_owner_id(owner.id)

    assert exists is True


@pytest.mark.asyncio
async def test_exists_by_slug(db_session) -> None:
    """
    Verify that the repository can determine whether
    a store slug already exists.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyStoreRepository(db_session)

    owner = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john5@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(owner)

    store = Store.create(
        owner_id=owner.id,
        name=StoreName.create("Phone Store"),
        slug=StoreSlug.create("phone-store"),
        description=StoreDescription.create("Phones."),
        plan=StarterPlan(),
    )

    await repository.save(store)

    exists = await repository.exists_by_slug(
        StoreSlug.create("phone-store")
    )

    assert exists is True


@pytest.mark.asyncio
async def test_update_store(db_session) -> None:
    """
    Verify that updates made to a store are
    correctly persisted.
    """
    user_repository = SqlAlchemyUserRepository(db_session)
    repository = SqlAlchemyStoreRepository(db_session)

    owner = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create("john6@example.com"),
        password_hash="hashed-password",
    )

    await user_repository.save(owner)

    store = Store.create(
        owner_id=owner.id,
        name=StoreName.create("Original Store"),
        slug=StoreSlug.create("original-store"),
        description=StoreDescription.create("Original description."),
        plan=StarterPlan(),
    )

    await repository.save(store)

    store.change_name(
        StoreName.create("Updated Store")
    )
    store.change_description(
        StoreDescription.create("Updated description.")
    )

    await repository.update(store)

    updated_store = await repository.find_by_id(store.id)

    assert updated_store is not None
    assert updated_store.name == StoreName.create("Updated Store")
    assert updated_store.description == StoreDescription.create(
        "Updated description."
    )