"""
Owner Stores Router.

This module exposes endpoints that allow an authenticated user
to manage their own store.
"""

from fastapi import APIRouter, Depends, status

from app.auth.infrastructure.dependencies import (
    get_current_user,
)
from app.stores.application.dto.create_store_command import (
    CreateStoreCommand,
)
from app.stores.application.use_cases.create_store_use_case import (
    CreateStoreUseCase,
)
from app.stores.presentation.dependencies.get_create_store_use_case import (
    get_create_store_use_case,
)
from app.stores.presentation.dependencies.get_my_store_use_case import (
    get_get_my_store_use_case
)
from app.stores.presentation.schemas.create_store_request import (
    CreateStoreRequest,
)
from app.stores.presentation.schemas.create_store_response import (
    CreateStoreResponse,
)
from app.stores.application.use_cases.get_my_store_use_case import (
    GetMyStoreUseCase,
)
from app.stores.presentation.schemas.get_my_store_response import (
    GetMyStoreResponse,
)
from app.users.domain.entities.user import User

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
)


@router.post(
    "",
    response_model=CreateStoreResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_store(
    request: CreateStoreRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreateStoreUseCase = Depends(
        get_create_store_use_case,
    ),
) -> CreateStoreResponse:
    """
    Create a new store for the authenticated user.

    Business Rules:
        - A user may own only one store.
        - The store slug must be unique.
        - The requested plan must be valid.

    Args:
        request:
            The validated request payload.

        current_user:
            The authenticated user extracted from the access token.

        use_case:
            The application use case responsible for creating stores.

    Returns:
        The newly created store.
    """
    result = await use_case.execute(
        CreateStoreCommand(
            user_id=current_user.id,
            name=request.name,
            slug=request.slug,
            description=request.description,
            plan=request.plan,
        )
    )

    return CreateStoreResponse.model_validate(result)

@router.get(
    "/me",
    response_model=GetMyStoreResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_store(
    current_user: User = Depends(get_current_user),
    use_case: GetMyStoreUseCase = Depends(
        get_get_my_store_use_case,
    ),
) -> GetMyStoreResponse:
    """
    Retrieve the authenticated user's store.

    Args:
        current_user:
            The authenticated user extracted from the access token.

        use_case:
            The application use case responsible for retrieving
            the authenticated user's store.

    Returns:
        The authenticated user's store.
    """
    result = await use_case.execute(current_user.id)

    return GetMyStoreResponse.model_validate(result)