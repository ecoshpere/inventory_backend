from sqlalchemy import Column, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Service(Base):
    __tablename__ = "services"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    image_thumbnail = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Active")
    barcode = Column(String, nullable=True, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category", backref="services")
    department = relationship("Department", backref="services")
