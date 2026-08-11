from contextlib import contextmanager
from pathlib import Path
import sqlite3

# SQLite database file path definition
DB_PATH = Path(__file__).parent / "tasks.db"


@contextmanager
def get_db_connection():
    """Context manager for managing SQLite database connections cleanly.

    Ensures connections are properly closed after operations, preventing database file locks.
    """
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dictionary-like Row objects for easy column access
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the SQLite database schema and seed 3 initial tasks if the table is empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Create tasks table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)

        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]

        # Insert 3 example tasks ONLY if table is empty
        if count == 0:
            seed_tasks = [
                ("Setup FastAPI project", True),
                ("Build Stage 2 read endpoints", False),
                ("Publish to GitHub", False),
            ]
            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)", seed_tasks
            )
            conn.commit()
