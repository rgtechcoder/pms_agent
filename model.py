from sqlmodel import SQLModel, Field
from typing import Optional

# ✅ Task table
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: str
    assignee: str
    status: str = "pending"

# ✅ Request Models
class TaskCreate(SQLModel):
    title: str
    description: str
    due_date: str
    assignee: str  # simplified if you're not using employee_id anymore

class TaskUpdate(SQLModel):
    status: str
