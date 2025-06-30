from sqlalchemy.orm import Session
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.dto.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from typing import List, Optional

class PurchaseOrderDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, purchase_order: PurchaseOrderCreate) -> PurchaseOrder:
        # Extract items from the create DTO
        items_data = purchase_order.items
        po_data = purchase_order.dict(exclude={'items'})
        
        # Create purchase order
        db_purchase_order = PurchaseOrder(**po_data)
        self.db.add(db_purchase_order)
        self.db.flush()  # Flush to get the ID
        
        # Calculate total amount
        total_amount = 0.0
        
        # Create purchase order items
        for item_data in items_data:
            item_dict = item_data.dict()
            total_price = item_dict['quantity'] * item_dict['unit_price']
            total_amount += total_price
            
            db_item = PurchaseOrderItem(
                purchase_order_id=db_purchase_order.id,
                total_price=total_price,
                **item_dict
            )
            self.db.add(db_item)
        
        # Update total amount
        db_purchase_order.total_amount = total_amount
        
        self.db.commit()
        self.db.refresh(db_purchase_order)
        return db_purchase_order

    def get_by_id(self, purchase_order_id: str) -> Optional[PurchaseOrder]:
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()

    def get_by_po_number(self, po_number: str) -> Optional[PurchaseOrder]:
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.po_number == po_number).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PurchaseOrder]:
        return self.db.query(PurchaseOrder).offset(skip).limit(limit).all()

    def get_active(self) -> List[PurchaseOrder]:
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.is_active == True).all()

    def update(self, purchase_order_id: str, purchase_order: PurchaseOrderUpdate) -> Optional[PurchaseOrder]:
        db_purchase_order = self.get_by_id(purchase_order_id)
        if db_purchase_order:
            update_data = purchase_order.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_purchase_order, field, value)
            self.db.commit()
            self.db.refresh(db_purchase_order)
        return db_purchase_order

    def delete(self, purchase_order_id: str) -> bool:
        db_purchase_order = self.get_by_id(purchase_order_id)
        if db_purchase_order:
            self.db.delete(db_purchase_order)
            self.db.commit()
            return True
        return False

    def soft_delete(self, purchase_order_id: str) -> bool:
        db_purchase_order = self.get_by_id(purchase_order_id)
        if db_purchase_order:
            db_purchase_order.is_active = False
            self.db.commit()
            return True
        return False

    def update_status(self, purchase_order_id: str, status: str) -> Optional[PurchaseOrder]:
        db_purchase_order = self.get_by_id(purchase_order_id)
        if db_purchase_order:
            db_purchase_order.status = status
            self.db.commit()
            self.db.refresh(db_purchase_order)
        return db_purchase_order 