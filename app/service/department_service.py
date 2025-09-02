from sqlalchemy.orm import Session
from typing import List, Optional
from ..dao.department import DepartmentDAO
from ..dto.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse

class DepartmentService:
    def __init__(self, db: Session):
        self.dao = DepartmentDAO(db)

    def create_department(self, department: DepartmentCreate) -> DepartmentResponse:
        db_department = self.dao.create(department)
        return DepartmentResponse.from_orm(db_department)

    def get_department(self, department_id: str) -> Optional[DepartmentResponse]:
        db_department = self.dao.get_by_id(department_id)
        if db_department:
            return DepartmentResponse.from_orm(db_department)
        return None

    def get_departments(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[DepartmentResponse]:
        db_departments = self.dao.get_all(skip=skip, limit=limit, search=search)
        return [DepartmentResponse.from_orm(dept) for dept in db_departments]

    def update_department(self, department_id: str, department: DepartmentUpdate) -> Optional[DepartmentResponse]:
        db_department = self.dao.update(department_id, department)
        if db_department:
            return DepartmentResponse.from_orm(db_department)
        return None

    def delete_department(self, department_id: str) -> bool:
        return self.dao.delete(department_id)
