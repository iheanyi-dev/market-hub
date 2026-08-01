from fastapi import FastAPI

from app.shared.config.settings import settings

from app.shared.presentation.exception_handlers import (
    register_exception_handlers,
)
from app.users.presentation.controllers.users_controller import (
    router as users_router,
)

from app.users.presentation.controllers.auth_controller import (
    router as auth_router,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

register_exception_handlers(app)

# Register feature routers.
app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "environment": settings.ENVIRONMENT,
    }