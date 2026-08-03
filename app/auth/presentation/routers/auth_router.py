"""
Authentication API endpoints.

This router is responsible only for HTTP concerns.

Responsibilities:
    - Receive client requests.
    - Invoke the appropriate use case.
    - Set the refresh token as an HttpOnly cookie.
    - Return the access token to the client.

Business rules remain inside the application layer.
"""

from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    status,
)
from fastapi.responses import Response

from app.auth.application.use_cases.logout_use_case import (
    LogoutUseCase,
)
from app.auth.infrastructure.dependencies import (
    get_logout_use_case,
)

from app.auth.application.dto.refresh_token_command import (
    RefreshTokenCommand,
)
from app.auth.application.exceptions.invalid_refresh_token_error import (
    InvalidRefreshTokenError,
)
from app.auth.application.use_cases.refresh_token_use_case import (
    RefreshTokenUseCase,
)
from app.auth.infrastructure.dependencies import (
    get_refresh_token_use_case,
)
from app.auth.presentation.schemas.refresh_token_response import (
    RefreshTokenResponse,
)
from app.shared.config.settings import settings
from app.core.dependencies.use_cases import get_login_user_use_case
from app.users.application.dto.login_user_command import (
    LoginUserCommand,
)
from app.users.application.use_cases.login_user_use_case import (
    LoginUserUseCase,
)
from app.users.presentation.schemas.login_user_request import (
    LoginUserRequest,
)
from app.users.presentation.schemas.login_user_response import (
    LoginUserResponse,
)

from app.auth.infrastructure.dependencies import (
    get_current_user,
)
from app.users.domain.entities.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginUserRequest,
    response: Response,
    use_case: LoginUserUseCase = Depends(
        get_login_user_use_case,
    ),
) -> LoginUserResponse:
    """
    Authenticate a user.

    The refresh token is stored as an HttpOnly cookie while the
    access token is returned in the response body.
    """

    result = await use_case.execute(
        LoginUserCommand(
            email=request.email,
            password=request.password,
        )
    )

    #
    # Store refresh token as an HttpOnly cookie.
    #
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth/refresh",
    )

    #
    # Do NOT expose the refresh token in JSON.
    #
    return LoginUserResponse(
        access_token=result.access_token,
    )


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    request: Request,
    response: Response,
    use_case: RefreshTokenUseCase = Depends(
        get_refresh_token_use_case,
    ),
) -> RefreshTokenResponse:
    """
    Issue a new access token using the refresh token stored
    in the HttpOnly cookie.
    """

    refresh_token = request.cookies.get(
        "refresh_token",
    )

    if refresh_token is None:
        raise InvalidRefreshTokenError()

    result = await use_case.execute(
        RefreshTokenCommand(
            refresh_token=refresh_token,
        )
    )

    #
    # Rotate the refresh token by replacing the cookie.
    #
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth/refresh",
    )

    return RefreshTokenResponse(
        access_token=result.access_token,
    )

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    request: Request,
    response: Response,
    use_case: LogoutUseCase = Depends(
        get_logout_use_case,
    ),
) -> Response:
    """
    Logout the authenticated user.

    The refresh token is revoked and the HttpOnly cookie
    is removed from the browser.
    """

    refresh_token = request.cookies.get(
        "refresh_token",
    )

    if refresh_token is not None:
        await use_case.execute(
            RefreshTokenCommand(
                refresh_token=refresh_token,
            )
        )
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh",
    )

    response.status_code = status.HTTP_204_NO_CONTENT

    return response

@router.get("/me")
async def me(
    current_user: User = Depends(
        get_current_user,
    ),
):
    """
    Retrieve the authenticated user.
    """

    return {
        "id": current_user.id,
        "full_name": current_user.full_name.value,
        "email": current_user.email.value,
        "role": current_user.role.value,
        "status": current_user.status.value,
    }