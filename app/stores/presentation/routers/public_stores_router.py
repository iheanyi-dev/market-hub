from fastapi import Path, APIRouter, Depends

from app.stores.application.dto.get_store_result import GetStoreResult
from app.stores.application.use_cases.get_store_by_slug_use_case import (
    GetStoreBySlugUseCase,
)
from app.stores.domain.exceptions.store_not_found_error import StoreNotFoundError
from app.stores.domain.value_objects.store_slug import StoreSlug
from app.stores.presentation.dependencies.get_store_by_slug_use_case import (
    get_store_by_slug_use_case,
)
from app.stores.presentation.schemas.get_store_response import (
    GetStoreResponse,
)

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
)

@router.get(
    "/{slug}",
    response_model=GetStoreResponse,
    status_code=200,
)
async def get_store_by_slug(
    slug: str = Path(
        ...,
        description="Public store slug.",
    ),
    use_case: GetStoreBySlugUseCase = Depends(
        get_store_by_slug_use_case,
    ),
) -> GetStoreResponse:
    """
    Retrieve a public store by its slug.

    This endpoint is publicly accessible and exposes only
    non-sensitive information.
    """

    result: GetStoreResult = await use_case.execute(
        StoreSlug.create(slug),
    )

    return GetStoreResponse.model_validate(result)