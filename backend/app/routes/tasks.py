from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, auth

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/project/{project_id}", response_model=List[schemas.TaskOut])
def get_tasks(project_id: int, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

@router.post("/project/{project_id}", response_model=schemas.TaskOut)
def create_task(project_id: int, task: schemas.TaskBase, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    new_task = models.Task(**task.dict(), project_id=project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskBase, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id, models.Project.user_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id, models.Project.user_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
