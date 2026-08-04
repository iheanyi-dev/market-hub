"""
Integration tests for the Create Store API endpoint.

These tests verify that:

1. An authenticated user can create a store.
2. A user cannot create more than one store.
3. A duplicate slug cannot be used.
4. Authentication is required.

These tests interact with the real application stack:
    - FastAPI
    - Authentication dependency
    - Database session
    - Store repository
    - CreateStoreUseCase
"""

import pytest
from httpx import AsyncClient

from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.infrastructure.database.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from uuid import uuid4

async def create_test_user(db_session) -> User:
    """
    Create and persist a user required for authentication tests.
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
async def test_create_store_success(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that an authenticated user can create a store.
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

    body = response.json()

    assert body["name"] == "My Store"
    assert body["slug"] == "my-store"
    assert body["plan"] == "starter"


@pytest.mark.asyncio
async def test_create_store_without_token_returns_401(
    async_client: AsyncClient,
) -> None:
    """
    Verify that creating a store requires authentication.
    """

    response = await async_client.post(
        "/stores",
        json={
            "name": "My Store",
            "slug": "my-store",
            "description": "My online store",
            "plan": "starter",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_cannot_create_two_stores(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that a user can own only one store.
    """

    user = await create_test_user(db_session)

    payload = {
        "name": "First Store",
        "slug": "first-store",
        "description": "First store",
        "plan": "starter",
    }

    first_response = await async_client.post(
        "/stores",
        headers=auth_headers(user),
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await async_client.post(
        "/stores",
        headers=auth_headers(user),
        json={
            **payload,
            "slug": "second-store",
        },
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_duplicate_store_slug_returns_error(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that duplicate store slugs are rejected.
    """

    user_one = await create_test_user(db_session)

    response = await async_client.post(
        "/stores",
        headers=auth_headers(user_one),
        json={
            "name": "Store One",
            "slug": "same-slug",
            "description": "Store one",
            "plan": "starter",
        },
    )

    assert response.status_code == 201

    user_two = await create_test_user(db_session)

    response = await async_client.post(
        "/stores",
        headers=auth_headers(user_two),
        json={
            "name": "Store Two",
            "slug": "same-slug",
            "description": "Store two",
            "plan": "starter",
        },
    )

    assert response.status_code == 409