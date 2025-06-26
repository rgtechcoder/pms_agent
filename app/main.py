from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Task
from database import engine, init_db

app = FastAPI()
init_db()

@app.post("/api/tasks/create")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"message": "Task created successfully!", "task_id": task.id}

@app.post("/api/tasks/update-status")
def update_status(task_id: int, status: str):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.status = status
        session.add(task)
        session.commit()
        return {"message": "Status updated successfully", "task": task}

