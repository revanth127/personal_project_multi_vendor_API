import time
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import json

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
                "timestamp": start_time
            }
        )
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log successful response
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time": round(process_time, 4),
                    "timestamp": time.time()
                }
            )
            
            # Add process time header
            response.headers["X-Process-Time"] = str(round(process_time, 4))
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            
            # Log error
            logger.error(
                "Request failed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e),
                    "process_time": round(process_time, 4),
                    "timestamp": time.time()
                }
            )
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
