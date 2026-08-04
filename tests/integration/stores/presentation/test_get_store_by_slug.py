"""
Integration tests for the Get Store By Slug endpoint.

These tests verify that:

1. Anyone can retrieve a store by its slug.
2. A non-existent slug returns 404.
"""

from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


async def create_test_user(db_session) -> User:
    """
    Create and persist a unique test user.
    """
    repository = SqlAlchemyUserRepository(db_session)

    user = User.create(
        full_name=FullName.create("John Doe"),
        email=Email.create(f"{uuid4()}@example.com"),
        password_hash="hashed-password",
    )

    await repository.save(user)

    return user


@pytest.mark.asyncio
async def test_get_store_by_slug_success(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that anyone can retrieve a store using its slug.
    """

    user = await create_test_user(db_session)

    response = await async_client.post(
        "/stores",
        headers=auth_headers(user),
        json={
            "name": "My Store",
            "slug": "my-store",
            "description": "My online store",
            "plan": "starter",
        },
    )

    assert response.status_code == 201

    response = await async_client.get(
        "/stores/my-store",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "My Store"
    assert body["slug"] == "my-store"
    assert body["description"] == "My online store"
    assert body["plan"] == "Starter"
    assert body["product_count"] == 0


@pytest.mark.asyncio
async def test_get_store_by_slug_not_found(
    async_client: AsyncClient,
) -> None:
    """
    Verify that 404 is returned when the store
    does not exist.
    """

    response = await async_client.get(
        "/stores/non-existent-store",
    )

    assert response.status_code == 404