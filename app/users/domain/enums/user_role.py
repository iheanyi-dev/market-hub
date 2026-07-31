"""
User role enumeration.

This module defines the roles available within the system.

A user's role determines the permissions and capabilities they have
throughout the application.
"""

from enum import Enum


class UserRole(str, Enum):
    """
    Represents the role assigned to a user.

    Inheriting from ``str`` ensures enum values are serialized naturally
    when stored in the database or returned in API responses.
    """

    CUSTOMER = "customer"
    VENDOR = "vendor"
    ADMIN = "admin"