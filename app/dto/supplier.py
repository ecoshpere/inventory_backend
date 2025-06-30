from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SupplierBase(BaseModel):
    name: str
    code: str
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

class SupplierResponse(SupplierBase):
    id: str
    
    class Config:
        from_attributes = True 