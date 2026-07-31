"""
User Mapper.

This module contains helper methods for converting User aggregates into
application DTOs.
"""

from app.users.application.dto.register_user_result import (
    RegisterUserResult,
)
from app.users.domain.entities.user import User


class UserMapper:
    """
    Maps User aggregates to application DTOs.
    """

    @staticmethod
    def to_register_result(user: User) -> RegisterUserResult:
        """
        Convert a User aggregate into a RegisterUserResult DTO.

        Args:
            user:
                The User aggregate.

        Returns:
            A RegisterUserResult DTO.
        """
        return RegisterUserResult(
            id=str(user.id),
            full_name=user.full_name.value,
            email=user.email.value,
            role=user.role.value,
            status=user.status.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )