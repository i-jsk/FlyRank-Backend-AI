# W3 · A2 — Containerizing Stack 🐳

Welcome to **Week 3 - Assignment 2** of the FlyRank Backend AI Internship!

---

## 🎯 Purpose & Goal

Transition from SQLite file storage to a production-grade **PostgreSQL** database running inside a **Docker container**.
- Manage database configuration securely via `.env`.
- Ensure data survives restarts using a Docker named volume (`taskdata`).
- Eventually run both the application and database together via Docker Compose.

---

## 🛠️ Technology Stack (Python Lane)

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ (3.12) | Modern typed Python |
| **Framework** | FastAPI | High-performance Python web framework |
| **Database** | PostgreSQL 16 | Containerized relational database |
| **Database Driver** | `psycopg` (v3 with binary) | Official PostgreSQL database adapter |
| **Configuration** | `python-dotenv` | Loads `.env` configuration securely |
| **Container Engine** | Docker Desktop / Podman | Container runtime and volume manager |
| **Orchestration** | Docker Compose | Multi-container orchestration (`compose.yaml`) |

---

## 🚀 Running the Stack

### 1. Launch PostgreSQL Container in One Command
```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:16
```

### 2. Configure Environment (`.env`)
Create a `.env` file (copied from `.env.example`):
```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

### 3. Run FastAPI Application
```bash
python main.py
```

### 4. Test Read Endpoints
```bash
# List all tasks (200 OK)
curl -i http://localhost:8000/tasks

# Get single task (200 OK)
curl -i http://localhost:8000/tasks/1

# Get non-existent task (404 Not Found)
curl -i http://localhost:8000/tasks/999
```

---

## 📊 Database Schema (`tasks` table in PostgreSQL)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | `PRIMARY KEY` | Unique auto-incrementing task ID |
| `title` | `TEXT` | `NOT NULL` | Description of the task |
| `done` | `BOOLEAN` | `NOT NULL DEFAULT FALSE` | Task completion status (`TRUE` / `FALSE`) |

---

## 🚦 Stage Progress Roadmap

- [x] **Stage 0: Postgres in Docker + gitignore** — Launch PostgreSQL container with persistent volume, configure `.env.example` & `.gitignore`.
- [x] **Stage 1: Connect via .env and create table** — Load `DATABASE_URL` via `python-dotenv`, connect using `psycopg`, create `tasks` table, and seed 3 initial tasks.
- [x] **Stage 2: Read from Postgres** — Parameterized `GET /tasks` and `GET /tasks/{id}` reading directly from PostgreSQL with 404 error handling.
- [ ] **Stage 3: Full CRUD on Postgres** — Verify create, update, delete endpoints against PostgreSQL.
- [ ] **Stage 4: Containerize Application** — Create `Dockerfile` and build app image.
- [ ] **Stage 5: Docker Compose Stack** — Start app + Postgres with one `docker compose up` command.
