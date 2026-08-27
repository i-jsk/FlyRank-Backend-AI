# W3 · A2 — Containerizing Stack 🐳

Welcome to **Week 3 - Assignment 2** of the FlyRank Backend AI Internship!

---

## 🎯 Purpose & Goal

Transition from SQLite file storage to a production-grade **PostgreSQL** database running inside a **Docker container**.
- Manage database configuration via `.env`.
- Ensure data survives restarts using a Docker named volume (`taskdata`).
- Eventually run both the application and database together via Docker Compose.

---

## 🛠️ Technology Stack (Python Lane)

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ (3.12) | Modern typed Python |
| **Framework** | FastAPI | High-performance Python web framework |
| **Database** | PostgreSQL 16 | Containerized relational database |
| **Database Driver** | `psycopg` (v3) / `psycopg2-binary` | PostgreSQL database adapter |
| **Configuration** | `python-dotenv` | Loads `.env` configuration securely |
| **Container Engine** | Docker Desktop / Podman | Container runtime and volume manager |
| **Orchestration** | Docker Compose | Multi-container orchestration (`compose.yaml`) |

---

## 🚀 Stage 0: Run PostgreSQL in Docker

### 1. Launch PostgreSQL Container in One Command
```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres
```

#### 🔍 Command Breakdown:
- `--name taskdb`: Names the running container `taskdb`.
- `-e POSTGRES_PASSWORD=dev`: Sets the database password to `dev`.
- `-e POSTGRES_DB=tasks`: Automatically creates a database called `tasks`.
- `-p 5432:5432`: Maps port `5432` from inside the container to `localhost:5432` on your machine.
- `-v taskdata:/var/lib/postgresql/data`: Attaches a persistent named volume `taskdata` so rows survive container restarts.
- `-d postgres`: Downloads and runs the official `postgres` image in the background (detached mode).

---

### 2. Verify Running Container & Open `psql`

1. **Check container status**:
   ```bash
   docker ps
   ```
   *(You will see `taskdb` with status `Up` on port `0.0.0.0:5432->5432/tcp`).*

2. **Open interactive `psql` terminal inside container**:
   ```bash
   docker exec -it taskdb psql -U postgres -d tasks
   ```

3. **Check tables and exit**:
   - Type `\dt` (Displays relation list: *Did not find any relations*).
   - Type `\q` (Exits the psql prompt).

---

## 🚦 Stage Progress Roadmap

- [x] **Stage 0: Postgres in Docker + gitignore** — Launch PostgreSQL container with persistent volume, configure `.env.example` & `.gitignore`.
- [ ] **Stage 1: Connect App to Postgres** — Switch database layer to PostgreSQL via `.env` configuration.
- [ ] **Stage 2: Full CRUD on Postgres** — Verify all CRUD endpoints against PostgreSQL.
- [ ] **Stage 3: Containerize Application** — Create `Dockerfile` and build app image.
- [ ] **Stage 4: Docker Compose Stack** — Start app + Postgres with one `docker compose up` command.
- [ ] **Stage 5: Final Documentation & Verification**.
