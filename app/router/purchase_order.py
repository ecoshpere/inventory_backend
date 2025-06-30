from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.purchase_order_service import PurchaseOrderService
from app.dto.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse

router = APIRouter(prefix="/purchase-orders", tags=["purchase-orders"])

@router.post("/", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(purchase_order: PurchaseOrderCreate, db: Session = Depends(get_db)):
    """Create a new purchase order"""
    try:
        service = PurchaseOrderService(db)
        return service.create_purchase_order(purchase_order)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[PurchaseOrderResponse])
def get_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all purchase orders"""
    try:
        service = PurchaseOrderService(db)
        return service.get_purchase_orders(skip=skip, limit=limit)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/active", response_model=List[PurchaseOrderResponse])
def get_active_purchase_orders(db: Session = Depends(get_db)):
    """Get all active purchase orders"""
    try:
        service = PurchaseOrderService(db)
        return service.get_active_purchase_orders()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(purchase_order_id: str, db: Session = Depends(get_db)):
    """Get a purchase order by ID"""
    try:
        service = PurchaseOrderService(db)
        purchase_order = service.get_purchase_order(purchase_order_id)
        if not purchase_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
        return purchase_order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(purchase_order_id: str, purchase_order: PurchaseOrderUpdate, db: Session = Depends(get_db)):
    """Update a purchase order"""
    try:
        service = PurchaseOrderService(db)
        updated_purchase_order = service.update_purchase_order(purchase_order_id, purchase_order)
        if not updated_purchase_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
        return updated_purchase_order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.patch("/{purchase_order_id}/status", response_model=PurchaseOrderResponse)
def update_purchase_order_status(purchase_order_id: str, status: str, db: Session = Depends(get_db)):
    """Update purchase order status"""
    try:
        service = PurchaseOrderService(db)
        updated_purchase_order = service.update_purchase_order_status(purchase_order_id, status)
        if not updated_purchase_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
        return updated_purchase_order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{purchase_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_order(purchase_order_id: str, db: Session = Depends(get_db)):
    """Delete a purchase order"""
    try:
        service = PurchaseOrderService(db)
        success = service.delete_purchase_order(purchase_order_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 