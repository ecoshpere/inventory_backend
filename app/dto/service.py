from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: str
    department_id: str
    image_thumbnail: Optional[str] = None
    status: str = "Active"
    barcode: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[str] = None
    department_id: Optional[str] = None
    image_thumbnail: Optional[str] = None
    status: Optional[str] = None
    barcode: Optional[str] = None

class ServiceResponse(ServiceBase):
    id: str
    category_name: Optional[str] = None
    department_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
