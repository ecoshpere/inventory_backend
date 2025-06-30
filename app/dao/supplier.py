from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.dto.supplier import SupplierCreate, SupplierUpdate
from typing import List, Optional

class SupplierDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, supplier: SupplierCreate) -> Supplier:
        db_supplier = Supplier(**supplier.dict())
        self.db.add(db_supplier)
        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    def get_by_id(self, supplier_id: str) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def get_by_code(self, code: str) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.code == code).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def get_active(self) -> List[Supplier]:
        return self.db.query(Supplier).filter(Supplier.is_active == True).all()

    def update(self, supplier_id: str, supplier: SupplierUpdate) -> Optional[Supplier]:
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            update_data = supplier.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_supplier, field, value)
            self.db.commit()
            self.db.refresh(db_supplier)
        return db_supplier

    def delete(self, supplier_id: str) -> bool:
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            self.db.delete(db_supplier)
            self.db.commit()
            return True
        return False

    def soft_delete(self, supplier_id: str) -> bool:
        db_supplier = self.get_by_id(supplier_id)
        if db_supplier:
            db_supplier.is_active = False
            self.db.commit()
            return True
        return False 