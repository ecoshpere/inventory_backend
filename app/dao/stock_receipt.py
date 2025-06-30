from sqlalchemy.orm import Session
from app.models.stock_receipt import StockReceipt
from app.models.stock_receipt_item import StockReceiptItem
from app.dto.stock_receipt import StockReceiptCreate, StockReceiptUpdate
from typing import List, Optional

class StockReceiptDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, stock_receipt: StockReceiptCreate) -> StockReceipt:
        # Extract items from the create DTO
        items_data = stock_receipt.items
        receipt_data = stock_receipt.dict(exclude={'items'})
        
        # Create stock receipt
        db_stock_receipt = StockReceipt(**receipt_data)
        self.db.add(db_stock_receipt)
        self.db.flush()  # Flush to get the ID
        
        # Calculate total amount
        total_amount = 0.0
        
        # Create stock receipt items
        for item_data in items_data:
            item_dict = item_data.dict()
            total_price = item_dict['quantity'] * item_dict['unit_price']
            total_amount += total_price
            
            db_item = StockReceiptItem(
                stock_receipt_id=db_stock_receipt.id,
                total_price=total_price,
                **item_dict
            )
            self.db.add(db_item)
        
        # Update total amount
        db_stock_receipt.total_amount = total_amount
        
        self.db.commit()
        self.db.refresh(db_stock_receipt)
        return db_stock_receipt

    def get_by_id(self, stock_receipt_id: str) -> Optional[StockReceipt]:
        return self.db.query(StockReceipt).filter(StockReceipt.id == stock_receipt_id).first()

    def get_by_receipt_number(self, receipt_number: str) -> Optional[StockReceipt]:
        return self.db.query(StockReceipt).filter(StockReceipt.receipt_number == receipt_number).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[StockReceipt]:
        return self.db.query(StockReceipt).offset(skip).limit(limit).all()

    def get_active(self) -> List[StockReceipt]:
        return self.db.query(StockReceipt).filter(StockReceipt.is_active == True).all()

    def get_by_purchase_order(self, purchase_order_id: str) -> List[StockReceipt]:
        return self.db.query(StockReceipt).filter(StockReceipt.purchase_order_id == purchase_order_id).all()

    def update(self, stock_receipt_id: str, stock_receipt: StockReceiptUpdate) -> Optional[StockReceipt]:
        db_stock_receipt = self.get_by_id(stock_receipt_id)
        if db_stock_receipt:
            update_data = stock_receipt.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_stock_receipt, field, value)
            self.db.commit()
            self.db.refresh(db_stock_receipt)
        return db_stock_receipt

    def delete(self, stock_receipt_id: str) -> bool:
        db_stock_receipt = self.get_by_id(stock_receipt_id)
        if db_stock_receipt:
            self.db.delete(db_stock_receipt)
            self.db.commit()
            return True
        return False

    def soft_delete(self, stock_receipt_id: str) -> bool:
        db_stock_receipt = self.get_by_id(stock_receipt_id)
        if db_stock_receipt:
            db_stock_receipt.is_active = False
            self.db.commit()
            return True
        return False

    def update_status(self, stock_receipt_id: str, status: str) -> Optional[StockReceipt]:
        db_stock_receipt = self.get_by_id(stock_receipt_id)
        if db_stock_receipt:
            db_stock_receipt.status = status
            self.db.commit()
            self.db.refresh(db_stock_receipt)
        return db_stock_receipt 