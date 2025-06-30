from pydantic import BaseModel, Field
from typing import Optional
import uuid

class ProductBase(BaseModel):
    name: str
    sku: str
    default_unit_price: Optional[float] = None
    units: str
    rating: float = 0
    default_markup_percent: float
    status: str = "Active"
    category_id: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    sku: Optional[str] = None
    units: Optional[str] = None
    default_markup_percent: Optional[float] = None
    status: Optional[str] = None
    category_id: Optional[str] = None

class ProductResponse(ProductBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True 