from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class StockReceiptItem(Base):
    __tablename__ = "stock_receipt_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stock_receipt_id = Column(String, ForeignKey("stock_receipts.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    
    # Relationships
    stock_receipt = relationship("StockReceipt", back_populates="items")
    product = relationship("Product", back_populates="stock_receipt_items") 