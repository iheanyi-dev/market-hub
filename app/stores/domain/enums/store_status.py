"""
Store Status.

Defines the lifecycle states of a store.
"""

from enum import Enum


class StoreStatus(str, Enum):
    """
    Enumeration of store statuses.
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"