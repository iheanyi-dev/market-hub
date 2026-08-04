"""
Invalid Store Plan Error.

Raised when an invalid or unsupported store plan is requested.
"""


class InvalidStorePlanError(Exception):
    """
    Raised when a requested store plan is invalid.
    """

    def __init__(
        self,
        message: str = "Invalid store plan.",
    ) -> None:
        super().__init__(message)