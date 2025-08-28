from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from models import UserRole, TaskStatus, TaskPriority

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Organization schemas
class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase, BaseSchema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.MEMBER

class UserCreate(UserBase):
    password: str
    organization_id: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase, BaseSchema):
    id: int
    is_active: bool
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime]

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase, BaseSchema):
    id: int
    organization_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectMemberAdd(BaseModel):
    user_id: int

class ProjectMemberResponse(BaseSchema):
    id: int
    user_id: int
    user: UserResponse
    joined_at: datetime

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date must be today or in the future')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date must be today or in the future')
        return v

class TaskResponse(TaskBase, BaseSchema):
    id: int
    status: TaskStatus
    project_id: int
    assignee_id: Optional[int]
    creator_id: int
    assignee: Optional[UserResponse]
    creator: UserResponse
    created_at: datetime
    updated_at: Optional[datetime]

class TaskListFilter(BaseModel):
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
    priority: Optional[TaskPriority] = None
    overdue_only: Optional[bool] = False

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase, BaseSchema):
    id: int
    task_id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: Optional[datetime]

# Attachment schemas
class AttachmentResponse(BaseSchema):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    task_id: int
    uploaded_by: int
    uploader: UserResponse
    uploaded_at: datetime

# Notification schemas
class NotificationResponse(BaseSchema):
    id: int
    message: str
    type: str
    is_read: bool
    task_id: Optional[int]
    created_at: datetime

class NotificationMarkRead(BaseModel):
    notification_ids: List[int]

# Report schemas
class TaskCountByStatus(BaseModel):
    status: TaskStatus
    count: int

class ProjectReport(BaseModel):
    project_id: int
    project_name: str
    task_counts: List[TaskCountByStatus]
    total_tasks: int

class OverdueTaskResponse(BaseModel):
    task: TaskResponse
    days_overdue: int