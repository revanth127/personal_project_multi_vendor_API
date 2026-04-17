from fastapi import FastAPI
from app.database import engine
from app.database import Base
import app.models as models
from app.api.v1.api import api_router
from app.middleware.logging import LoggingMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Multi-Vendor Marketplace API",
    description="A FastAPI-based multi-vendor marketplace with role-based access control",
    version="1.0.0"
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include API v1 routes
app.include_router(api_router)

