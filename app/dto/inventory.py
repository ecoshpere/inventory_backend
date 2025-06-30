from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class InventoryBase(BaseModel):
    product_id: str
    warehouse_id: str
    quantity: float = 0
    available_quantity: float = 0
    markup_percentage: float = 0
    reorder_point: Optional[float] = None
    reorder_quantity: Optional[float] = None
    date_added: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    product_id: Optional[str] = None
    warehouse_id: Optional[str] = None
    quantity: Optional[float] = None
    available_quantity: Optional[float] = None
    markup_percentage: Optional[float] = None
    reorder_point: Optional[float] = None
    reorder_quantity: Optional[float] = None
    date_added: Optional[str] = None
    last_updated: Optional[str] = None

class InventoryResponse(InventoryBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True 