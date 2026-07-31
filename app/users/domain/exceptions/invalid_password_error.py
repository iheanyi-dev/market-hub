"""
Password-related domain exceptions.

This module contains the base exception for all password validation errors.
Separating password exceptions from generic exceptions keeps the domain explicit
and allows the application layer to handle password-specific failures cleanly.
"""


class InvalidPasswordError(ValueError):
    """
    Base exception raised when a password is invalid.

    All password-related domain exceptions should inherit from this class so
    callers can either catch specific password errors or handle all password
    validation failures uniformly.
    """