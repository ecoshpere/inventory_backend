from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DepartmentBase(BaseModel):
    name: str
    function: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    function: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
