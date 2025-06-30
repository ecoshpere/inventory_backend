from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid

class WarehouseBase(BaseModel):
    name: str
    code: str
    address: str
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    is_active: bool = True
    is_default: bool = False

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None

class WarehouseResponse(WarehouseBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True 