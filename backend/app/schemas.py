from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectBase(BaseModel):
    title: str

class ProjectOut(ProjectBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class TaskBase(BaseModel):
    title: str
    status: Optional[str] = "Pending"
    due_date: Optional[datetime] = None

class TaskOut(TaskBase):
    id: int
    model_config = {
        "from_attributes": True
    }
