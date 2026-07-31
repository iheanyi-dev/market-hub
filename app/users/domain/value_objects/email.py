"""
Email value object.

Represents a valid email address within the domain. Once created,
an Email object is guaranteed to contain a normalized, valid email.
"""

from dataclasses import dataclass
import re

from app.users.domain.exceptions.invalid_email_error import InvalidEmailError


@dataclass(frozen=True, slots=True)
class Email:
    """
    Immutable email value object.
    """

    value: str

    # Simple email validation pattern.
    # This is sufficient for our domain. We intentionally avoid
    # overly complex RFC-compliant regular expressions.
    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def __post_init__(self) -> None:
        """
        Normalize and validate the email during object creation.
        """
        normalized_email = self.value.strip().lower()

        if not self.EMAIL_PATTERN.fullmatch(normalized_email):
            raise InvalidEmailError(self.value)

        # The dataclass is frozen, so object.__setattr__ is required
        # to assign the normalized value during initialization.
        object.__setattr__(self, "value", normalized_email)

    @classmethod
    def create(cls, email: str) -> 'Email':
        """
        Normalize and validate the email during object creation.
        """
        normalized_email = email.strip().lower()

        if not cls.EMAIL_PATTERN.fullmatch(normalized_email):
            raise InvalidEmailError(email)

        return cls(normalized_email)

    def __str__(self) -> str:
        """
        Return the normalized email address.
        """
        return self.value