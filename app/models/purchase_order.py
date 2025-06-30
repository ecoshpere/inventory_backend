from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    po_number = Column(String, unique=True, nullable=False)
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=False)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expected_delivery_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="Draft")  # Draft, Submitted, Approved, Received, Cancelled
    total_amount = Column(Float, nullable=False, default=0.0)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    warehouse = relationship("Warehouse", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
    stock_receipts = relationship("StockReceipt", back_populates="purchase_order") 