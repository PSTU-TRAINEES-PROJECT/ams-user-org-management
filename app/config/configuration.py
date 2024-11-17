from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    project_title: str
    backend_port: int
    is_reload: bool
    database_url: str

    class Config:
        env_path = ".env"


@lru_cache()
def get_config():
    return Config()


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = [
        {
            "field": error["loc"][-1],
            "message": error["msg"],  # The actual error message
        }
        for error in errors
    ]
    return JSONResponse(
        status_code=400,
        content={"message": "Validation failed", "errors": custom_errors}
    )