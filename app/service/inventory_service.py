from typing import List, Optional
from sqlalchemy.orm import Session
from app.dao.inventory import InventoryDAO
from app.dto.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.models.inventory import Inventory

class InventoryService:
    def __init__(self, db: Session):
        self.inventory_dao = InventoryDAO(db)

    def get_inventory(self, inventory_id: str) -> Optional[InventoryResponse]:
        inventory = self.inventory_dao.get_inventory(inventory_id)
        if inventory:
            return InventoryResponse.model_validate(inventory)
        return None

    def get_inventory_by_product_and_warehouse(self, product_id: str, warehouse_id: str) -> Optional[InventoryResponse]:
        inventory = self.inventory_dao.get_inventory_by_product_and_warehouse(product_id, warehouse_id)
        if inventory:
            return InventoryResponse.model_validate(inventory)
        return None

    def get_inventory_list(self, skip: int = 0, limit: int = 100) -> List[InventoryResponse]:
        inventory_list = self.inventory_dao.get_inventory_list(skip, limit)
        return [InventoryResponse.model_validate(inventory) for inventory in inventory_list]

    def create_inventory(self, inventory: InventoryCreate) -> InventoryResponse:
        inventory_data = inventory.model_dump()
        created_inventory = self.inventory_dao.create_inventory(inventory_data)
        return InventoryResponse.model_validate(created_inventory)

    def update_inventory(self, inventory_id: str, inventory: InventoryUpdate) -> Optional[InventoryResponse]:
        inventory_data = inventory.model_dump(exclude_unset=True)
        updated_inventory = self.inventory_dao.update_inventory(inventory_id, inventory_data)
        if updated_inventory:
            return InventoryResponse.model_validate(updated_inventory)
        return None

    def delete_inventory(self, inventory_id: str) -> bool:
        return self.inventory_dao.delete_inventory(inventory_id)

    def get_inventory_by_product(self, product_id: str) -> List[InventoryResponse]:
        inventory_list = self.inventory_dao.get_inventory_by_product(product_id)
        return [InventoryResponse.model_validate(inventory) for inventory in inventory_list]

    def get_inventory_by_warehouse(self, warehouse_id: str) -> List[InventoryResponse]:
        inventory_list = self.inventory_dao.get_inventory_by_warehouse(warehouse_id)
        return [InventoryResponse.model_validate(inventory) for inventory in inventory_list]

    def update_quantity(self, inventory_id: str, quantity_change: float) -> Optional[InventoryResponse]:
        updated_inventory = self.inventory_dao.update_quantity(inventory_id, quantity_change)
        if updated_inventory:
            return InventoryResponse.model_validate(updated_inventory)
        return None

    def update_available_quantity(self, inventory_id: str, available_quantity_change: float) -> Optional[InventoryResponse]:
        updated_inventory = self.inventory_dao.update_available_quantity(inventory_id, available_quantity_change)
        if updated_inventory:
            return InventoryResponse.model_validate(updated_inventory)
        return None 