import uvicorn
from fastapi import FastAPI

# Initialize FastAPI application
app = FastAPI(
    title="Task API",
    description="A small API managing a to-do list for FlyRank Backend AI Internship.",
    version="1.0",
)


@app.get("/", status_code=200)
def read_root():
    """Root endpoint returning API metadata and available endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", status_code=200)
def read_health():
    """Health check endpoint used to verify that the server is operational."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
