from pydantic import BaseModel
from uuid import UUID
from .models import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.CREATED

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

class Task(TaskBase):
    uuid: UUID

    class Config:
        from_attributes = True