from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import Any, Optional

class CustomResponseHandler:
    @staticmethod
    def success(message: str, data: Optional[Any] = None, status_code: int = HTTPStatus.OK ) -> JSONResponse:
        content = {"message": message}
        if data is not None:
            content["data"] = data
        return JSONResponse(
            status_code=status_code,
            content=content
        )

    @staticmethod
    def error( message: str, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR, errors: Optional[list] = None ) -> JSONResponse:
        content = {"message": message}
        if errors:
            content["errors"] = errors
        return JSONResponse(
            status_code=status_code,
            content=content
        )
