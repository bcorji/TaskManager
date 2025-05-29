from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.models import TaskPriority, TaskStatus

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    theme_preference: Optional[str] = None
    notifications_enabled: Optional[bool] = None

class UserProfile(BaseModel):
    id: int
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    theme_preference: str
    notifications_enabled: bool
    model_config = {
        "from_attributes": True
    }

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    is_active: bool
    profile: Optional[UserProfile] = None
    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class CategoryBase(BaseModel):
    name: str
    color: Optional[str] = "#808080"

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class TaskCommentBase(BaseModel):
    content: str

class TaskCommentCreate(TaskCommentBase):
    pass

class TaskCommentOut(TaskCommentBase):
    id: int
    created_at: datetime
    user_id: int
    model_config = {
        "from_attributes": True
    }

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.PENDING
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: int
    category_ids: Optional[List[int]] = None

class TaskUpdate(TaskBase):
    category_ids: Optional[List[int]] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime]
    project_id: int
    categories: List[CategoryOut]
    comments: List[TaskCommentOut]
    model_config = {
        "from_attributes": True
    }
