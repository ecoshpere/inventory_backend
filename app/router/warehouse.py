from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.service.warehouse_service import WarehouseService
from app.dto.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from app.database import get_db

router = APIRouter(
    prefix="/warehouses",
    tags=["warehouses"]
)

@router.get("/", response_model=List[WarehouseResponse])
def get_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    return warehouse_service.get_warehouses(skip, limit)

@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@router.post("/", response_model=WarehouseResponse)
def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    return warehouse_service.create_warehouse(warehouse)

@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(warehouse_id: str, warehouse: WarehouseUpdate, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    updated_warehouse = warehouse_service.update_warehouse(warehouse_id, warehouse)
    if updated_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return updated_warehouse

@router.delete("/{warehouse_id}")
def delete_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    success = warehouse_service.delete_warehouse(warehouse_id)
    if not success:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return {"message": "Warehouse deleted successfully"}

@router.get("/search/{query}", response_model=List[WarehouseResponse])
def search_warehouses(query: str, db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    return warehouse_service.search_warehouses(query)

@router.get("/active", response_model=List[WarehouseResponse])
def get_active_warehouses(db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    return warehouse_service.get_active_warehouses()

@router.get("/default", response_model=WarehouseResponse)
def get_default_warehouse(db: Session = Depends(get_db)):
    warehouse_service = WarehouseService(db)
    warehouse = warehouse_service.get_default_warehouse()
    if warehouse is None:
        raise HTTPException(status_code=404, detail="No default warehouse found")
    return warehouse 