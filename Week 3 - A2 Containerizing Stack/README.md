# W3 · A2 — Containerizing Stack 🐳

Welcome to **Week 3 - Assignment 2** of the FlyRank Backend AI Internship!

---

## 🎯 Purpose & Goal

Transition from SQLite file storage to a production-grade **PostgreSQL** database running inside a **Docker container**, then containerize the entire stack to start both the FastAPI application and PostgreSQL database with **one command** via **Docker Compose**.
- Manage database configuration securely via `.env`.
- Ensure data survives container restarts using a Docker named volume (`taskdata`).
- Run both services connected together in an isolated container network.

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

## 🚀 Running the Whole Stack in One Command

### 1. Start App + Database via Docker Compose
```bash
docker compose up -d --build
```

#### 🔍 Compose Services Architecture:
- **`api` service**: Built from [Dockerfile](Dockerfile), runs FastAPI on port `8000`. Connects to `DATABASE_URL=postgresql://postgres:dev@db:5432/tasks` (reaching the database using internal container hostname `db`).
- **`db` service**: Runs official `postgres:16` image, persists data into named volume `taskdata`.

---

### 2. Verify Running Services
```bash
docker compose ps
```
*(You will see both `api` and `db` running).*

---

### 3. Test API Endpoints via `curl.exe`
```powershell
# 1. Create task (201 Created)
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Docker Compose Task\"}"

# 2. List all tasks (200 OK)
curl.exe -i http://localhost:8000/tasks

# 3. Update task (200 OK)
curl.exe -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"done\":true}"

# 4. Delete task (204 No Content)
curl.exe -i -X DELETE http://localhost:8000/tasks/1
```

---

### 4. Verify Volume Persistence Across Stack Restarts
```powershell
# Stop and remove containers
docker compose down

# Bring stack back up
docker compose up -d

# Verify data still exists (survives restart!)
curl.exe -i http://localhost:8000/tasks
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
- [x] **Stage 3: Full CRUD on Postgres** — Complete `POST`, `PUT`, `DELETE` operations using SQL queries (`RETURNING *`) on containerized PostgreSQL.
- [x] **Stage 4: Docker-compose the whole stack** — Multi-container `Dockerfile` + `compose.yaml` starting `api` and `db` with volume persistence across full-stack restarts.
- [ ] **Stage 5: Final Documentation & Verification**.
