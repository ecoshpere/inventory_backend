from sqlalchemy.orm import Session
from app.dao.supplier import SupplierDAO
from app.dto.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from typing import List, Optional

class SupplierService:
    def __init__(self, db: Session):
        self.dao = SupplierDAO(db)

    def create_supplier(self, supplier: SupplierCreate) -> SupplierResponse:
        # Check if supplier with same code already exists
        existing_supplier = self.dao.get_by_code(supplier.code)
        if existing_supplier:
            raise ValueError(f"Supplier with code {supplier.code} already exists")
        
        db_supplier = self.dao.create(supplier)
        return SupplierResponse.from_orm(db_supplier)

    def get_supplier(self, supplier_id: str) -> Optional[SupplierResponse]:
        db_supplier = self.dao.get_by_id(supplier_id)
        if db_supplier:
            return SupplierResponse.from_orm(db_supplier)
        return None

    def get_suppliers(self, skip: int = 0, limit: int = 100) -> List[SupplierResponse]:
        db_suppliers = self.dao.get_all(skip=skip, limit=limit)
        return [SupplierResponse.from_orm(supplier) for supplier in db_suppliers]

    def get_active_suppliers(self) -> List[SupplierResponse]:
        db_suppliers = self.dao.get_active()
        return [SupplierResponse.from_orm(supplier) for supplier in db_suppliers]

    def update_supplier(self, supplier_id: str, supplier: SupplierUpdate) -> Optional[SupplierResponse]:
        # If updating code, check if it already exists
        if supplier.code:
            existing_supplier = self.dao.get_by_code(supplier.code)
            if existing_supplier and existing_supplier.id != supplier_id:
                raise ValueError(f"Supplier with code {supplier.code} already exists")
        
        db_supplier = self.dao.update(supplier_id, supplier)
        if db_supplier:
            return SupplierResponse.from_orm(db_supplier)
        return None

    def delete_supplier(self, supplier_id: str) -> bool:
        return self.dao.soft_delete(supplier_id) 