"""
Store Already Exists Error.

Raised when a user attempts to create more than one store.
"""


class StoreAlreadyExistsError(Exception):
    """
    Raised when a user already owns a store.
    """

    def __init__(
        self,
        message: str = "The user already owns a store.",
    ) -> None:
        super().__init__(message)