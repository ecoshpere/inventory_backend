from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.service.inventory_service import InventoryService
from app.dto.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.database import get_db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.get("/", response_model=List[InventoryResponse])
def get_inventory_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory_list(skip, limit)

@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(inventory_id: str, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    inventory = inventory_service.get_inventory(inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inventory

@router.get("/product/{product_id}", response_model=List[InventoryResponse])
def get_inventory_by_product(product_id: str, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory_by_product(product_id)

@router.get("/warehouse/{warehouse_id}", response_model=List[InventoryResponse])
def get_inventory_by_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory_by_warehouse(warehouse_id)

@router.get("/product/{product_id}/warehouse/{warehouse_id}", response_model=InventoryResponse)
def get_inventory_by_product_and_warehouse(product_id: str, warehouse_id: str, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    inventory = inventory_service.get_inventory_by_product_and_warehouse(product_id, warehouse_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inventory

@router.post("/", response_model=InventoryResponse)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    return inventory_service.create_inventory(inventory)

@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(inventory_id: str, inventory: InventoryUpdate, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    updated_inventory = inventory_service.update_inventory(inventory_id, inventory)
    if updated_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return updated_inventory

@router.patch("/{inventory_id}/quantity", response_model=InventoryResponse)
def update_quantity(inventory_id: str, quantity_change: float, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    updated_inventory = inventory_service.update_quantity(inventory_id, quantity_change)
    if updated_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return updated_inventory

@router.patch("/{inventory_id}/available-quantity", response_model=InventoryResponse)
def update_available_quantity(inventory_id: str, available_quantity_change: float, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    updated_inventory = inventory_service.update_available_quantity(inventory_id, available_quantity_change)
    if updated_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return updated_inventory

@router.delete("/{inventory_id}")
def delete_inventory(inventory_id: str, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    success = inventory_service.delete_inventory(inventory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return {"message": "Inventory record deleted successfully"} 