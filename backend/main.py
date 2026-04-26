from pathlib import Path
import sqlite3
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
DB_PATH = BASE_DIR / "tasks.db"

app = FastAPI()

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

class Task(BaseModel):
    id: int
    text: str

class CreateTask(BaseModel):
    text: str


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/tasks", response_model=List[Task])
def read_tasks() -> List[Task]:
    conn = get_connection()
    rows = conn.execute("SELECT id, text FROM tasks ORDER BY id").fetchall()
    tasks = [Task(id=row["id"], text=row["text"]) for row in rows]
    conn.close()
    return tasks


@app.post("/tasks", response_model=Task)
def create_task(task: CreateTask) -> Task:
    if not task.text.strip():
        raise HTTPException(status_code=400, detail="Task text cannot be empty")
    conn = get_connection()
    cursor = conn.execute("INSERT INTO tasks (text) VALUES (?)", (task.text.strip(),))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return Task(id=task_id, text=task.text.strip())


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = None
    try:
        conn = get_connection()
        # Check if task exists before deletion
        cursor = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Delete the task
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        return {"message": "Task deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if conn:
            conn.close()


@app.get("/")
def serve_index(request: Request):
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)
