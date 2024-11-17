from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import logger

class CustomLogRequestPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(
            f"API Call | {request.method} {request.url.path} | "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )
        response = await call_next(request)
        
        if 200 <= response.status_code < 400:
            logger.debug(
                f"API Response | {request.method} {request.url.path} | "
                f"Client: {request.client.host if request.client else 'Unknown'} | "
                f"Status: {response.status_code}"
            )
        else:
            logger.warning(
                f"API Response | {request.method} {request.url.path} | "
                f"Client: {request.client.host if request.client else 'Unknown'} | "
                f"Status: {response.status_code}"
            )
            
        return response

async def authenticate_header(request: Request):    
    return request.headers.get('X-User-ID')
