from fastapi.exceptions import RequestValidationError
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.middleware import CustomLogRequestPathMiddleware
from core import const, auth
from config import get_config, validation_exception_handler
from routers.api.v1 import user_router, organization_router, service_profile_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title=get_config().project_title,
    docs_url="/api/docs",
    debug=True
)

app.mount("/uploads/profile_images", StaticFiles(directory="uploads/profile_images"), name="profile_images")

app.add_middleware(
    CORSMiddleware, allow_headers=["*"], allow_origins=["*"], allow_methods=["*"]
)

app.add_middleware(CustomLogRequestPathMiddleware)

app.include_router(
    user_router,
    prefix=const.API_STR,
    tags=["Users Management"]
)

app.include_router(
    organization_router,
    prefix=const.API_STR,
    tags=["Organization Management"]
)
app.include_router(
    service_profile_router,
    prefix=const.API_STR,
    tags=["Service Management"]
)


# Register the events
# app.add_event_handler("startup", auth.on_startup)
# app.add_event_handler("shutdown", auth.on_shutdown)


# Register the custom validation error handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=get_config().is_reload,
        port=get_config().backend_port,
    )
