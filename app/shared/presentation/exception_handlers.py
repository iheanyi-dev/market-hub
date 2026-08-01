"""
Global exception handlers.
"""

from datetime import UTC, datetime

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.users.application.exceptions.email_already_exists_error import (
    EmailAlreadyExistsError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """

    @app.exception_handler(EmailAlreadyExistsError)
    async def email_already_exists_handler(
        request: Request,
        exc: EmailAlreadyExistsError,
    ) -> JSONResponse:
        """
        Handle duplicate email registration.
        """
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": str(exc),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )