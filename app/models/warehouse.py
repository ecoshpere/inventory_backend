from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    address = Column(Text, nullable=False)
    contact_person = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Relationships
    stock_receipts = relationship("StockReceipt", back_populates="warehouse")
    purchase_orders = relationship("PurchaseOrder", back_populates="warehouse")
    stock_inventory = relationship("Inventory", back_populates="warehouse")
    outgoing_movements = relationship("StockMovement", foreign_keys="StockMovement.source_warehouse_id", back_populates="source_warehouse")
    incoming_movements = relationship("StockMovement", foreign_keys="StockMovement.destination_warehouse_id", back_populates="destination_warehouse") 