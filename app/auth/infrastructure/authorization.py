from fastapi import Depends, HTTPException, status

from app.auth.infrastructure.dependencies import (
    get_current_user,
)
from app.users.domain.entities.user import User


class RequireRole:
    """
    Role-based authorization dependency.
    """

    def __init__(
        self,
        *roles: str,
    ):
        self._roles = roles

    async def __call__(
        self,
        current_user: User = Depends(
            get_current_user,
        ),
    ) -> User:

        if current_user.role.value not in self._roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return current_user