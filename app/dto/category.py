from pydantic import BaseModel, Field
from typing import Optional
import uuid

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True 