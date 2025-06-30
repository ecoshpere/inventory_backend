from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="category") 