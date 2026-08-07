from typing import Optional
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI(
    title="Task API",
    description="A small API managing a to-do list for FlyRank Backend AI Internship.",
    version="1.0",
)


# Pydantic model for task creation payload validation and Swagger UI documentation
class TaskCreate(BaseModel):
    title: Optional[str] = None


# In-memory data store with 3 initial example tasks
tasks = [
    {"id": 1, "title": "Setup FastAPI project", "done": True},
    {"id": 2, "title": "Build Stage 2 read endpoints", "done": False},
    {"id": 3, "title": "Publish to GitHub", "done": False},
]


@app.get("/", status_code=200)
def read_root():
    """Root endpoint returning API metadata and available endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200)
def read_health():
    """Health check endpoint used to verify that the server is operational."""
    return {"status": "ok"}


@app.get("/tasks", status_code=200)
def get_all_tasks():
    """Retrieve the complete list of tasks."""
    return tasks


@app.get("/tasks/{id}")
def get_task_by_id(id: int):
    """Retrieve a single task by its integer ID. Returns 404 if not found."""
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


@app.post("/tasks", status_code=201)
def create_task(task_input: TaskCreate):
    """Create a new task with input validation.

    Generates the next available ID, defaults done to False, and returns 201 Created.
    Returns 400 Bad Request if title is missing or empty.
    """
    # Business rule validation: title must exist, be a non-empty string
    if not task_input.title or not task_input.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    # Generate next free ID (handles empty list safely)
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id": new_id, "title": task_input.title.strip(), "done": False}

    tasks.append(new_task)
    return JSONResponse(status_code=201, content=new_task)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
