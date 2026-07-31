"""
Domain exception raised when an email address is invalid.

The domain raises this exception whenever an Email value object
cannot be created from the supplied input.
"""


class InvalidEmailError(ValueError):
    """
    Raised when an email address fails domain validation.
    """

    def __init__(self, email: str) -> None:
        """
        Initialize the exception with the invalid email value.

        Args:
            email: The invalid email supplied by the caller.
        """
        super().__init__(f"'{email}' is not a valid email address.")