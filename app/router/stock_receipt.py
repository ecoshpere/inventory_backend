from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.stock_receipt_service import StockReceiptService
from app.dto.stock_receipt import StockReceiptCreate, StockReceiptUpdate, StockReceiptResponse

router = APIRouter(prefix="/stock-receipts", tags=["stock-receipts"])

@router.post("/", response_model=StockReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_stock_receipt(stock_receipt: StockReceiptCreate, db: Session = Depends(get_db)):
    """Create a new stock receipt"""
    try:
        service = StockReceiptService(db)
        return service.create_stock_receipt(stock_receipt)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[StockReceiptResponse])
def get_stock_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all stock receipts"""
    try:
        service = StockReceiptService(db)
        return service.get_stock_receipts(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/active", response_model=List[StockReceiptResponse])
def get_active_stock_receipts(db: Session = Depends(get_db)):
    """Get all active stock receipts"""
    try:
        service = StockReceiptService(db)
        return service.get_active_stock_receipts()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/purchase-order/{purchase_order_id}", response_model=List[StockReceiptResponse])
def get_stock_receipts_by_purchase_order(purchase_order_id: str, db: Session = Depends(get_db)):
    """Get stock receipts by purchase order ID"""
    try:
        service = StockReceiptService(db)
        return service.get_stock_receipts_by_purchase_order(purchase_order_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{stock_receipt_id}", response_model=StockReceiptResponse)
def get_stock_receipt(stock_receipt_id: str, db: Session = Depends(get_db)):
    """Get a stock receipt by ID"""
    try:
        service = StockReceiptService(db)
        stock_receipt = service.get_stock_receipt(stock_receipt_id)
        if not stock_receipt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock receipt not found")
        return stock_receipt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{stock_receipt_id}", response_model=StockReceiptResponse)
def update_stock_receipt(stock_receipt_id: str, stock_receipt: StockReceiptUpdate, db: Session = Depends(get_db)):
    """Update a stock receipt"""
    try:
        service = StockReceiptService(db)
        updated_stock_receipt = service.update_stock_receipt(stock_receipt_id, stock_receipt)
        if not updated_stock_receipt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock receipt not found")
        return updated_stock_receipt
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.patch("/{stock_receipt_id}/status", response_model=StockReceiptResponse)
def update_stock_receipt_status(stock_receipt_id: str, status: str, db: Session = Depends(get_db)):
    """Update stock receipt status"""
    try:
        service = StockReceiptService(db)
        updated_stock_receipt = service.update_stock_receipt_status(stock_receipt_id, status)
        if not updated_stock_receipt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock receipt not found")
        return updated_stock_receipt
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{stock_receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_receipt(stock_receipt_id: str, db: Session = Depends(get_db)):
    """Delete a stock receipt"""
    try:
        service = StockReceiptService(db)
        success = service.delete_stock_receipt(stock_receipt_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock receipt not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 