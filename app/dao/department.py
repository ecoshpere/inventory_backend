from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import uuid
from ..models.department import Department
from ..dto.department import DepartmentCreate, DepartmentUpdate

class DepartmentDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, department: DepartmentCreate) -> Department:
        db_department = Department(
            id=str(uuid.uuid4()),
            name=department.name,
            function=department.function
        )
        self.db.add(db_department)
        self.db.commit()
        self.db.refresh(db_department)
        return db_department

    def get_by_id(self, department_id: str) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == department_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Department]:
        query = self.db.query(Department)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Department.name.ilike(search_term),
                    Department.function.ilike(search_term)
                )
            )
        
        return query.offset(skip).limit(limit).all()

    def update(self, department_id: str, department: DepartmentUpdate) -> Optional[Department]:
        db_department = self.get_by_id(department_id)
        if not db_department:
            return None
        
        update_data = department.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_department, field, value)
        
        self.db.commit()
        self.db.refresh(db_department)
        return db_department

    def delete(self, department_id: str) -> bool:
        db_department = self.get_by_id(department_id)
        if not db_department:
            return False
        
        self.db.delete(db_department)
        self.db.commit()
        return True
