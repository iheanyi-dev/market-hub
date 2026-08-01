"""
User authentication endpoints.
"""

from fastapi import APIRouter, Depends, status

from app.core.dependencies.use_cases import get_login_user_use_case
from app.users.application.dto.login_user_command import LoginUserCommand
from app.users.application.use_cases.login_user_use_case import (
    LoginUserUseCase,
)
from app.users.domain.value_objects.email import Email
from app.users.presentation.schemas.login_user_request import (
    LoginUserRequest,
)
from app.users.presentation.schemas.login_user_response import (
    LoginUserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    request: LoginUserRequest,
    use_case: LoginUserUseCase = Depends(
        get_login_user_use_case,
    ),
) -> LoginUserResponse:
    """
    Authenticate a registered user and return an access token.
    """

    command = LoginUserCommand(
        email=Email(request.email),
        password=request.password,
    )

    print(command)

    result = await use_case.execute(command)

    return LoginUserResponse(
        access_token=result.access_token,
        token_type=result.token_type,
    )