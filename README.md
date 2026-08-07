# FlyRank To-Do CRUD API 🚀

Welcome to the **FlyRank To-Do CRUD API** repository! This repository contains a backend RESTful API built with **Python 3.12** and **FastAPI** as part of the FlyRank Backend AI Internship program.

---

## 🎯 Purpose & Goals

CRUD (Create, Read, Update, Delete) is the fundamental pattern for almost every backend service in software engineering:
- Social networks CRUD posts & comments.
- E-commerce platforms CRUD products & orders.
- **FlyRank** CRUDs SEO reports & AI insights.

This project builds an in-memory To-Do list API stage-by-stage to master core backend concepts: REST principles, endpoint routing, HTTP status codes, request validation, and interactive documentation via Swagger UI.

---

## 🛠️ Technology Stack (Python Lane)

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ (3.12) | Modern, strongly-typed Python |
| **Framework** | FastAPI | High-performance Python web framework |
| **ASGI Server** | Uvicorn | Async server implementation running FastAPI |
| **API Docs** | Swagger UI (`/docs`) | Built-in interactive documentation |
| **HTTP Client** | `curl` / Browser / HTTPX | Testing and verification tools |

---

## 🚦 Stages & Roadmap

- [x] **Stage 0: Hello, server** — Server startup (`GET /` returning 200 OK & message).
- [x] **Stage 1: Root and health endpoints** — API metadata (`GET /`) & health monitor (`GET /health`).
- [x] **Stage 2: Read endpoints** — List all tasks (`GET /tasks`) & single task (`GET /tasks/{id}`) with 404 error handling.
- [ ] **Stage 3: Create endpoint** — Add new task (`POST /tasks`).
- [ ] **Stage 4: Update endpoint** — Modify existing task (`PUT /tasks/{id}`).
- [ ] **Stage 5: Delete endpoint** — Remove task (`DELETE /tasks/{id}`).

---

## 💻 Quick Start & Running Locally

### 1. Run the API Server

```bash
python main.py
# Or directly via Uvicorn:
uvicorn main:app --reload --port 8000
```

### 2. Verify API Endpoints

- **List All Tasks**:
  ```bash
  curl -i http://127.0.0.1:8000/tasks
  ```
  *Response*: `200 OK` with JSON array of 3 tasks.

- **Get Single Task (Existing)**:
  ```bash
  curl -i http://127.0.0.1:8000/tasks/1
  ```
  *Response*: `200 OK` with `{"id": 1, "title": "Setup FastAPI project", "done": true}`

- **Get Single Task (Non-Existent)**:
  ```bash
  curl -i http://127.0.0.1:8000/tasks/99
  ```
  *Response*: `404 Not Found` with `{"error": "Task 99 not found"}`

- **Swagger UI Interactive Docs**:
  Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.