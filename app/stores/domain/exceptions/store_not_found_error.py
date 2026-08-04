"""
Store Not Found Exists Error.

Raised when a user attempts retrieve store that does not exist.
"""


class StoreNotFoundError(Exception):
    """
    Raised when a user already owns a store.
    """

    def __init__(
        self,
        message: str = "Store does not exist",
    ) -> None:
        super().__init__(message)