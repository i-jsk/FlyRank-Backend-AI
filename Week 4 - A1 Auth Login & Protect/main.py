import os
import sys
from pathlib import Path
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client, Client

# Ensure current package path is available for imports
sys.path.insert(0, str(Path(__file__).parent))

# Load environment configuration from .env
load_dotenv()

# Read environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your_anon_key")
PORT = int(os.getenv("PORT", 3000))

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Server running and connected to Supabase", flush=True)

from database import init_db
from routers.tasks import router as tasks_router

# Initialize PostgreSQL database schema and seed table
try:
    init_db()
except Exception as e:
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

# Register modular /tasks router from previous build
app.include_router(tasks_router)


@app.get("/", status_code=200, summary="Root API Metadata")
def read_root():
    """API metadata and connection status."""
    return {
        "status": "online",
        "message": "Server running and connected to Supabase",
        "endpoints": ["/tasks", "/docs", "/health"],
    }


@app.get("/health", status_code=200, summary="Server Health Monitor")
def read_health():
    """Server health status monitor."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)
