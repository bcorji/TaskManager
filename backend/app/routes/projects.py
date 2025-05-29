from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from typing import List
from datetime import datetime

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[schemas.ProjectOut])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    return (
        db.query(models.Project)
        .filter(models.Project.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.post("/", response_model=schemas.ProjectOut)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_project = models.Project(
        **project.model_dump(),
        user_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    project_update: schemas.ProjectCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project_update.model_dump().items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None

@router.get("/{project_id}/tasks", response_model=List[schemas.TaskOut])
def get_project_tasks(
    project_id: int,
    status: models.TaskStatus = None,
    priority: models.TaskPriority = None,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    query = db.query(models.Task).filter(models.Task.project_id == project_id)
    
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    
    return query.all()
