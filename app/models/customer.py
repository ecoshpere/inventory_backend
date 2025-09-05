from sqlalchemy import Column, String, Text, DateTime, func, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum

class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=True)
    first_name = Column(String, nullable=False, index=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=True, index=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    address = Column(Text, nullable=True)
    state_region = Column(String, nullable=True)
    country = Column(String, nullable=True)
    mobile_number = Column(String, nullable=True, index=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    website = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
