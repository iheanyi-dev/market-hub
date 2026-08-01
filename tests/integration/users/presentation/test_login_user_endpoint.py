"""
Integration tests for the user login endpoint.

These tests exercise the complete authentication flow through the HTTP API,
ensuring that the presentation, application, infrastructure, and persistence
layers work together correctly.

Scenarios covered:
- Successful login with valid credentials.
- Login with an email that does not exist.
- Login with an incorrect password.
"""

import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_user_success(async_client: AsyncClient) -> None:
    """
    A registered user should be able to authenticate successfully.

    Expected result:
    - HTTP 200 OK
    - Access token returned
    - Token type is 'bearer'
    """

    registration_payload = {
        "full_name": "John Doe",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "Password123!",
    }

    register_response = await async_client.post(
        "/api/v1/users/register",
        json=registration_payload,
    )

    assert register_response.status_code == 201

    login_response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": registration_payload["email"],
            "password": registration_payload["password"],
        },
    )

    assert login_response.status_code == 200

    body = login_response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user_with_unknown_email(
    async_client: AsyncClient,
) -> None:
    """
    Authentication should fail when the supplied email
    does not belong to any registered user.
    """

    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_user_with_invalid_password(
    async_client: AsyncClient,
) -> None:
    """
    Authentication should fail when the supplied password
    is incorrect.
    """

    registration_payload = {
        "full_name": "John Doe",
        "email": f"{uuid.uuid4()}@example.com",
        "password": "Password123!",
    }

    register_response = await async_client.post(
        "/api/v1/users/register",
        json=registration_payload,
    )

    assert register_response.status_code == 201

    login_response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": registration_payload["email"],
            "password": "WrongPassword123!",
        },
    )

    assert login_response.status_code == 401