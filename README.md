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
- [ ] **Stage 1: Read endpoints** — List all tasks (`GET /tasks`) & get single task (`GET /tasks/{id}`).
- [ ] **Stage 2: Create endpoint** — Add new task (`POST /tasks`).
- [ ] **Stage 3: Update endpoint** — Modify existing task (`PUT /tasks/{id}`).
- [ ] **Stage 4: Delete endpoint** — Remove task (`DELETE /tasks/{id}`).
- [ ] **Stage 5: Final Polish & Swagger UI Verification**.

---

## 💻 Quick Start & Running Locally

### 1. Set Up Virtual Environment

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API Server

```bash
python main.py
# Or directly via Uvicorn:
uvicorn main:app --reload --port 8000
```

### 4. Verify API Endpoints

- **Browser / Curl**:
  ```bash
  curl -i http://127.0.0.1:8000/
  ```
  Expected output:
  `HTTP/1.1 200 OK`
  `{"message":"Hello, server!","status":"online"}`

- **Swagger UI Interactive Docs**:
  Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.