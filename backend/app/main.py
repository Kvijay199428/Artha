from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import AppException
from app.api.v1 import api_router
from app.seed_data import seed_all

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
seed_all()

app = FastAPI(
    title="GST Billing API",
    version="1.0.0",
    description="GST Billing Web Application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": {"code": exc.code, "message": exc.message, "fields": getattr(exc, "fields", None)}}
    )

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
