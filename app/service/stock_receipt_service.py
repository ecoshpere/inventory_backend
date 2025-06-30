from sqlalchemy.orm import Session
from app.dao.stock_receipt import StockReceiptDAO
from app.dto.stock_receipt import StockReceiptCreate, StockReceiptUpdate, StockReceiptResponse
from typing import List, Optional

class StockReceiptService:
    def __init__(self, db: Session):
        self.dao = StockReceiptDAO(db)

    def create_stock_receipt(self, stock_receipt: StockReceiptCreate) -> StockReceiptResponse:
        # Check if receipt number already exists
        existing_receipt = self.dao.get_by_receipt_number(stock_receipt.receipt_number)
        if existing_receipt:
            raise ValueError(f"Stock receipt with number {stock_receipt.receipt_number} already exists")
        
        # Validate items
        if not stock_receipt.items:
            raise ValueError("Stock receipt must have at least one item")
        
        db_stock_receipt = self.dao.create(stock_receipt)
        return StockReceiptResponse.from_orm(db_stock_receipt)

    def get_stock_receipt(self, stock_receipt_id: str) -> Optional[StockReceiptResponse]:
        db_stock_receipt = self.dao.get_by_id(stock_receipt_id)
        if db_stock_receipt:
            return StockReceiptResponse.from_orm(db_stock_receipt)
        return None

    def get_stock_receipts(self, skip: int = 0, limit: int = 100) -> List[StockReceiptResponse]:
        db_stock_receipts = self.dao.get_all(skip=skip, limit=limit)
        return [StockReceiptResponse.from_orm(receipt) for receipt in db_stock_receipts]

    def get_active_stock_receipts(self) -> List[StockReceiptResponse]:
        db_stock_receipts = self.dao.get_active()
        return [StockReceiptResponse.from_orm(receipt) for receipt in db_stock_receipts]

    def get_stock_receipts_by_purchase_order(self, purchase_order_id: str) -> List[StockReceiptResponse]:
        db_stock_receipts = self.dao.get_by_purchase_order(purchase_order_id)
        return [StockReceiptResponse.from_orm(receipt) for receipt in db_stock_receipts]

    def update_stock_receipt(self, stock_receipt_id: str, stock_receipt: StockReceiptUpdate) -> Optional[StockReceiptResponse]:
        # If updating receipt number, check if it already exists
        if stock_receipt.receipt_number:
            existing_receipt = self.dao.get_by_receipt_number(stock_receipt.receipt_number)
            if existing_receipt and existing_receipt.id != stock_receipt_id:
                raise ValueError(f"Stock receipt with number {stock_receipt.receipt_number} already exists")
        
        db_stock_receipt = self.dao.update(stock_receipt_id, stock_receipt)
        if db_stock_receipt:
            return StockReceiptResponse.from_orm(db_stock_receipt)
        return None

    def delete_stock_receipt(self, stock_receipt_id: str) -> bool:
        return self.dao.soft_delete(stock_receipt_id)

    def update_stock_receipt_status(self, stock_receipt_id: str, status: str) -> Optional[StockReceiptResponse]:
        # Validate status
        valid_statuses = ["Draft", "Received", "Posted", "Cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        db_stock_receipt = self.dao.update_status(stock_receipt_id, status)
        if db_stock_receipt:
            return StockReceiptResponse.from_orm(db_stock_receipt)
        return None 