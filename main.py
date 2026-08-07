import uvicorn
from fastapi import FastAPI

# Initialize FastAPI application
app = FastAPI(
    title="FlyRank To-Do CRUD API",
    description="A small API managing a to-do list for FlyRank Backend AI Internship.",
    version="0.1.0",
)


@app.get("/", status_code=200)
def read_root():
    """Stage 0: Root endpoint confirming the server is online and serving requests."""
    return {"message": "Hello, server!", "status": "online"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
