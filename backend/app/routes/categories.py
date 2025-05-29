from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Category).all()

@router.post("/", response_model=schemas.CategoryOut)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    if db.query(models.Category).filter(models.Category.name == category.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = models.Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    category_update: schemas.CategoryCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if (
        category_update.name != category.name and
        db.query(models.Category).filter(models.Category.name == category_update.name).first()
    ):
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    for key, value in category_update.model_dump().items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_user)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return None
