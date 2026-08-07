# W2 · A1 — First CRUD API

Welcome to **Week 2 - Assignment 1** of the FlyRank Backend AI Internship!

---

## Purpose & Goal

Build an in-memory To-Do list API stage-by-stage to master core backend concepts: REST principles, endpoint routing, HTTP status codes, request validation, and interactive documentation via Swagger UI.

---

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Documentation**: Swagger UI (`/docs`)

---

## Stage Progress Roadmap

- [x] **Stage 0: Hello, server** — Server startup (`GET /` returning 200 OK & hello message).
- [x] **Stage 1: Root & Health endpoints** — API metadata (`GET /`) & health check (`GET /health`).
- [x] **Stage 2: Read endpoints** — List all tasks (`GET /tasks`) & single task (`GET /tasks/{id}`) with 404 handling.
- [x] **Stage 3: Create endpoint** — Add new task (`POST /tasks`) with 201 Created & 400 validation.
- [x] **Stage 4: Update & Delete endpoints** — Modify task (`PUT /tasks/{id}`) & delete task (`DELETE /tasks/{id}` 204 No Content).
- [x] **Stage 5: Swagger UI Verification** — Interactive visual documentation at `http://localhost:8000/docs`.

---

## Interactive Swagger UI (`/docs`)

FastAPI automatically generates interactive OpenAPI documentation at **[http://localhost:8000/docs](http://localhost:8000/docs)**:

![Swagger UI Screenshot](Swagger%20UI-%20CRUD%20API.png)

### Verified Endpoints:
- **Root & Health**: `GET /`, `GET /health`
- **Create**: `POST /tasks` (Try it out with `{"title": "Buy milk"}`)
- **Read**: `GET /tasks`, `GET /tasks/{id}`
- **Update**: `PUT /tasks/{id}` (Try it out with `{"done": true}`)
- **Delete**: `DELETE /tasks/{id}` (Returns `204 No Content`)

---

## How to Run & Verify

1. **Navigate to this folder**:
   ```bash
   cd "Week 2 - A1 CRUD API"
   ```

2. **Run Server**:
   ```bash
   python main.py
   ```

3. **Endpoints & Swagger UI**:
   - Interactive Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Root Metadata: `curl -i http://localhost:8000/`
   - Health Monitor: `curl -i http://localhost:8000/health`
   - List All Tasks: `curl -i http://localhost:8000/tasks`
   - Get Task 1: `curl -i http://localhost:8000/tasks/1`
   - Create Task: `curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"`
   - Update Task: `curl -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"done\":true}"`
   - Delete Task: `curl -i -X DELETE http://localhost:8000/tasks/1`
