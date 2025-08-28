from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas import BaseSchema

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase, BaseSchema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]