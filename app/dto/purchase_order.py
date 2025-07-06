from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.dto.supplier import SupplierResponse
from app.dto.warehouse import WarehouseResponse
from app.dto.product import ProductResponse

class PurchaseOrderItemBase(BaseModel):
    product_id: str
    quantity: float
    unit_price: float
    notes: Optional[str] = None

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemUpdate(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    notes: Optional[str] = None

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: str
    total_price: float
    received_quantity: float
    product: ProductResponse
    
    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    po_number: str
    supplier_id: str
    warehouse_id: str
    order_date: datetime
    expected_delivery_date: Optional[datetime] = None
    status: str = "Draft"
    notes: Optional[str] = None
    is_active: bool = True

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]

class PurchaseOrderUpdate(BaseModel):
    po_number: Optional[str] = None
    supplier_id: Optional[str] = None
    warehouse_id: Optional[str] = None
    order_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
    items: Optional[List[PurchaseOrderItemUpdate]] = None

class PurchaseOrderResponse(PurchaseOrderBase):
    id: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[PurchaseOrderItemResponse] = []
    supplier: SupplierResponse
    warehouse: WarehouseResponse
    
    class Config:
        from_attributes = True 