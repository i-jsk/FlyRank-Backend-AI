# Week 4 — Assignment 1: Auth Login & Protect

This module builds on top of the containerized stack from Week 3, integrating user authentication and route protection using **Supabase Auth** as the external Identity Provider (IdP) with our **FastAPI** backend and **PostgreSQL 16** database.

---

## Overview

Task API is a production-grade RESTful service built with **Python 3.12** and **FastAPI** for the FlyRank Backend Internship. It combines containerized relational persistence in **PostgreSQL 16** with secure, identity-provider-backed authentication powered by **Supabase Auth**.

The service manages tasks with full CRUD operations, advanced query parameters (filtering, search, pagination), and automatic seed data. Security is managed through **JSON Web Tokens (JWT)**: users register and log in via Supabase, receive signed bearer tokens, and access protected application endpoints guarded by reusable FastAPI dependencies.

The entire architecture is containerized with **Docker** and orchestrated via **Docker Compose**, with PostgreSQL data persisted on a dedicated named volume.

---

## The Trust Triangle Architecture

The API implements the classic three-tier Identity Provider pattern:

```text
  +------------------+         1. Credentials (email, password)       +-----------------------+
  |                  | ---------------------------------------------> |                       |
  |      Client      |                                                |     Supabase Auth     |
  | (Swagger / curl) | <--------------------------------------------- |   (Identity Provider) |
  |                  |         2. Signed JWT (access_token)           |                       |
  +------------------+                                                +-----------------------+
           |
           | 3. Protected Request
           |    Header: Authorization: Bearer <access_token>
           v
  +-------------------------------------------------------------------------------------------+
  | FastAPI Backend Server (Resource Server on Port 3000)                                     |
  |                                                                                           |
  |  [ Dependencies Guard: get_current_user ]                                                 |
  |   -> Validates cryptographic JWT signature with Supabase SDK                              |
  |   -> Rejects missing tokens: 401 Unauthorized ("Access token required")                   |
  |   -> Rejects invalid/expired tokens: 401 Unauthorized ("Invalid or expired token")        |
  |   -> Extracts verified user metadata and authorizes downstream endpoint execution         |
  |                                                                                           |
  |  [ Endpoints & Relational Database ]                                                      |
  |   -> /protected/profile, /protected/dashboard, /auth/logout                               |
  |   -> /tasks CRUD via psycopg (v3) -> PostgreSQL 16 Database Container                     |
  +-------------------------------------------------------------------------------------------+
```

---

## Tech Stack

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.12 | Modern typed asynchronous Python runtime |
| **Framework** | FastAPI | High-performance API framework with OpenAPI / Swagger UI |
| **Authentication** | Supabase Auth | Identity Provider (IdP) for password security & JWT issuance |
| **Python SDK** | `supabase` (v2.31.0) | Official Supabase client for authentication & user retrieval |
| **Database** | PostgreSQL 16 | ACID-compliant relational persistence engine |
| **Database Driver** | `psycopg` (v3) | High-performance PostgreSQL database adapter |
| **Containerization** | Docker | Container specification for reproducible deployments |
| **Orchestration** | Docker Compose | Multi-container coordination (`api` + `db`) |
| **Server** | Uvicorn | Lightning-fast ASGI web server |
| **Configuration** | `python-dotenv` | 12-Factor environment configuration |

---

## Quickstart: Run in Under 5 Minutes

### 1. Clone the Repository
```bash
git clone https://github.com/i-jsk/FlyRank-Backend-AI.git
cd "FlyRank-Backend-AI/Week 4 - A1 Auth Login & Protect"
```

### 2. Configure Environment Variables
Copy the `.env.example` template to `.env`:
```bash
cp .env.example .env
```

Open `.env` and plug in your Supabase project credentials:
```env
DATABASE_URL=postgresql://postgres:dev@db:5432/tasks
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dev
POSTGRES_DB=tasks
POSTGRES_PORT=5432

SUPABASE_URL=https://<your-project-ref>.supabase.co
SUPABASE_KEY=<your-anon-public-key>
PORT=3000
```

