from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockMovementBase(BaseModel):
    movement_number: str
    product_id: str
    source_warehouse_id: str
    destination_warehouse_id: str
    quantity: float
    movement_date: datetime
    movement_type: str
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementUpdate(BaseModel):
    movement_number: Optional[str] = None
    product_id: Optional[str] = None
    source_warehouse_id: Optional[str] = None
    destination_warehouse_id: Optional[str] = None
    quantity: Optional[float] = None
    movement_date: Optional[datetime] = None
    movement_type: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class StockMovementResponse(StockMovementBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 