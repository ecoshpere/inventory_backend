from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_order_id = Column(String, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    received_quantity = Column(Float, nullable=False, default=0.0)
    notes = Column(String, nullable=True)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product", back_populates="purchase_order_items") 