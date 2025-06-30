from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.service.supplier_service import SupplierService
from app.dto.supplier import SupplierCreate, SupplierUpdate, SupplierResponse

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Create a new supplier"""
    try:
        service = SupplierService(db)
        return service.create_supplier(supplier)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all suppliers"""
    try:
        service = SupplierService(db)
        return service.get_suppliers(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/active", response_model=List[SupplierResponse])
def get_active_suppliers(db: Session = Depends(get_db)):
    """Get all active suppliers"""
    try:
        service = SupplierService(db)
        return service.get_active_suppliers()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: str, db: Session = Depends(get_db)):
    """Get a supplier by ID"""
    try:
        service = SupplierService(db)
        supplier = service.get_supplier(supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return supplier
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: str, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    """Update a supplier"""
    try:
        service = SupplierService(db)
        updated_supplier = service.update_supplier(supplier_id, supplier)
        if not updated_supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return updated_supplier
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: str, db: Session = Depends(get_db)):
    """Delete a supplier"""
    try:
        service = SupplierService(db)
        success = service.delete_supplier(supplier_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 