"""
Application exceptions for user registration.

This module contains exceptions raised by the user registration use case.
"""


class EmailAlreadyExistsError(Exception):
    """
    Raised when attempting to register a user with an email address that
    already exists in the system.
    """