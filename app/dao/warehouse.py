from sqlalchemy.orm import Session
from app.models.warehouse import Warehouse
from typing import List, Optional

class WarehouseDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_warehouse(self, warehouse_id: str) -> Optional[Warehouse]:
        return self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    def get_warehouses(self, skip: int = 0, limit: int = 100) -> List[Warehouse]:
        return self.db.query(Warehouse).offset(skip).limit(limit).all()

    def create_warehouse(self, warehouse_data: dict) -> Warehouse:
        # If this warehouse is being set as default, unset any existing default warehouse
        if warehouse_data.get('is_default', False):
            self.db.query(Warehouse).filter(Warehouse.is_default == True).update({"is_default": False})
        
        warehouse = Warehouse(**warehouse_data)
        self.db.add(warehouse)
        self.db.commit()
        self.db.refresh(warehouse)
        return warehouse

    def update_warehouse(self, warehouse_id: str, warehouse_data: dict) -> Optional[Warehouse]:
        # If this warehouse is being set as default, unset any existing default warehouse
        if warehouse_data.get('is_default', False):
            self.db.query(Warehouse).filter(
                Warehouse.is_default == True,
                Warehouse.id != warehouse_id
            ).update({"is_default": False})
        
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            for key, value in warehouse_data.items():
                setattr(warehouse, key, value)
            self.db.commit()
            self.db.refresh(warehouse)
        return warehouse

    def delete_warehouse(self, warehouse_id: str) -> bool:
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            self.db.delete(warehouse)
            self.db.commit()
            return True
        return False

    def search_warehouses(self, query: str) -> List[Warehouse]:
        return self.db.query(Warehouse).filter(
            (Warehouse.name.ilike(f"%{query}%")) | 
            (Warehouse.code.ilike(f"%{query}%")) |
            (Warehouse.address.ilike(f"%{query}%"))
        ).all()

    def get_active_warehouses(self) -> List[Warehouse]:
        return self.db.query(Warehouse).filter(Warehouse.is_active == True).all()

    def get_default_warehouse(self) -> Optional[Warehouse]:
        return self.db.query(Warehouse).filter(Warehouse.is_default == True).first() 