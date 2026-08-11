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
- [x] **Stage 2: Create endpoint to DB** — `POST /tasks` inserting rows into SQLite with 201 Created & 400 validation. Data survives server restarts!
- [ ] **Stage 3: Update endpoint in DB** — `PUT /tasks/{id}` updating SQLite row.
- [ ] **Stage 4: Delete endpoint in DB** — `DELETE /tasks/{id}` removing SQLite row.
- [ ] **Stage 5: Swagger UI & Persistence Verification**.

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

3. **Verify Stage 2 Create & Persistence Endpoints**:
   - **Create Task**: `curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"` (Returns `201 Created`)
   - **Create Invalid Task**: `curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{}"` (Returns `400 Bad Request`)
   - **Verify Persistence**: Stop and restart `python main.py`, then run `curl -i http://localhost:8000/tasks` to confirm new tasks persist in `tasks.db`!
