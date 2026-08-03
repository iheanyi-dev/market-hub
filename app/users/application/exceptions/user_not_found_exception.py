"""
Exception raised when user not found .
"""



class UserNotFoundException(Exception):
    """
    Raised when the supplied user is not registered.
    """

    def __init__(self) -> None:
        super().__init__(
            "user not found",
        )