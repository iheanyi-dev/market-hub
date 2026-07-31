"""
User status enumeration.

This module defines the lifecycle states of a user account.

A user's status determines whether the account can authenticate
or perform certain actions within the system.
"""

from enum import Enum


class UserStatus(str, Enum):
    """
    Represents the current status of a user account.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"