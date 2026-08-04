"""
Integration tests for the Change Store Plan endpoint.

These tests verify that:

1. A store owner can change their subscription plan.
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
async def test_change_store_plan_success(
    async_client: AsyncClient,
    db_session,
    auth_headers,
) -> None:
    """
    Verify that a store owner can change
    their subscription plan.
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

    response = await async_client.patch(
        "/stores/me/plan",
        headers=auth_headers(user),
        json={
            "plan": "professional",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["plan"] == "Professional"


@pytest.mark.asyncio
async def test_change_store_plan_requires_authentication(
    async_client: AsyncClient,
) -> None:
    """
    Verify that authentication is required.
    """

    response = await async_client.patch(
        "/stores/me/plan",
        json={
            "plan": "professional",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_change_store_plan_not_found(
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
        "/stores/me/plan",
        headers=auth_headers(user),
        json={
            "plan": "professional",
        },
    )

    assert response.status_code == 404