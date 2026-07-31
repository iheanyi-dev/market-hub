"""
Database engine and session configuration.

This module provides a single source for creating database connections.
All repositories obtain database sessions from here, ensuring consistent
configuration and easy maintenance.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.shared.config.settings import settings

# Create a single asynchronous database engine for the application.
# The engine manages the connection pool and communicates with PostgreSQL.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Factory responsible for creating AsyncSession instances.
# Disabling expire_on_commit prevents SQLAlchemy from automatically
# expiring objects after a transaction is committed.
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for a single request.

    FastAPI automatically closes the session after the request
    completes, preventing connection leaks.
    """
    async with AsyncSessionFactory() as session:
        yield session