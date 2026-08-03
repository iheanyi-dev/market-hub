"""
User registration endpoints.
"""

from fastapi import APIRouter, Depends, status

from app.users.application.dto.register_user_command import RegisterUserCommand
from app.users.application.dto.register_user_result import RegisterUserResult
from app.users.application.use_cases.register_user_use_case import RegisterUserUseCase
from app.users.presentation.schemas.register_user_request import RegisterUserRequest
from app.users.presentation.schemas.register_user_response import RegisterUserResponse
from app.core.dependencies.use_cases import (
    get_register_user_use_case,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: RegisterUserRequest,
    use_case: RegisterUserUseCase = Depends(
        get_register_user_use_case,
    ),
) -> RegisterUserResponse:
    """
    Register a new user.
    """

    command = RegisterUserCommand(
        full_name=request.full_name,
        email=request.email,
        password=request.password,
    )

    result = await use_case.execute(command)

    return result
