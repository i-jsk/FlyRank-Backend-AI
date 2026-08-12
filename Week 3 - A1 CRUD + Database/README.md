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
- [x] **Stage 4: Explored SQLite** — Executed manual SQL queries (`SELECT`, `WHERE`, `COUNT`, `UPDATE`, `DELETE`) & verified direct DB-to-API reflections.
- [ ] **Stage 5: Database documentation** — Final database documentation, schema specs, and Swagger UI integration.

---

## 🗄️ Stage 4: Manual SQL Exploration Queries

The following 5 standard SQL queries were executed against `tasks.db`:

1. **List every task**:
   ```sql
   SELECT * FROM tasks;
   ```
2. **Show only completed tasks**:
   ```sql
   SELECT * FROM tasks WHERE done = 1;
   ```
3. **Count all tasks**:
   ```sql
   SELECT COUNT(*) FROM tasks;
   ```
4. **Mark every task as completed**:
   ```sql
   UPDATE tasks SET done = 1;
   ```
5. **Delete all completed tasks**:
   ```sql
   DELETE FROM tasks WHERE done = 1;
   ```

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

3. **Interactive Swagger UI**:
   - Open **[http://localhost:8000/docs](http://localhost:8000/docs)** to test all CRUD endpoints visually!

4. **Verify Endpoints via `curl`**:
   - **Root Metadata**: `curl -i http://localhost:8000/`
   - **Health Monitor**: `curl -i http://localhost:8000/health`
   - **List All Tasks**: `curl -i http://localhost:8000/tasks`
   - **Get Task 1**: `curl -i http://localhost:8000/tasks/1`
   - **Create Task**: `curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"`
   - **Update Task**: `curl -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"done\":true}"`
   - **Delete Task**: `curl -i -X DELETE http://localhost:8000/tasks/1`
