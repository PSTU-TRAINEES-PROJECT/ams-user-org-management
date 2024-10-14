from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from app.core.const import GREEN_BG, RESET

logging.basicConfig(level=logging.INFO)

class LogRequestPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"{GREEN_BG}Request path: {request.url.path}{RESET}")
        
        response = await call_next(request)
        
        return response



async def authenticate_header(request: Request):    
    return request.headers.get('X-User-ID')
