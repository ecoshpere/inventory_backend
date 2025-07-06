from sqlalchemy.orm import Session, joinedload
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
            items_data = update_data.pop('items', None)
            for field, value in update_data.items():
                setattr(db_purchase_order, field, value)
            if items_data is not None:
                # Update, add, and remove items
                existing_items = {item.id: item for item in db_purchase_order.items}
                updated_item_ids = set()
                for item_data in items_data:
                    item_id = item_data.get('id')
                    if item_id and item_id in existing_items:
                        # Update existing item
                        db_item = existing_items[item_id]
                        for k, v in item_data.items():
                            if k != 'id' and v is not None:
                                setattr(db_item, k, v)
                        updated_item_ids.add(item_id)
                    else:
                        # Add new item
                        from app.models.purchase_order_item import PurchaseOrderItem
                        new_item = PurchaseOrderItem(
                            purchase_order_id=purchase_order_id,
                            product_id=item_data['product_id'],
                            quantity=item_data['quantity'],
                            unit_price=item_data['unit_price'],
                            total_price=item_data['quantity'] * item_data['unit_price'],
                            notes=item_data.get('notes', None),
                            received_quantity=item_data.get('received_quantity', 0.0)
                        )
                        self.db.add(new_item)
                # Remove items not in update
                for item in list(db_purchase_order.items):
                    if item.id not in updated_item_ids and items_data:
                        self.db.delete(item)
                self.db.flush()  # Ensure new items are persisted
                self.db.refresh(db_purchase_order)  # Ensure items relationship is up to date
                db_purchase_order.total_amount = sum(
                    item.quantity * item.unit_price for item in db_purchase_order.items
                )
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

    def get_by_id_with_relationships(self, purchase_order_id: str) -> Optional[PurchaseOrder]:
        return (
            self.db.query(PurchaseOrder)
            .options(
                joinedload(PurchaseOrder.supplier),
                joinedload(PurchaseOrder.warehouse),
                joinedload(PurchaseOrder.items).joinedload(PurchaseOrderItem.product)
            )
            .filter(PurchaseOrder.id == purchase_order_id)
            .first()
        )

    def get_all_with_relationships(self, skip: int = 0, limit: int = 100) -> List[PurchaseOrder]:
        return (
            self.db.query(PurchaseOrder)
            .options(
                joinedload(PurchaseOrder.supplier),
                joinedload(PurchaseOrder.warehouse),
                joinedload(PurchaseOrder.items).joinedload(PurchaseOrderItem.product)
            )
            .offset(skip)
            .limit(limit)
            .all()
        ) 