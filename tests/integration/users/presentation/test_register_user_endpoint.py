import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
    payload = {
        "full_name": "John Doe",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "Password123!",
    }

    response = await async_client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["full_name"] == payload["full_name"]
    assert body["email"] == payload["email"]
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


@pytest.mark.asyncio
async def test_register_user_duplicate_email(async_client: AsyncClient):
    payload = {
        "full_name": "John Doe",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "Password123!",
    }

    await async_client.post(
        "/api/v1/users/register",
        json=payload,
    )

    response = await async_client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_user_invalid_email(async_client: AsyncClient):
    payload = {
        "full_name": "John Doe",
        "email": "invalid-email",
        "password": "Password123!",
    }

    response = await async_client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_short_password(async_client: AsyncClient):
    payload = {
        "full_name": "John Doe",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "123",
    }

    response = await async_client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_missing_full_name(async_client: AsyncClient):
    payload = {
        "email": f"{uuid.uuid4()}@example.com",
        "password": "Password123!",
    }

    response = await async_client.post(
        "/api/v1/users/register",
        json=payload,
    )

    assert response.status_code == 422