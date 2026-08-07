import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Initialize FastAPI application
app = FastAPI(
    title="Task API",
    description="A small API managing a to-do list for FlyRank Backend AI Internship.",
    version="1.0",
)

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
