from typing import Optional
import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Initialize FastAPI application with rich OpenAPI metadata
# swagger_ui_parameters hides/collapses the Schemas section by default on page load
app = FastAPI(
    title="Task API — FlyRank To-Do CRUD Service",
    description=(
        "A small RESTful CRUD API managing an in-memory to-do list built for "
        "the FlyRank Backend AI Internship program."
    ),
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


# Pydantic schema for task creation request body
class TaskCreate(BaseModel):
    title: Optional[str] = None

    class Config:
        json_schema_extra = {"example": {"title": "Buy milk"}}


# Pydantic schema for task update request body
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    class Config:
        json_schema_extra = {"example": {"title": "Buy organic milk", "done": True}}


# In-memory data store initialized with 3 example tasks
tasks = [
    {"id": 1, "title": "Setup FastAPI project", "done": True},
    {"id": 2, "title": "Build Stage 2 read endpoints", "done": False},
    {"id": 3, "title": "Publish to GitHub", "done": False},
]


@app.get("/", status_code=200, summary="Root API Metadata")
def read_root():
    """Returns core API metadata including name, version, and primary endpoint paths."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200, summary="Server Health Monitor")
def read_health():
    """Returns operational uptime status of the server."""
    return {"status": "ok"}


@app.get("/tasks", status_code=200, summary="List All Tasks")
def get_all_tasks():
    """Retrieves the complete list of tasks currently stored in memory."""
    return tasks


@app.get("/tasks/{id}", summary="Get Single Task by ID")
def get_task_by_id(id: int):
    """Retrieves a single task matching the integer path parameter ID. Returns 404 if not found."""
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


@app.post("/tasks", status_code=201, summary="Create New Task")
def create_task(task_input: TaskCreate):
    """Creates a new task with input validation. Generates next ID, sets done=false, and returns 201 Created."""
    if not task_input.title or not task_input.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id": new_id, "title": task_input.title.strip(), "done": False}

    tasks.append(new_task)
    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{id}", status_code=200, summary="Update Task by ID")
def update_task(id: int, task_input: TaskUpdate):
    """Updates title and/or done status of an existing task matching ID. Returns 200 OK or 404 Not Found."""
    target_task = None
    for task in tasks:
        if task["id"] == id:
            target_task = task
            break

    if not target_task:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

    if task_input.title is None and task_input.done is None:
        return JSONResponse(
            status_code=400,
            content={
                "error": (
                    "At least one field (title or done) must be provided for update"
                )
            },
        )

    if task_input.title is not None:
        if not isinstance(task_input.title, str) or not task_input.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"},
            )
        target_task["title"] = task_input.title.strip()

    if task_input.done is not None:
        target_task["done"] = task_input.done

    return JSONResponse(status_code=200, content=target_task)


@app.delete("/tasks/{id}", status_code=204, summary="Delete Task by ID")
def delete_task(id: int):
    """Deletes an existing task matching ID. Returns 204 No Content or 404 Not Found."""
    for i, task in enumerate(tasks):
        if task["id"] == id:
            del tasks[i]
            return Response(status_code=204)

    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
