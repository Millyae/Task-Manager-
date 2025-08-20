from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID

def get_task(db: Session, task_uuid: UUID):
    return db.query(models.Task).filter(models.Task.uuid == task_uuid).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_uuid: UUID, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_uuid)
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_uuid: UUID):
    db_task = get_task(db, task_uuid)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task