from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from typing import List, Optional
from datetime import datetime

class InventoryDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_inventory(self, inventory_id: str) -> Optional[Inventory]:
        return self.db.query(Inventory).filter(Inventory.id == inventory_id).first()

    def get_inventory_by_product_and_warehouse(self, product_id: str, warehouse_id: str) -> Optional[Inventory]:
        return self.db.query(Inventory).filter(
            Inventory.product_id == product_id,
            Inventory.warehouse_id == warehouse_id
        ).first()

    def get_inventory_list(self, skip: int = 0, limit: int = 100) -> List[Inventory]:
        return self.db.query(Inventory).offset(skip).limit(limit).all()

    def create_inventory(self, inventory_data: dict) -> Inventory:
        inventory = Inventory(**inventory_data)
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def update_inventory(self, inventory_id: str, inventory_data: dict) -> Optional[Inventory]:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            for key, value in inventory_data.items():
                if value is not None:
                    setattr(inventory, key, value)
            inventory.last_updated = datetime.utcnow().isoformat()
            self.db.commit()
            self.db.refresh(inventory)
        return inventory

    def delete_inventory(self, inventory_id: str) -> bool:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            self.db.delete(inventory)
            self.db.commit()
            return True
        return False

    def get_inventory_by_product(self, product_id: str) -> List[Inventory]:
        return self.db.query(Inventory).filter(Inventory.product_id == product_id).all()

    def get_inventory_by_warehouse(self, warehouse_id: str) -> List[Inventory]:
        return self.db.query(Inventory).filter(Inventory.warehouse_id == warehouse_id).all()

    def update_quantity(self, inventory_id: str, quantity_change: float) -> Optional[Inventory]:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            inventory.quantity += quantity_change
            inventory.available_quantity += quantity_change
            inventory.last_updated = datetime.utcnow().isoformat()
            self.db.commit()
            self.db.refresh(inventory)
        return inventory

    def update_available_quantity(self, inventory_id: str, available_quantity_change: float) -> Optional[Inventory]:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            inventory.available_quantity += available_quantity_change
            inventory.last_updated = datetime.utcnow().isoformat()
            self.db.commit()
            self.db.refresh(inventory)
        return inventory 