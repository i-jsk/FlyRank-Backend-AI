from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from database import get_db_connection
from schemas import TaskCreate, TaskUpdate

# Create router for /tasks resources
router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=200, summary="List All Tasks")
@router.get("/", status_code=200, include_in_schema=False)
def get_all_tasks():
    """Retrieve the complete list of tasks from PostgreSQL database."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks ORDER BY id ASC;"
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "title": row["title"],
                    "done": bool(row["done"]),
                }
                for row in rows
            ]


@router.get("/{id}", summary="Get Single Task by ID")
def get_task_by_id(id: int):
    """Retrieve a single task by ID from PostgreSQL database. Returns 404 if not found."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s;", (id,)
            )
            row = cursor.fetchone()
            if not row:
                return JSONResponse(
                    status_code=404, content={"error": f"Task {id} not found"}
                )
            return {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"]),
            }


@router.post("", status_code=201, summary="Create New Task")
@router.post("/", status_code=201, include_in_schema=False)
def create_task(task_input: TaskCreate):
    """Create a new task in PostgreSQL database.

    Returns 201 Created on success, or 400 Bad Request if title is missing/empty.
    """
    if not task_input.title or not task_input.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"},
        )

    clean_title = task_input.title.strip()
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done;",
                (clean_title,),
            )
            row = cursor.fetchone()
            conn.commit()

            return JSONResponse(
                status_code=201,
                content={
                    "id": row["id"],
                    "title": row["title"],
                    "done": bool(row["done"]),
                },
            )


@router.put("/{id}", status_code=200, summary="Update Task by ID")
def update_task(id: int, task_input: TaskUpdate):
    """Update an existing task's title and/or done status in PostgreSQL database."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s;", (id,)
            )
            row = cursor.fetchone()
            if not row:
                return JSONResponse(
                    status_code=404, content={"error": f"Task {id} not found"}
                )

            # Validation: at least one field must be supplied
            if task_input.title is None and task_input.done is None:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": (
                            "At least one field (title or done) must be"
                            " provided for update"
                        )
                    },
                )

            current_title = row["title"]
            current_done = bool(row["done"])

            if task_input.title is not None:
                if (
                    not isinstance(task_input.title, str)
                    or not task_input.title.strip()
                ):
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"},
                    )
                current_title = task_input.title.strip()

            if task_input.done is not None:
                current_done = bool(task_input.done)

            cursor.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                (current_title, current_done, id),
            )
            updated_row = cursor.fetchone()
            conn.commit()

            return {
                "id": updated_row["id"],
                "title": updated_row["title"],
                "done": bool(updated_row["done"]),
            }


@router.delete("/{id}", status_code=204, summary="Delete Task by ID")
def delete_task(id: int):
    """Delete a task by ID from PostgreSQL database.

    Returns 204 No Content on success, or 404 if not found.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM tasks WHERE id = %s;", (id,)
            )
            row = cursor.fetchone()
            if not row:
                return JSONResponse(
                    status_code=404, content={"error": f"Task {id} not found"}
                )

            cursor.execute("DELETE FROM tasks WHERE id = %s;", (id,))
            conn.commit()
            return Response(status_code=204)
