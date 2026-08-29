# Week 3 — Assignment 2: Containerizing Stack

This module contains the containerized implementation of the Task CRUD API developed for the FlyRank Backend AI Internship.

---

## Overview

A production-ready **Task CRUD REST API** built with **FastAPI** and **PostgreSQL 16**.
- The entire stack (FastAPI web application + PostgreSQL relational database) runs in isolated Docker containers on a shared bridge network.
- Configuration and database credentials are managed through environment variables (`.env`).
- Persistent storage is guaranteed across container restarts using a Docker named volume (`taskdata`).

---

## Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.12 | Modern typed Python |
| **Framework** | FastAPI | High-performance Python web API framework |
| **Database** | PostgreSQL 16 | Relational database server |
| **Database Driver** | `psycopg` (v3) | PostgreSQL database adapter with binary extensions |
| **Configuration** | `python-dotenv` | Environment variable management |
| **Container Engine** | Docker & Docker Compose | Multi-container lifecycle and volume orchestration |

---

## Quick Start Guide (One Command)

Start both the FastAPI application and PostgreSQL database with a single command:

```bash
docker compose up -d --build
```

To stop and tear down the stack:
```bash
docker compose down
```

---

## Environment Configuration

Configuration is managed via environment variables. Before starting the stack, copy the example template:

```bash
cp .env.example .env
```

### Required Variables ([.env.example](.env.example)):
| Variable | Example Value | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://postgres:dev@db:5432/tasks` | Internal connection string for API container |
| `POSTGRES_USER` | `postgres` | Database administrator username |
| `POSTGRES_PASSWORD` | `dev` | Database password |
| `POSTGRES_DB` | `tasks` | Initial database name |
| `POSTGRES_PORT` | `5432` | Database port |

> [!NOTE]
> `.env` is git-ignored for security. Only `.env.example` is committed to the repository.

---

## API Endpoints Matrix

| Operation | HTTP Method | Path | Status Codes | Description |
| :--- | :---: | :--- | :---: | :--- |
| **Root Metadata** | `GET` | `/` | `200 OK` | Core API metadata and available endpoint index |
| **Health Monitor** | `GET` | `/health` | `200 OK` | Health uptime status (`{"status": "ok"}`) |
| **List All Tasks** | `GET` | `/tasks` | `200 OK` | Retrieves all tasks from PostgreSQL database |
| **Get Task by ID** | `GET` | `/tasks/{id}` | `200 OK`, `404 Not Found` | Retrieves single task by primary key |
| **Create Task** | `POST` | `/tasks` | `201 Created`, `400 Bad Request` | Inserts a new task (`RETURNING id, title, done`) |
| **Update Task** | `PUT` | `/tasks/{id}` | `200 OK`, `400 Bad Request`, `404 Not Found` | Updates title/done status in PostgreSQL |
| **Delete Task** | `DELETE` | `/tasks/{id}` | `204 No Content`, `404 Not Found` | Deletes task row from database |

---

## Pasted `curl -i` Request & Response Example Below

### 1. List Tasks (`GET /tasks`)
```text
$ curl.exe -i http://localhost:8000/tasks

HTTP/1.1 200 OK
date: Sat, 29 Aug 2026 16:22:50 GMT
server: uvicorn
content-length: 167
content-type: application/json

[
  {"id": 1, "title": "Setup FastAPI project", "done": true},
  {"id": 2, "title": "Build Stage 2 read endpoints", "done": false},
  {"id": 3, "title": "Publish to GitHub", "done": false}
]
```

### 2. Create Task (`POST /tasks`)
```text
$ curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "Docker Compose Task"}'

HTTP/1.1 201 Created
date: Sat, 29 Aug 2026 16:23:05 GMT
server: uvicorn
content-length: 56
content-type: application/json

{"id": 4, "title": "Docker Compose Task", "done": false}
```

---

## Database Inspection in PostgreSQL Container

### 1. Table Relations (`\dt` in `psql`)
```text
$ docker compose exec db psql -U postgres -d tasks -c "\dt"

         List of relations
 Schema | Name  | Type  |  Owner   
--------+-------+-------+----------
 public | tasks | table | postgres
(1 row)
```

### 2. Query Seeded & Persisted Rows
```text
$ docker compose exec db psql -U postgres -d tasks -c "SELECT * FROM tasks;"

 id |            title             | done 
----+------------------------------+------
  1 | Setup FastAPI project        | t
  2 | Build Stage 2 read endpoints | f
  3 | Publish to GitHub            | f
(3 rows)
```

---

## Stage Progress Roadmap

- [x] **Stage 0: Postgres in Docker + gitignore** — Launch PostgreSQL container with persistent volume, configure `.env.example` & `.gitignore`.
- [x] **Stage 1: Connect via .env and create table** — Load `DATABASE_URL` via `python-dotenv`, connect using `psycopg`, create `tasks` table, and seed 3 initial tasks.
- [x] **Stage 2: Read from Postgres** — Parameterized `GET /tasks` and `GET /tasks/{id}` reading directly from PostgreSQL with 404 error handling.
- [x] **Stage 3: Full CRUD on Postgres** — Complete `POST`, `PUT`, `DELETE` operations using SQL queries (`RETURNING *`) on containerized PostgreSQL.
- [x] **Stage 4: Docker-compose the whole stack** — Multi-container `Dockerfile` + `compose.yaml` starting `api` and `db` with volume persistence across full-stack restarts.
- [x] **Stage 5: Publish to GitHub & One-command stack documentation** — Completed documentation, endpoint table, pasted `curl` output, and fresh clone verification.
