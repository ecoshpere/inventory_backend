from typing import List, Optional
from sqlalchemy.orm import Session
from app.dao.warehouse import WarehouseDAO
from app.dto.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from app.models.warehouse import Warehouse

class WarehouseService:
    def __init__(self, db: Session):
        self.warehouse_dao = WarehouseDAO(db)

    def get_warehouse(self, warehouse_id: str) -> Optional[WarehouseResponse]:
        warehouse = self.warehouse_dao.get_warehouse(warehouse_id)
        if warehouse:
            return WarehouseResponse.model_validate(warehouse)
        return None

    def get_warehouses(self, skip: int = 0, limit: int = 100) -> List[WarehouseResponse]:
        warehouses = self.warehouse_dao.get_warehouses(skip, limit)
        return [WarehouseResponse.model_validate(warehouse) for warehouse in warehouses]

    def create_warehouse(self, warehouse: WarehouseCreate) -> WarehouseResponse:
        warehouse_data = warehouse.model_dump()
        created_warehouse = self.warehouse_dao.create_warehouse(warehouse_data)
        return WarehouseResponse.model_validate(created_warehouse)

    def update_warehouse(self, warehouse_id: str, warehouse: WarehouseUpdate) -> Optional[WarehouseResponse]:
        warehouse_data = warehouse.model_dump(exclude_unset=True)
        updated_warehouse = self.warehouse_dao.update_warehouse(warehouse_id, warehouse_data)
        if updated_warehouse:
            return WarehouseResponse.model_validate(updated_warehouse)
        return None

    def delete_warehouse(self, warehouse_id: str) -> bool:
        return self.warehouse_dao.delete_warehouse(warehouse_id)

    def search_warehouses(self, query: str) -> List[WarehouseResponse]:
        warehouses = self.warehouse_dao.search_warehouses(query)
        return [WarehouseResponse.model_validate(warehouse) for warehouse in warehouses]

    def get_active_warehouses(self) -> List[WarehouseResponse]:
        warehouses = self.warehouse_dao.get_active_warehouses()
        return [WarehouseResponse.model_validate(warehouse) for warehouse in warehouses]

    def get_default_warehouse(self) -> Optional[WarehouseResponse]:
        warehouse = self.warehouse_dao.get_default_warehouse()
        if warehouse:
            return WarehouseResponse.model_validate(warehouse)
        return None 