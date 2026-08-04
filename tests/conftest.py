"""
Shared pytest fixtures.
"""
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app

import pytest

from tests.fakes.fake_user_repository import FakeUserRepository

"""
Shared fixtures for integration tests.

Each test gets:
- its own database connection
- its own transaction
- its own SQLAlchemy session
- an HTTP client connected to the FastAPI app

The transaction is rolled back after every test so the database remains clean.
"""

from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.main import app
from app.shared.database.session import get_db_session
from tests.database import engine


@pytest_asyncio.fixture
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    """
    Create a dedicated database connection for a single test.
    """
    async with engine.connect() as connection:
        yield connection


@pytest_asyncio.fixture
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[None, None]:
    """
    Start an outer transaction that will always be rolled back.
    """

    transaction = await connection.begin()

    try:
        yield
    finally:
        if transaction.is_active:
            await transaction.rollback()


@pytest_asyncio.fixture
async def db_session(
    connection: AsyncConnection,
    transaction: None,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a session bound to the test connection.

    A SAVEPOINT is started so application code may call commit()
    without ending the outer transaction. After each commit, a new
    SAVEPOINT is automatically created.
    """

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
    )

    # Begin the first SAVEPOINT.
    await session.begin_nested()

    from sqlalchemy import event

    @event.listens_for(session.sync_session, "after_transaction_end")
    def restart_savepoint(sync_session, trans):
        """
        Recreate the SAVEPOINT whenever the previous nested transaction
        ends. This allows multiple commits during a single test.
        """
        if trans.nested and not trans._parent.nested:
            sync_session.begin_nested()

    try:
        yield session
    finally:
        await session.close()
        await session.close()


@pytest_asyncio.fixture
async def async_client(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Override the application's database dependency so every request
    uses the test session.
    """

    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def user_repository() -> FakeUserRepository:
    """
    Return a fresh in-memory user repository for each test.
    """
    return FakeUserRepository()

from app.core.dependencies.use_cases import get_register_user_use_case
from app.users.application.use_cases.register_user_use_case import RegisterUserUseCase


# @pytest_asyncio.fixture
# async def async_client():

#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#     ) as client:
#         yield client

"""
Shared pytest fixtures.

Contains reusable fixtures for integration tests.
"""

from app.shared.infrastructure.security.jwt_token_generator import (
    JwtTokenGenerator
)


@pytest.fixture
def auth_headers() -> callable:
    """
    Generate Authorization headers for authenticated requests.

    This fixture creates a valid access token and returns
    the HTTP Authorization header required by protected endpoints.
    """

    def create_headers(user) -> dict[str, str]:
        """
        Create bearer token headers for a user.

        Args:
            user:
                Authenticated domain user.

        Returns:
            Authorization headers.
        """

        token = JwtTokenGenerator().generate_access_token(
            subject=str(user.id),
        )

        return {
            "Authorization": f"Bearer {token}",
        }

    return create_headers