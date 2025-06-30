from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StockReceiptItemBase(BaseModel):
    product_id: str
    quantity: float
    unit_price: float
    notes: Optional[str] = None

class StockReceiptItemCreate(StockReceiptItemBase):
    pass

class StockReceiptItemUpdate(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    notes: Optional[str] = None

class StockReceiptItemResponse(StockReceiptItemBase):
    id: str
    total_price: float
    
    class Config:
        from_attributes = True

class StockReceiptBase(BaseModel):
    receipt_number: str
    purchase_order_id: Optional[str] = None
    warehouse_id: str
    supplier_id: str
    receipt_date: datetime
    status: str = "Draft"
    notes: Optional[str] = None
    is_active: bool = True

class StockReceiptCreate(StockReceiptBase):
    items: List[StockReceiptItemCreate]

class StockReceiptUpdate(BaseModel):
    receipt_number: Optional[str] = None
    purchase_order_id: Optional[str] = None
    warehouse_id: Optional[str] = None
    supplier_id: Optional[str] = None
    receipt_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class StockReceiptResponse(StockReceiptBase):
    id: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[StockReceiptItemResponse] = []
    
    class Config:
        from_attributes = True 