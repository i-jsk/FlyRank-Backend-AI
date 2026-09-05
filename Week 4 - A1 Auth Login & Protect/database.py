from contextlib import contextmanager
import os
from pathlib import Path
import time
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

# Load environment variables from .env file in the current assignment directory
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Retrieve DATABASE_URL with fallback for local docker postgres
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:dev@localhost:5432/tasks"
)

# Normalize postgres:// to postgresql:// if needed (compatibility with various container/cloud providers)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


@contextmanager
def get_db_connection():
    """Context manager for managing PostgreSQL connections cleanly.

    Ensures connections are properly closed after operations and rows are returned as dict-like mappings.
    """
    conn = psycopg.connect(DATABASE_URL, connect_timeout=2, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def init_db(max_retries: int = 10, retry_delay: float = 1.5):
    """Initialize PostgreSQL database schema and seed 3 initial tasks if table is empty.

    Includes retry logic to handle container startup latency in Docker Compose environments.
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Create tasks table if it doesn't already exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            done BOOLEAN NOT NULL DEFAULT FALSE
                        );
                    """)

                    # Check if table is empty
                    cursor.execute("SELECT COUNT(*) AS count FROM tasks;")
                    row = cursor.fetchone()
                    count = row["count"] if row else 0

                    # Insert 3 example tasks ONLY if table is empty
                    if count == 0:
                        seed_tasks = [
                            ("Setup FastAPI project", True),
                            ("Build Stage 2 read endpoints", False),
                            ("Publish to GitHub", False),
                        ]
                        cursor.executemany(
                            "INSERT INTO tasks (title, done) VALUES (%s, %s);",
                            seed_tasks,
                        )
                        conn.commit()
            return
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                raise last_error
