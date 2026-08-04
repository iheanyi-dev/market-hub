"""
Global user exception handlers.
"""

from datetime import UTC, datetime

from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse


from app.stores.domain.exceptions.store_already_exists_error import (
    StoreAlreadyExistsError
)
from app.stores.domain.exceptions.store_slug_already_exists_error import (
    StoreSlugAlreadyExistsError
)

from app.stores.domain.exceptions.invalid_store_plan_error import (
    InvalidStorePlanError
)
from app.stores.domain.exceptions.store_product_limit_exceeded_error import (
    StoreProductLimitExceededError
)

from app.stores.domain.exceptions.store_not_found_error import (
    StoreNotFoundError
)

def register_store_exception_handlers(app: FastAPI) -> None:
    """
    Register all user exception handlers.
    """
    @app.exception_handler(StoreAlreadyExistsError)
    async def email_already_exists_handler(
        request: Request,
        exc: StoreAlreadyExistsError,
    ) -> JSONResponse:
        """
        Handle duplicate email registration.
        """
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content= {
                "message": str(exc)
            }
        )

    @app.exception_handler(StoreSlugAlreadyExistsError)
    async def email_already_exists_handler(
        request: Request,
        exc: StoreSlugAlreadyExistsError,
    ) -> JSONResponse:
        """
        Handle duplicate email registration.
        """
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
             content= {
                "message": str(exc)
            }
        )

    @app.exception_handler(InvalidStorePlanError)
    async def email_already_exists_handler(
        request: Request,
        exc: InvalidStorePlanError,
    ) -> JSONResponse:
        """
        Handle duplicate email registration.
        """
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
             content= {
                "message": str(exc)
            }
        )

    @app.exception_handler(StoreProductLimitExceededError)
    async def email_already_exists_handler(
        request: Request,
        exc: StoreProductLimitExceededError,
    ) -> JSONResponse:
        """
        Handle duplicate email registration.
        """
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
             content= {
                "message": str(exc)
            }
        )

    @app.exception_handler(StoreNotFoundError)
    async def email_already_exists_handler(
        request: Request,
        exc: StoreNotFoundError,
    ) -> JSONResponse:
        """
        Handle duplicate email registration.
        """
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
             content= {
                "message": str(exc)
            }
        )



