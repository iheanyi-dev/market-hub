"""
Abstract StorePlan.

A StorePlan encapsulates plan-specific business rules.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.stores.domain.exceptions.store_product_limit_exceeded_error import (
    StoreProductLimitExceededError,
)


class StorePlan(ABC):
    """
    Base class for all store plans.
    """

    @property
    @abstractmethod
    def code(self) -> str:
        """
        Return the machine-readable plan identifier.
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the human-readable plan name.
        """

    @property
    @abstractmethod
    def max_products(self) -> int:
        """
        Return the maximum number of products allowed.
        """

    def can_add_product(self, product_count: int) -> bool:
        """
        Determine whether another product can be added.
        """
        return product_count < self.max_products

    def ensure_can_add_product(self, product_count: int) -> None:
        """
        Ensure another product can be added.

        Raises:
            StoreProductLimitExceededError:
                If the plan limit has been reached.
        """
        if not self.can_add_product(product_count):
            raise StoreProductLimitExceededError(
                f"The '{self.name}' plan allows a maximum of "
                f"{self.max_products} products."
            )