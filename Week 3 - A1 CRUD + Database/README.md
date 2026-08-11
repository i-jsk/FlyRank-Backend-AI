# W3 · A1 — CRUD + Database 🗄️

Welcome to **Week 3 - Assignment 1** of the FlyRank Backend AI Internship!

---

## Purpose & Goal

Replace the in-memory array storage from Week 2 with a persistent **SQLite** database (`tasks.db`). The API endpoints continue to behave identically, but data now survives server restarts!

---

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **Database**: SQLite 3 (`tasks.db`)
- **Library**: `sqlite3` (Built-in Python Standard Library)
- **ASGI Server**: Uvicorn
- **Documentation**: Swagger UI (`/docs`)

---

## Database Schema (`tasks` table)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique auto-incrementing task ID |
| `title` | `TEXT` | `NOT NULL` | Description of the task |
| `done` | `BOOLEAN` | `NOT NULL DEFAULT 0` | Task completion status (`0` / `1`) |

---

## Stage Progress Roadmap

- [x] **Stage 0: Create SQLite Database** — Auto-create `tasks.db`, `tasks` table, and seed 3 initial tasks if empty.
- [x] **Stage 1: Read endpoints from DB** — `GET /tasks` & `GET /tasks/{id}` reading directly from SQLite with 404 handling.
- [x] **Stage 2: Create endpoint to DB** — `POST /tasks` inserting rows into SQLite with 201 Created & 400 validation.
- [x] **Stage 3: Update & Delete endpoints in DB** — `PUT /tasks/{id}` updating SQLite rows & `DELETE /tasks/{id}` removing rows (`204 No Content`).
- [ ] **Stage 4: Swagger UI & Persistence Verification**.

---

## How to Run & Verify

1. **Navigate to this folder**:
   ```bash
   cd "Week 3 - A1 CRUD + Database"
   ```

2. **Run Server**:
   ```bash
   python main.py
   ```

3. **Verify Stage 3 Update & Delete Endpoints**:
   - **Update Task**: `curl -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"done\":true}"` (Returns `200 OK`)
   - **Delete Task**: `curl -i -X DELETE http://localhost:8000/tasks/1` (Returns `204 No Content`)
   - **Confirm Deletion**: `curl -i http://localhost:8000/tasks/1` (Returns `404 Not Found`)
