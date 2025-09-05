from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False, default="Enabled")
    title = Column(String, nullable=False)
    firstname = Column(String, nullable=False, index=True)
    middlename = Column(String, nullable=True)
    lastname = Column(String, nullable=False, index=True)
    mobile_number = Column(String, nullable=False)
    email_address = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    employee_number = Column(String, nullable=False, unique=True, index=True)
    designation = Column(String, nullable=False)
    date_employed = Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to Department
    department = relationship("Department", backref="staff")
