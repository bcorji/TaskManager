from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[schemas.ProjectOut])
def get_projects(db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Project).filter(models.Project.user_id == current_user.id).all()

@router.post("/", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectBase, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    new_project = models.Project(title=project.title, user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.put("/{id}", response_model=schemas.ProjectOut)
def update_project(id: int, project: schemas.ProjectBase, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    proj = db.query(models.Project).filter(models.Project.id == id, models.Project.user_id == current_user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    proj.title = project.title
    db.commit()
    return proj

@router.delete("/{id}")
def delete_project(id: int, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    proj = db.query(models.Project).filter(models.Project.id == id, models.Project.user_id == current_user.id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(proj)
    db.commit()
    return {"detail": "Deleted"}
