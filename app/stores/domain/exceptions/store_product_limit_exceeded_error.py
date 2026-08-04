"""
Store Product Limit Exceeded Error.

Raised when an operation would exceed the maximum number of products
allowed by the store's current plan.
"""


class StoreProductLimitExceededError(Exception):
    """
    Raised when a store has reached its product limit.
    """

    def __init__(self, message: str = "Store product limit exceeded.") -> None:
        super().__init__(message)