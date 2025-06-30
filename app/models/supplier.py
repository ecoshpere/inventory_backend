from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    contact_person = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
    stock_receipts = relationship("StockReceipt", back_populates="supplier") 