> [!TIP]
> **One-Time Supabase Dashboard Setting**:
> Under **Authentication -> Providers -> Email**, turn **Confirm email** off so newly created accounts can log in immediately without waiting for an email confirmation link.

### 3. Build and Start With Docker Compose
```bash
docker compose up -d --build
```

The services will initialize automatically:
- PostgreSQL container spins up and establishes the `tasks` schema with seed tasks.
- FastAPI container starts on port `3000` and connects to both PostgreSQL and Supabase.

API Root:
```text
http://localhost:3000
```

Interactive Swagger UI Documentation:
```text
http://localhost:3000/docs
```

To view live container logs:
```bash
docker compose logs -f api
```

To stop the services:
```bash
docker compose down
```

To stop and remove persistent database storage:
```bash
docker compose down -v
```

---

## Standalone Development (Without Docker)

You can also run FastAPI directly on the host machine using Python while keeping PostgreSQL running in Docker (or on a local PostgreSQL instance):

```bash
# 1. Create and activate a Python virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env for host connection (use localhost instead of db hostname)
# DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks

# 4. Start the application
python main.py
# or: uvicorn main:app --host 127.0.0.1 --port 3000 --reload
```

---

## Environment Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://postgres:dev@db:5432/tasks` | PostgreSQL connection URI for `psycopg` |
| `POSTGRES_USER` | `postgres` | Database administrator username |
| `POSTGRES_PASSWORD` | `dev` | Database administrator password |
| `POSTGRES_DB` | `tasks` | Relational database name |
| `POSTGRES_PORT` | `5432` | Database port exposed to host |
| `SUPABASE_URL` | `https://your-project.supabase.co` | Supabase project API gateway URL |
| `SUPABASE_KEY` | `your_anon_key` | Supabase anonymous public client API key |
| `PORT` | `3000` | FastAPI server listening port |

> [!CRITICAL]
> **Secret Security**: The `.env` file containing private credentials is listed in `.gitignore` and is never committed to GitHub. Only `.env.example` with dummy values is tracked.

---

## Interactive Swagger UI Documentation

FastAPI automatically generates interactive OpenAPI documentation at:
```text
http://localhost:3000/docs
```

### Visualizing the Secure Doors
Protected endpoints feature a padlock icon on the route bar. The global **Authorize** button allows pasting the JWT access token once to test all guarded endpoints across the session:

![Swagger UI Authorize and Routes](Swagger%20UI-%20Authorize%20%26%20Routes.jpeg)

#### Using the Authorize Button:
1. Execute `POST /auth/login` to obtain an `access_token`.
2. Click the green **Authorize** padlock button at the top right.
3. Paste the token string into the **Value** input field and click **Authorize**, then click **Close**.
4. Test any protected route (`/protected/profile`, `/protected/dashboard`, `/auth/logout`) with **Try it out** -> **Execute**.

---

## API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint | Description | Access Level | Success | Error Responses |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `POST` | `/auth/signup` | Register new user account in Supabase | Public | `201 Created` | `400 Bad Request` (missing/empty credentials) |
| `POST` | `/auth/login` | Authenticate user and issue JWT | Public | `200 OK` | `400 Bad Request`, `401 Unauthorized` |
| `POST` | `/auth/logout` | Terminate session and revoke JWT | Protected | `204 No Content` | `401 Unauthorized` (missing or invalid token) |

### Public & System Endpoints

| Method | Endpoint | Description | Access Level | Response |
| :--- | :--- | :--- | :---: | :---: |
| `GET` | `/` | API status, greeting, and available endpoints | Public | `200 OK` |
| `GET` | `/health` | Server health check and uptime monitor | Public | `200 OK` |
| `GET` | `/public/info` | Unprotected informational announcement | Public | `200 OK` |
| `GET` | `/docs` | Interactive Swagger UI documentation | Public | `200 OK` |

### Protected Endpoints

All protected endpoints require the header:
```http
Authorization: Bearer <access_token>
```

| Method | Endpoint | Description | Access Level | Response |
| :--- | :--- | :--- | :---: | :---: |
| `GET` | `/protected/profile` | Retrieve verified user identity & metadata | Protected | `200 OK` / `401 Unauthorized` |
| `GET` | `/protected/dashboard` | Protected dashboard verifying guard reuse | Protected | `200 OK` / `401 Unauthorized` |
| `POST` | `/auth/logout` | Terminate user session in Supabase | Protected | `204 No Content` / `401 Unauthorized` |

### Task Management Endpoints (PostgreSQL CRUD)

| Method | Endpoint | Description | Access Level | Response |
| :--- | :--- | :--- | :---: | :---: |
| `GET` | `/tasks` | List all tasks (supports filtering, search, pagination) | Open / Pre-auth | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve single task by primary key | Open / Pre-auth | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create new task | Open / Pre-auth | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update task title and/or done state | Open / Pre-auth | `200 OK` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by primary key | Open / Pre-auth | `204 No Content` / `404 Not Found` |

---

## Authentication & Authorization Examples

### 1. User Sign Up (`POST /auth/signup`)
```bash
curl.exe -i -X POST http://localhost:3000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"developer@flyrank.com","password":"SecurePassword123!"}'
```

**Response (`201 Created`)**:
```json
{
  "id": "ba593210-3ca9-4af1-9a9c-ecc328e4796a",
  "email": "developer@flyrank.com",
  "created_at": "2026-09-06T12:00:00.000000Z",
  "app_metadata": { "provider": "email", "providers": ["email"] }
}
```

If email or password is omitted:
```json
// HTTP 400 Bad Request
{"error": "Email and password are required"}
```

---

### 2. User Log In (`POST /auth/login`)
```bash
curl.exe -i -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"developer@flyrank.com","password":"SecurePassword123!"}'
```

**Response (`200 OK`)**:
```json
{
  "access_token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "xk67cu5vybss...",
  "token_type": "bearer",
  "user": {
    "id": "ba593210-3ca9-4af1-9a9c-ecc328e4796a",
    "email": "developer@flyrank.com"
  }
}
```

If incorrect credentials are submitted:
```json
// HTTP 401 Unauthorized
{"error": "Invalid login credentials"}
```

---

### 3. Accessing Protected Profile (`GET /protected/profile`)
Send the received JWT in the `Authorization` header:

```bash
curl.exe -i http://localhost:3000/protected/profile \
  -H "Authorization: Bearer <VALID_ACCESS_TOKEN>"
```

**Response (`200 OK`)**:
```json
{
  "id": "ba593210-3ca9-4af1-9a9c-ecc328e4796a",
  "email": "developer@flyrank.com",
  "created_at": "2026-09-06T12:00:00.000000Z",
  "user_metadata": { "email": "developer@flyrank.com" }
}
```

If the authorization header is missing:
```json
// HTTP 401 Unauthorized
{"error": "Access token required"}
```

If the token is tampered with or expired:
```json
// HTTP 401 Unauthorized
{"error": "Invalid or expired token"}
```

---

### 4. Protected Checkpoint (`GET /protected/dashboard`)
Demonstrates auth dependency reuse with zero duplicated security logic:

```bash
curl.exe -i http://localhost:3000/protected/dashboard \
  -H "Authorization: Bearer <VALID_ACCESS_TOKEN>"
```

**Response (`200 OK`)**:
```json
{
  "message": "Welcome to the dashboard, developer@flyrank.com!",
  "user_id": "ba593210-3ca9-4af1-9a9c-ecc328e4796a"
}
```

---

### 5. User Log Out (`POST /auth/logout`)
Terminates the user session in Supabase Auth:

```bash
curl.exe -i -X POST http://localhost:3000/auth/logout \
  -H "Authorization: Bearer <VALID_ACCESS_TOKEN>"
```

**Response (`204 No Content`)**:
```http
HTTP/1.1 204 No Content
```

*(Any subsequent requests using this access token will immediately receive `401 Unauthorized: Invalid or expired token` because the session has been revoked).*

---

## Task API (PostgreSQL CRUD) Examples

