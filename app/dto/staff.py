from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class StaffBase(BaseModel):
    status: str
    title: str
    firstname: str
    middlename: Optional[str] = None
    lastname: str
    mobile_number: str
    email_address: str
    address: str
    gender: str
    date_of_birth: str
    employee_number: str
    designation: str
    date_employed: str
    department_id: str

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    firstname: Optional[str] = None
    middlename: Optional[str] = None
    lastname: Optional[str] = None
    mobile_number: Optional[str] = None
    email_address: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    employee_number: Optional[str] = None
    designation: Optional[str] = None
    date_employed: Optional[str] = None
    department_id: Optional[str] = None

class StaffResponse(StaffBase):
    id: str
    department_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
