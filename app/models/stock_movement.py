from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    movement_number = Column(String, unique=True, nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    source_warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    destination_warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    movement_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default="Draft")  # Draft, Completed, Cancelled
    movement_type = Column(String, nullable=False)  # Transfer, Adjustment, Return
    reference_number = Column(String, nullable=True)  # PO, SO, or other reference
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="stock_movements")
    source_warehouse = relationship("Warehouse", foreign_keys=[source_warehouse_id], back_populates="outgoing_movements")
    destination_warehouse = relationship("Warehouse", foreign_keys=[destination_warehouse_id], back_populates="incoming_movements") 