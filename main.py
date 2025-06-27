from fastapi import FastAPI
from models import Task, TaskCreate, TaskUpdate
from database import engine, init_db
from sqlmodel import Session, select

app = FastAPI()

# Initialize DB
init_db()

# Create Task
@app.post("/api/tasks/create")
def create_task(task: TaskCreate):
    with Session(engine) as session:
        db_task = Task(**task.dict())
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return {"message": "Task created successfully!", "task_id": db_task.id}

# Update Task Status
@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task:
            return {"error": "Task not found"}
        db_task.status = task.status
        session.commit()
        return {"message": "Task updated successfully!"}

# Get Task Summary by Assignee Name
@app.get("/api/tasks/summary/{assignee}")
def get_summary(assignee: str):
    with Session(engine) as session:
        statement = select(Task).where(Task.assignee == assignee)
        results = session.exec(statement).all()
        completed = sum(1 for task in results if task.status == "completed")
        pending = sum(1 for task in results if task.status == "pending")
        return {
            "assignee": assignee,
            "completed": completed,
            "pending": pending
        }


