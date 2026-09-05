# Week 4 — Assignment 1: Auth Login & Protect

This module builds on top of the containerized stack from Week 3, integrating user authentication and route protection using **Supabase Auth** as the external Identity Provider (IdP) with our **FastAPI** backend and **PostgreSQL 16** database.

---

## Overview

In previous assignments, the API endpoints were unprotected, allowing unrestricted read, create, and delete access. This assignment introduces modern production-grade API security by establishing an authentication layer on top of our existing containerized Task stack.

Rather than implementing custom cryptography or password hashing from scratch, the system integrates with Supabase to manage user credentials, session security, and JSON Web Token (JWT) issuance.

### The Trust Triangle Architecture
The system operates on a three-tier security model:

1. **Client**: Authenticates with credentials (email and password) directly against the Identity Provider.
2. **Identity Provider (Supabase Auth)**: Validates credentials and returns a signed JWT access token.
3. **Backend Server (FastAPI)**: Verifies incoming JWTs attached to the `Authorization: Bearer <token>` header, unlocking protected routes (such as user profiles and task management).

---

## Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.12 | Modern typed Python runtime |
| **Framework** | FastAPI | High-performance API framework with automatic Swagger UI |
| **Database** | PostgreSQL 16 | Relational database engine for persistent application data |
| **Database Adapter** | `psycopg` (v3) | PostgreSQL database adapter with binary extensions |
| **Identity Provider** | Supabase Auth | Managed authentication service and JWT issuer |
| **Python SDK** | `supabase` (v2.31.0) | Official Python client library for Supabase |
| **Containers** | Docker & Docker Compose | Multi-container stack orchestration (`api` + `db`) |
| **Configuration** | `python-dotenv` | Environment variable management |

---

## Environment Configuration

Configuration is managed via environment variables. Before starting the service, copy `.env.example`:

```bash
cp .env.example .env
```

### Configuration Variables ([.env.example](.env.example)):
| Variable | Example Value | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://postgres:dev@db:5432/tasks` | Internal connection string for PostgreSQL |
| `POSTGRES_USER` | `postgres` | Database administrator username |
| `POSTGRES_PASSWORD` | `dev` | Database administrator password |
| `POSTGRES_DB` | `tasks` | Initial application database name |
| `POSTGRES_PORT` | `5432` | PostgreSQL database port |
| `SUPABASE_URL` | `https://<project-ref>.supabase.co` | Supabase project API URL (Project Settings -> API) |
| `SUPABASE_KEY` | `your_anon_key` | Supabase anonymous public API key |
| `PORT` | `3000` | Application server port |

> [!NOTE]
> `.env` is excluded from version control via `.gitignore` to prevent secret exposure. Only `.env.example` is tracked.

---

## Quick Start (Docker Compose)

Start the entire stack (FastAPI API server + PostgreSQL database) with one command:

```bash
docker compose up -d --build
```

To view container logs:
```bash
docker compose logs -f api
```

To stop and remove containers:
```bash
docker compose down
```

---

## Local Development (Standalone)

To run the FastAPI server directly in a local Python virtual environment:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```
   *(or `uvicorn main:app --host 0.0.0.0 --port 3000 --reload`)*

---

## Stage 0 Checkpoint Verification

When the stack initializes, the API container connects to both the PostgreSQL database and the Supabase Identity Provider, logging:

```text
INFO:     Started server process [7]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
Database connected and initialized successfully.
Server running and connected to Supabase
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

### Verification Query 1: Root Metadata (`GET /`)
```text
$ curl.exe -i http://localhost:3000/

HTTP/1.1 200 OK
content-type: application/json

{"status":"online","message":"Server running and connected to Supabase","endpoints":["/tasks","/docs","/health"]}
```

### Verification Query 2: Persisted Tasks (`GET /tasks`)
```text
$ curl.exe -i http://localhost:3000/tasks

HTTP/1.1 200 OK
content-type: application/json

[
  {"id":1,"title":"Setup FastAPI project","done":true},
  {"id":2,"title":"Build Stage 2 read endpoints","done":false},
  {"id":3,"title":"Publish to GitHub","done":false}
]
```

Interactive Swagger UI documentation is available at:
```text
http://localhost:3000/docs
```

---

## API Endpoints Matrix

| Operation | HTTP Method | Path | Access Level | Description |
| :--- | :---: | :--- | :--- | :--- |
| **Root Metadata** | `GET` | `/` | Public | System status and available endpoints |
| **Health Monitor** | `GET` | `/health` | Public | Server uptime and status |
| **List Tasks** | `GET` | `/tasks` | Open / Pre-auth | Retrieves tasks from PostgreSQL database |
| **Get Task by ID** | `GET` | `/tasks/{id}` | Open / Pre-auth | Retrieves single task by primary key |
| **Create Task** | `POST` | `/tasks` | Open / Pre-auth | Inserts new task into database |
| **Update Task** | `PUT` | `/tasks/{id}` | Open / Pre-auth | Updates task title or done state |
| **Delete Task** | `DELETE` | `/tasks/{id}` | Open / Pre-auth | Deletes task row from database |
| **Sign Up** | `POST` | `/auth/signup` | Public | Registers a new user account (Upcoming) |
| **Log In** | `POST` | `/auth/login` | Public | Authenticates user & returns JWT (Upcoming) |
| **Log Out** | `POST` | `/auth/logout` | Protected | Terminates user session (Upcoming) |
| **User Profile** | `GET` | `/protected/profile` | Protected | Returns private user profile data (Upcoming) |
| **Public Info** | `GET` | `/public/info` | Public | Returns general public information (Upcoming) |
