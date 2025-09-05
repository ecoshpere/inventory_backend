from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, date
from app.models.customer import GenderEnum

class CustomerBase(BaseModel):
    title: Optional[str] = None
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    company_name: Optional[str] = Field(None, max_length=200)
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    state_region: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    mobile_number: Optional[str] = Field(None, max_length=20)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=200)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    title: Optional[str] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    company_name: Optional[str] = Field(None, max_length=200)
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    state_region: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    mobile_number: Optional[str] = Field(None, max_length=20)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=200)

class CustomerResponse(CustomerBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
