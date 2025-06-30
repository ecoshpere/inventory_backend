from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class StockReceipt(Base):
    __tablename__ = "stock_receipts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    receipt_number = Column(String, unique=True, nullable=False)
    purchase_order_id = Column(String, ForeignKey("purchase_orders.id"), nullable=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=False)
    receipt_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default="Draft")  # Draft, Received, Posted, Cancelled
    total_amount = Column(Float, nullable=False, default=0.0)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="stock_receipts")
    warehouse = relationship("Warehouse", back_populates="stock_receipts")
    supplier = relationship("Supplier", back_populates="stock_receipts")
    items = relationship("StockReceiptItem", back_populates="stock_receipt", cascade="all, delete-orphan") 