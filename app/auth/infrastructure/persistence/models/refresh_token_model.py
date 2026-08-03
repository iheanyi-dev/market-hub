"""
SQLAlchemy Refresh Token Model.

This module defines the database representation of a refresh token.

A refresh token belongs to a single user and is used to issue
new access tokens without requiring the user to log in again.

Only the hash of the refresh token is stored in the database.
The raw refresh token is never persisted.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class RefreshTokenModel(Base):
    """
    Database representation of a refresh token.

    This model belongs to the persistence layer and should never
    be used directly by the domain layer.
    """

    __tablename__ = "refresh_tokens"

    # Unique identifier for the refresh token.
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    # User that owns this refresh token.
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # SHA-256 hash of the refresh token.
    # The raw token is never stored.
    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # Indicates whether this refresh token has been revoked.
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Date and time when the refresh token expires.
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )