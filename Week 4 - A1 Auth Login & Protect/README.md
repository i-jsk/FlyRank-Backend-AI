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

## Stage 1 Verification (Open Auth: Sign Up & Log In)

Stage 1 implements user registration (`POST /auth/signup`) and authentication (`POST /auth/login`) via Supabase Auth IdP.

> [!TIP]
> **One-Time Supabase Setting**: In your Supabase Dashboard under **Authentication → Providers → Email**, turn **Confirm email** off so new users can log in immediately after registration without waiting for verification emails.

### 1. User Sign Up (`POST /auth/signup`)
```bash
curl.exe -i -X POST http://localhost:3000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```
**Response (`201 Created`)**:
Returns the created user object from Supabase (containing user `id`, `email`, `created_at`, etc.).

### 2. Validation Checks (`400 Bad Request`)
If `email` or `password` is missing, empty, or whitespace, the server rejects the request:
```bash
curl.exe -i -X POST http://localhost:3000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```
**Response (`400 Bad Request`)**:
```json
{"error":"Email and password are required"}
```

### 3. User Log In (`POST /auth/login`)
```bash
curl.exe -i -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```
**Response (`200 OK`)**:
Returns session credentials including the cryptographic `access_token` (JWT) and `refresh_token`:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "...",
  "token_type": "bearer",
  "user": { "id": "...", "email": "test@example.com" }
}
```

### 4. Invalid Credentials Handling (`401 Unauthorized`)
If an invalid email or password is provided:
```bash
curl.exe -i -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"wrong@example.com","password":"wrongpassword"}'
```
**Response (`401 Unauthorized`)**:
```json
{"error":"Invalid login credentials"}
```

---

## Stage 2 Verification (The Public & Protected Gates)

Stage 2 introduces public access alongside header-based gatekeeping for protected routes.

### 1. Public Info Gate (`GET /public/info`)
Accessible by any client without authentication credentials:
```bash
curl.exe -i http://localhost:3000/public/info
```
**Response (`200 OK`)**:
```json
{"message":"Welcome stranger! This info is public."}
```

### 2. Protected Gate Without Token (`GET /protected/profile`)
Clients attempting to access the protected profile without a valid `Authorization: Bearer <token>` header are rejected immediately:
```bash
curl.exe -i http://localhost:3000/protected/profile
```
**Response (`401 Unauthorized`)**:
```json
{"error":"Access token required"}
```

### 3. Protected Gate With Token (Stage 2 Unverified Gate)
When an `Authorization: Bearer <token>` header was provided without verification:
```bash
curl.exe -i http://localhost:3000/protected/profile \
  -H "Authorization: Bearer <token>"
```
**Response (`200 OK`)**:
```json
{"message":"Access token received (unverified)","token":"<token>"}
```

---

## Stage 3 Verification (The Guard: Token Verification)

Stage 3 upgrades `GET /protected/profile` to cryptographically verify the incoming JWT with Supabase using `supabase.auth.get_user(token)`.

### 1. Verified Profile Access with Valid JWT (`200 OK`)
Log in via `POST /auth/login` to retrieve your fresh `access_token`, then pass it in the `Authorization` header:

```bash
curl.exe -i http://localhost:3000/protected/profile \
  -H "Authorization: Bearer <VALID_ACCESS_TOKEN>"
```

**Response (`200 OK`)**:
Returns the authenticated user's secure metadata (ID, email, creation timestamp):
```json
{
  "id": "ba593210-3ca9-4af1-9a9c-ecc328e4796a",
  "email": "checkpoint_user@flyrank.com",
  "created_at": "2026-09-05T21:03:41.155551Z",
  "app_metadata": { "provider": "email", "providers": ["email"] },
  "user_metadata": { "email": "checkpoint_user@flyrank.com" }
}
```

### 2. Tampered or Invalid Token Rejection (`401 Unauthorized`)
If the token is modified by even a single character, expired, or malformed:

```bash
curl.exe -i http://localhost:3000/protected/profile \
  -H "Authorization: Bearer <TAMPERED_OR_INVALID_TOKEN>"