### Create Task (`POST /tasks`)
```bash
curl.exe -i -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Ship Week 4 Authentication"}'
```
**Response (`201 Created`)**:
```json
{"id":4,"title":"Ship Week 4 Authentication","done":false}
```

### List Tasks with Filtering & Search (`GET /tasks`)
Query parameters can be combined:
```bash
curl.exe -i "http://localhost:3000/tasks?done=false&search=Authentication&limit=5&offset=0"
```
**Response (`200 OK`)**:
```json
[
  {"id":4,"title":"Ship Week 4 Authentication","done":false}
]
```

### Supported Query Parameters:
| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `done` | Boolean | Filter tasks by completion status | `/tasks?done=true` |
| `search` | String | Case-insensitive title substring search | `/tasks?search=ship` |
| `limit` | Integer | Pagination: maximum number of records to return | `/tasks?limit=10` |
| `offset` | Integer | Pagination: number of records to skip | `/tasks?offset=5` |

---

## Project Structure

```text
Week 4 - A1 Auth Login & Protect/
├── Dockerfile                         # API container build instructions (Python 3.12-slim)
├── compose.yaml                       # Multi-container orchestration (api + db)
├── .dockerignore                      # Docker context build exclusions
├── .gitignore                         # Local repository secret exclusions (.env, pycache)
├── .env.example                       # Safe environment configuration template
├── requirements.txt                   # Project dependencies (FastAPI, Supabase, psycopg)
├── supabase_client.py                 # Shared, singleton Supabase client
├── database.py                        # PostgreSQL connection pool, init_db, and seed tasks
├── dependencies.py                    # Reusable auth dependency (get_current_user) & HTTPBearer
├── schemas.py                         # Pydantic data schemas (UserAuth, TaskCreate, TaskUpdate)
├── main.py                            # FastAPI application entrypoint & exception handlers
├── Swagger UI- Authorize & Routes.jpeg# Verified Swagger documentation screenshot
├── README.md                          # Production manual and specification
└── routers/
    ├── auth.py                        # Authentication APIRouter (signup, login, logout)
    └── tasks.py                       # Task CRUD APIRouter (PostgreSQL queries)
```

---

## PostgreSQL Persistence & Database Architecture

The persistence layer uses a dedicated PostgreSQL 16 service:

- **Automatic Schema Migration**: Upon container initialization, `database.py` issues `CREATE TABLE IF NOT EXISTS tasks (...)` to establish the schema.
- **Automatic Seeding**: If the `tasks` table is empty on first boot, it seeds default demonstration tasks.
- **Docker Volume**: Data is mounted to `taskdata_w4:/var/lib/postgresql/data`, ensuring data survives container restarts and image rebuilds.

### Inspecting the Database via Container Shell:
```bash
docker exec -it week4-a1authloginprotect-db-1 psql -U postgres -d tasks
```
Common inspection SQL commands:
```sql
\dt
SELECT * FROM tasks;
```

---

## Stage-by-Stage Implementation Roadmap

- [x] **Stage 0: Setup Server and Supabase Client** (`fd13f64`): Multi-container Docker setup, startup connection verification.
- [x] **Stage 1: User Registration & Authentication** (`51e4677`): `POST /auth/signup` and `POST /auth/login` with 400/401 validation.
- [x] **Stage 2: Public Route and Unverified Protected Route** (`8d2cae9`): `GET /public/info` (200) and `GET /protected/profile` header gatekeeper (401).
- [x] **Stage 3: Profile Route Token Verification** (`cd94a41`): Cryptographic JWT verification with `supabase.auth.get_user(token)`.
- [x] **Stage 4: Middleware Protection & Logout** (`c643ee4`): Reusable `get_current_user` dependency, `POST /auth/logout` (204), and `/protected/dashboard` checkpoint.
- [x] **Stage 5: Swagger UI - Visualizing the Secure Doors** (`880c452`): `HTTPBearer` scheme integration, locked door icons, and Schemas model display.
- [x] **Stage 6: Publish to GitHub & Production Documentation**: Clean environment safety, comprehensive documentation, and repository synchronization.
