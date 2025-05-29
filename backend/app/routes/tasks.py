from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from typing import List
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(
    status: models.TaskStatus = None,
    priority: models.TaskPriority = None,
    category_id: int = None,
    due_before: datetime = None,
    search: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = (
        db.query(models.Task)
        .join(models.Project)
        .filter(models.Project.user_id == current_user.id)
    )
    
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if category_id:
        query = query.join(models.Task.categories).filter(models.Category.id == category_id)
    if due_before:
        query = query.filter(models.Task.due_date <= due_before)
    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify project belongs to user
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == task.project_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create task
    new_task = models.Task(**task.model_dump(exclude={'category_ids'}))
    
    # Add categories if provided
    if task.category_ids:
        categories = (
            db.query(models.Category)
            .filter(models.Category.id.in_(task.category_ids))
            .all()
        )
        new_task.categories = categories

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = (
        db.query(models.Task)
        .join(models.Project)
        .filter(
            models.Task.id == task_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = (
        db.query(models.Task)
        .join(models.Project)
        .filter(
            models.Task.id == task_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update basic fields
    update_data = task_update.model_dump(exclude={'category_ids'})
    for key, value in update_data.items():
        setattr(task, key, value)

    # Update categories if provided
    if task_update.category_ids is not None:
        categories = (
            db.query(models.Category)
            .filter(models.Category.id.in_(task_update.category_ids))
            .all()
        )
        task.categories = categories

    # Set completed_at if status changed to completed
    if task_update.status == models.TaskStatus.COMPLETED and task.status != models.TaskStatus.COMPLETED:
        task.completed_at = datetime.utcnow()
    elif task_update.status != models.TaskStatus.COMPLETED:
        task.completed_at = None

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = (
        db.query(models.Task)
        .join(models.Project)
        .filter(
            models.Task.id == task_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None

@router.post("/{task_id}/comments", response_model=schemas.TaskCommentOut)
def create_task_comment(
    task_id: int,
    comment: schemas.TaskCommentCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = (
        db.query(models.Task)
        .join(models.Project)
        .filter(
            models.Task.id == task_id,
            models.Project.user_id == current_user.id
        )
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_comment = models.TaskComment(
        **comment.model_dump(),
        task_id=task_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
