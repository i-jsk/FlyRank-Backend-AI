import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI

# Ensure current package path is available for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db
from routers.tasks import router as tasks_router

# Initialize SQLite database and seed table if empty (synchronous startup, zero async, zero deprecation warnings)
init_db()

# Initialize FastAPI application
app = FastAPI(
    title="Task API — SQLite Database Edition",
    description="FlyRank Backend AI Internship — Week 3 Assignment 1 (CRUD + SQLite).",
    version="1.0.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "list",
    },
)

# Register modular API router for /tasks endpoints
app.include_router(tasks_router)


@app.get("/", status_code=200, summary="Root API Metadata")
def read_root():
    """API metadata and available endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200, summary="Server Health Monitor")
def read_health():
    """Server health status check."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
