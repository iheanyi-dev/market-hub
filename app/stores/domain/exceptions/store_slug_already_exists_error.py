"""
Store Slug Already Exists Error.

Raised when a store slug is already in use.
"""


class StoreSlugAlreadyExistsError(Exception):
    """
    Raised when a store slug already exists.
    """

    def __init__(
        self,
        message: str = "The store slug already exists.",
    ) -> None:
        super().__init__(message)