"""
Defines the application's base ORM class.

Every SQLAlchemy model in the project inherits from `Base`, ensuring
they all share the same metadata and naming conventions. This provides
consistent schema generation and predictable Alembic migrations.
"""

from sqlalchemy.orm import DeclarativeBase

from app.shared.database.naming import metadata


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    Attaching the shared metadata ensures every model uses the same
    naming convention for indexes, primary keys, foreign keys,
    unique constraints, and check constraints.
    """

    # Use the project's shared metadata so all database objects
    # follow a consistent naming convention.
    metadata = metadata