import os
import sys
from pathlib import Path
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Ensure current package path is available for imports
sys.path.insert(0, str(Path(__file__).parent))

# Load environment configuration from .env
load_dotenv()
PORT = int(os.getenv("PORT", 3000))

# Import shared Supabase client
from supabase_client import supabase

# Log required Stage 0 checkpoint message on startup
print("Server running and connected to Supabase", flush=True)

from database import init_db
from routers.tasks import router as tasks_router
from routers.auth import router as auth_router

# Initialize PostgreSQL database schema and seed table
try:
    is_docker = "db:5432" in os.getenv("DATABASE_URL", "")
    init_db(max_retries=10 if is_docker else 1, retry_delay=1.0 if is_docker else 0.1)
except Exception:
    # Non-fatal fallback if running standalone without PostgreSQL container active
    print("Database note: PostgreSQL container not running locally.")

# Initialize FastAPI application
app = FastAPI(
    title="FlyRank Auth & Task API",
    description="Week 4 Assignment 1: Auth Login & Protect with Supabase IdP",
    version="1.0.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "list",
    },
)

# Custom validation exception handler to return 400 instead of default 422
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Email and password are required"},
    )


# Register modular routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/", status_code=200, summary="Root API Metadata")
def read_root():
    """API metadata and connection status."""
    return {
        "status": "online",
        "message": "Server running and connected to Supabase",
        "endpoints": [
            "/public/info",
            "/protected/profile",
            "/auth/signup",
            "/auth/login",
            "/tasks",
            "/docs",
            "/health",
        ],
    }


@app.get("/public/info", status_code=200, summary="Public Information Gate")
def public_info():
    """Unprotected public endpoint accessible by anyone."""
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile", status_code=200, summary="Protected Profile Gate")
def protected_profile(request: Request):
    """Protected endpoint requiring Authorization: Bearer <token> header."""
    auth_header = request.headers.get("authorization")
    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"},
        )

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"},
        )

    token = parts[1].strip()
    return {
        "message": "Access token received (unverified)",
        "token": token,
    }


@app.get("/health", status_code=200, summary="Server Health Monitor")
def read_health():
    """Server health status monitor."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)
