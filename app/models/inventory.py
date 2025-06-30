from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=0)
    available_quantity = Column(Float, nullable=False, default=0)
    markup_percentage = Column(Float, nullable=False, default=0)
    reorder_point = Column(Float, nullable=True)
    reorder_quantity = Column(Float, nullable=True)
    date_added = Column(String, nullable=False, default=lambda: datetime.utcnow().isoformat())
    last_updated = Column(String, nullable=False, default=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    product = relationship("Product", back_populates="inventory")
    warehouse = relationship("Warehouse", back_populates="stock_inventory") 