```

**Response (`401 Unauthorized`)**:
```json
{"error":"Invalid or expired token"}
```

### 3. Interactive Browser Testing via Swagger UI
You can also verify the entire flow interactively in the browser at `http://localhost:3000/docs`:
1. Execute `POST /auth/login` to obtain your `access_token`.
2. Click the green **Authorize** button (with the lock icon 🔓) at the top right of the Swagger UI page.
3. Paste your `access_token` into the **Value** field and click **Authorize**, then click **Close**.
4. Expand `GET /protected/profile`, click **Try it out**, and click **Execute**.
5. The request returns `200 OK` with your profile data.

---

## Stage 4 Verification (Middleware Protection & Logout)

Stage 4 extracts authentication validation into a reusable dependency (`get_current_user` in `dependencies.py`), implements `POST /auth/logout`, and adds a second protected route `GET /protected/dashboard` to prove guard reuse with zero duplicate auth code.

### 1. Second Protected Route Checkpoint (`GET /protected/dashboard`)
Proves reusable dependency guard on a new route:

```bash
# Valid Token -> 200 OK
curl.exe -i http://localhost:3000/protected/dashboard \
  -H "Authorization: Bearer <VALID_ACCESS_TOKEN>"
```

**Response (`200 OK`)**:
```json
{
  "message": "Welcome to the dashboard, checkpoint_user@flyrank.com!",
  "user_id": "ba593210-3ca9-4af1-9a9c-ecc328e4796a"
}
```

```bash
# Bad or Tampered Token -> 401 Unauthorized
curl.exe -i http://localhost:3000/protected/dashboard \
  -H "Authorization: Bearer bad_token_xyz"
```

**Response (`401 Unauthorized`)**:
```json
{"error":"Invalid or expired token"}
```

### 2. User Log Out (`POST /auth/logout`)
Terminates the user's session in Supabase Auth. Requires valid authorization and returns `204 No Content`:

```bash
curl.exe -i -X POST http://localhost:3000/auth/logout \
  -H "Authorization: Bearer <VALID_ACCESS_TOKEN>"
```

**Response (`204 No Content`)**:
```http
HTTP/1.1 204 No Content
date: ...
server: uvicorn
```

*(Subsequent requests using this logged-out token will be rejected with `401 Unauthorized: Invalid or expired token`).*

---

## Stage 5 Verification (See it: Swagger UI - Visualizing the Secure Doors)

FastAPI automatically serves interactive API documentation at `http://localhost:3000/docs`. The OpenAPI specification is configured with the `HTTPBearer` security scheme in `dependencies.py` and mapped across all protected routes (`/protected/profile`, `/protected/dashboard`, `/auth/logout`).

### 1. Swagger UI Interface & Authorize Padlock
Protected endpoints feature a dedicated padlock icon on the route bar. The global **Authorize** button allows pasting the JWT access token once to unlock all guarded endpoints for testing:

![Swagger UI Authorize and Routes](Swagger%20UI-%20Authorize%20%26%20Routes.jpeg)

---

## API Endpoints Matrix

| Operation | HTTP Method | Path | Access Level | Status | Description |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **Root Metadata** | `GET` | `/` | Public | Completed | System status and available endpoints |
| **Health Monitor** | `GET` | `/health` | Public | Completed | Server uptime and status |
| **Public Info Gate** | `GET` | `/public/info` | Public | Completed | Unprotected public information |
| **User Profile** | `GET` | `/protected/profile` | Protected | Completed | Verified profile data via reusable dependency |
| **Dashboard Checkpoint** | `GET` | `/protected/dashboard` | Protected | Completed | Second protected route proving dependency reuse |
| **User Sign Up** | `POST` | `/auth/signup` | Public | Completed | Creates new user account in Supabase |
| **User Log In** | `POST` | `/auth/login` | Public | Completed | Authenticates user and returns JWT |
| **User Log Out** | `POST` | `/auth/logout` | Protected | Completed | Terminates user session (returns 204) |
| **List Tasks** | `GET` | `/tasks` | Open / Pre-auth | Completed | Retrieves tasks from PostgreSQL database |
| **Get Task by ID** | `GET` | `/tasks/{id}` | Open / Pre-auth | Completed | Retrieves single task by primary key |
| **Create Task** | `POST` | `/tasks` | Open / Pre-auth | Completed | Inserts new task into database |
| **Update Task** | `PUT` | `/tasks/{id}` | Open / Pre-auth | Completed | Updates task title or done state |
| **Delete Task** | `DELETE` | `/tasks/{id}` | Open / Pre-auth | Completed | Deletes task row from database |



