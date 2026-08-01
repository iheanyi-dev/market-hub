"""
Database dependency providers.
"""

from app.shared.database.session import get_db_session

__all__ = ["get_db_session"]