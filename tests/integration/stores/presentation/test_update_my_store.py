"""
Integration tests for the Update My Store endpoint.

These tests verify that:

1. An authenticated store owner can update their store.
2. Authentication is required.
3. A user without a store receives 404.
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
async def test_update_my_store_success(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that a store owner can update
    their store information.
    """

    user = await create_test_user(db_session)

    response = await async_client.post(
        "/stores",
        headers=auth_headers(user),
        json={
            "name": "My Store",
            "slug": "my-store",
            "description": "Old description",
            "plan": "starter",
        },
    )

    assert response.status_code == 201

    response = await async_client.patch(
        "/stores/me",
        headers=auth_headers(user),
        json={
            "name": "Updated Store",
            "description": "New description",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Updated Store"
    assert body["slug"] == "my-store"
    assert body["description"] == "New description"
    assert body["plan"] == "starter"
    assert body["product_count"] == 0


@pytest.mark.asyncio
async def test_update_my_store_requires_authentication(
    async_client: AsyncClient,
) -> None:
    """
    Verify that authentication is required.
    """

    response = await async_client.patch(
        "/stores/me",
        json={
            "name": "Updated Store",
            "description": "New description",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_my_store_not_found(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that 404 is returned when the user
    does not own a store.
    """

    user = await create_test_user(db_session)

    response = await async_client.patch(
        "/stores/me",
        headers=auth_headers(user),
        json={
            "name": "Updated Store",
            "description": "New description",
        },
    )

    assert response.status_code == 404