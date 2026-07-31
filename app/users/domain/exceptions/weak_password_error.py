"""
Exceptions for weak passwords.

A weak password is considered syntactically valid but fails to satisfy the
security policy defined by the domain.
"""

from app.users.domain.exceptions.invalid_password_error import InvalidPasswordError


class WeakPasswordError(InvalidPasswordError):
    """
    Raised when a password does not satisfy the application's password policy.

    Examples:
        - Too short
        - Missing uppercase letter
        - Missing lowercase letter
        - Missing digit
        - Missing special character
    """