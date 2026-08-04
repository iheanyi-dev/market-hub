from fastapi import FastAPI

from app.shared.config.settings import settings

from app.shared.presentation.exception_handlers import (
    register_exception_handlers,
)
from app.stores.presentation.exceptions.store_exception_handlers import (
    register_store_exception_handlers
)
from app.users.presentation.controllers.users_controller import (
    router as users_router,
)

from app.stores.presentation.routers.public_stores_router import (
    router as public_stores_router,
)

from app.auth.presentation.routers.auth_router import (
    router as auth_router
)

from app.stores.presentation.routers.owner_stores_router import (
    router as owner_stores_router,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

register_exception_handlers(app)
register_store_exception_handlers(app)

# Register feature routers.
app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)
app.include_router(owner_stores_router)
app.include_router(public_stores_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "environment": settings.ENVIRONMENT,
    }