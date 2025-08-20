from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="CRUD API для управления задачами",
    version="1.0.0"
)

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_uuid}", response_model=schemas.Task)
def read_task(task_uuid: UUID, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_uuid=task_uuid)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_uuid}", response_model=schemas.Task)
def update_task(task_uuid: UUID, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_uuid=task_uuid, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_uuid}", response_model=schemas.Task)
def delete_task(task_uuid: UUID, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_uuid=task_uuid)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/")
def read_root():
    return {"message": "Task Manager API"}