from sqlalchemy.orm import Session
from app.dao.purchase_order import PurchaseOrderDAO
from app.dto.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse
from typing import List, Optional

class PurchaseOrderService:
    def __init__(self, db: Session):
        self.dao = PurchaseOrderDAO(db)

    def create_purchase_order(self, purchase_order: PurchaseOrderCreate) -> PurchaseOrderResponse:
        # Check if PO number already exists
        existing_po = self.dao.get_by_po_number(purchase_order.po_number)
        if existing_po:
            raise ValueError(f"Purchase order with number {purchase_order.po_number} already exists")
        
        # Validate items
        if not purchase_order.items:
            raise ValueError("Purchase order must have at least one item")
        
        db_purchase_order = self.dao.create(purchase_order)
        return PurchaseOrderResponse.from_orm(db_purchase_order)

    def get_purchase_order(self, purchase_order_id: str) -> Optional[PurchaseOrderResponse]:
        db_purchase_order = self.dao.get_by_id(purchase_order_id)
        if db_purchase_order:
            return PurchaseOrderResponse.from_orm(db_purchase_order)
        return None

    def get_purchase_orders(self, skip: int = 0, limit: int = 100) -> List[PurchaseOrderResponse]:
        db_purchase_orders = self.dao.get_all(skip=skip, limit=limit)
        return [PurchaseOrderResponse.from_orm(po) for po in db_purchase_orders]

    def get_active_purchase_orders(self) -> List[PurchaseOrderResponse]:
        db_purchase_orders = self.dao.get_active()
        return [PurchaseOrderResponse.from_orm(po) for po in db_purchase_orders]

    def update_purchase_order(self, purchase_order_id: str, purchase_order: PurchaseOrderUpdate) -> Optional[PurchaseOrderResponse]:
        # If updating PO number, check if it already exists
        if purchase_order.po_number:
            existing_po = self.dao.get_by_po_number(purchase_order.po_number)
            if existing_po and existing_po.id != purchase_order_id:
                raise ValueError(f"Purchase order with number {purchase_order.po_number} already exists")
        
        db_purchase_order = self.dao.update(purchase_order_id, purchase_order)
        if db_purchase_order:
            return PurchaseOrderResponse.from_orm(db_purchase_order)
        return None

    def delete_purchase_order(self, purchase_order_id: str) -> bool:
        return self.dao.soft_delete(purchase_order_id)

    def update_purchase_order_status(self, purchase_order_id: str, status: str) -> Optional[PurchaseOrderResponse]:
        # Validate status
        valid_statuses = ["Draft", "Submitted", "Approved", "Received", "Cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        db_purchase_order = self.dao.update_status(purchase_order_id, status)
        if db_purchase_order:
            return PurchaseOrderResponse.from_orm(db_purchase_order)
        return None 