from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.stock_movement_service import StockMovementService
from app.dto.stock_movement import StockMovementCreate, StockMovementUpdate, StockMovementResponse

router = APIRouter(prefix="/stock-movements", tags=["stock-movements"])

@router.post("/", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def create_stock_movement(stock_movement: StockMovementCreate, db: Session = Depends(get_db)):
    """Create a new stock movement"""
    try:
        service = StockMovementService(db)
        return service.create_stock_movement(stock_movement)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[StockMovementResponse])
def get_stock_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all stock movements"""
    try:
        service = StockMovementService(db)
        return service.get_stock_movements(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/active", response_model=List[StockMovementResponse])
def get_active_stock_movements(db: Session = Depends(get_db)):
    """Get all active stock movements"""
    try:
        service = StockMovementService(db)
        return service.get_active_stock_movements()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{stock_movement_id}", response_model=StockMovementResponse)
def get_stock_movement(stock_movement_id: str, db: Session = Depends(get_db)):
    """Get a stock movement by ID"""
    try:
        service = StockMovementService(db)
        stock_movement = service.get_stock_movement(stock_movement_id)
        if not stock_movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
        return stock_movement
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{stock_movement_id}", response_model=StockMovementResponse)
def update_stock_movement(stock_movement_id: str, stock_movement: StockMovementUpdate, db: Session = Depends(get_db)):
    """Update a stock movement"""
    try:
        service = StockMovementService(db)
        updated_stock_movement = service.update_stock_movement(stock_movement_id, stock_movement)
        if not updated_stock_movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
        return updated_stock_movement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.patch("/{stock_movement_id}/status", response_model=StockMovementResponse)
def update_stock_movement_status(stock_movement_id: str, status: str, db: Session = Depends(get_db)):
    """Update stock movement status"""
    try:
        service = StockMovementService(db)
        updated_stock_movement = service.update_stock_movement_status(stock_movement_id, status)
        if not updated_stock_movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
        return updated_stock_movement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{stock_movement_id}/execute", response_model=StockMovementResponse)
def execute_stock_movement(stock_movement_id: str, db: Session = Depends(get_db)):
    """Execute a stock movement (move from Draft to Completed)"""
    try:
        service = StockMovementService(db)
        success = service.execute_stock_movement(stock_movement_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to execute stock movement")
        
        # Return the updated stock movement
        updated_movement = service.get_stock_movement(stock_movement_id)
        if not updated_movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
        return updated_movement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/check-availability/{product_id}/{warehouse_id}/{quantity}")
def check_warehouse_availability(product_id: str, warehouse_id: str, quantity: float, db: Session = Depends(get_db)):
    """Check if a warehouse has sufficient quantity of a product"""
    try:
        service = StockMovementService(db)
        is_available = service.check_warehouse_availability(product_id, warehouse_id, quantity)
        return {"available": is_available, "product_id": product_id, "warehouse_id": warehouse_id, "quantity": quantity}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{stock_movement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_movement(stock_movement_id: str, db: Session = Depends(get_db)):
    """Delete a stock movement"""
    try:
        service = StockMovementService(db)
        success = service.delete_stock_movement(stock_movement_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock movement not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 