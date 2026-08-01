"""
Exception raised when authentication fails due to invalid credentials.
"""



class InvalidCredentialsException(Exception):
    """
    Raised when the supplied email or password is invalid.
    """

    def __init__(self) -> None:
        super().__init__(
            "Invalid email or password.",
        )