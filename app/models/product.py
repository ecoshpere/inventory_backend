from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    default_unit_price = Column(Float, nullable=True)
    units = Column(String, nullable=False)
    rating = Column(Float, default=0)
    default_markup_percent = Column(Float, nullable=False)
    status = Column(String, default="Active")
    category_id = Column(String, ForeignKey("categories.id"))
    
    # Relationships
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    purchase_order_items = relationship("PurchaseOrderItem", back_populates="product")
    stock_receipt_items = relationship("StockReceiptItem", back_populates="product")
    stock_movements = relationship("StockMovement", back_populates="product") 