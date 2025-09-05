from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional
import uuid
from ..models.staff import Staff
from ..models.department import Department
from ..dto.staff import StaffCreate, StaffUpdate

class StaffDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, staff: StaffCreate) -> Staff:
        db_staff = Staff(
            id=str(uuid.uuid4()),
            status=staff.status,
            title=staff.title,
            firstname=staff.firstname,
            middlename=staff.middlename,
            lastname=staff.lastname,
            mobile_number=staff.mobile_number,
            email_address=staff.email_address,
            address=staff.address,
            gender=staff.gender,
            date_of_birth=staff.date_of_birth,
            employee_number=staff.employee_number,
            designation=staff.designation,
            date_employed=staff.date_employed,
            department_id=staff.department_id
        )
        self.db.add(db_staff)
        self.db.commit()
        self.db.refresh(db_staff)
        return db_staff

    def get_by_id(self, staff_id: str) -> Optional[Staff]:
        return self.db.query(Staff).options(
            joinedload(Staff.department)
        ).filter(Staff.id == staff_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Staff]:
        query = self.db.query(Staff).options(
            joinedload(Staff.department)
        )
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Staff.firstname.ilike(search_term),
                    Staff.lastname.ilike(search_term),
                    Staff.employee_number.ilike(search_term),
                    Staff.email_address.ilike(search_term),
                    Staff.designation.ilike(search_term)
                )
            )
        
        return query.offset(skip).limit(limit).all()

    def update(self, staff_id: str, staff: StaffUpdate) -> Optional[Staff]:
        db_staff = self.get_by_id(staff_id)
        if not db_staff:
            return None
        
        update_data = staff.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_staff, field, value)
        
        self.db.commit()
        self.db.refresh(db_staff)
        return db_staff

    def delete(self, staff_id: str) -> bool:
        db_staff = self.get_by_id(staff_id)
        if not db_staff:
            return False
        
        self.db.delete(db_staff)
        self.db.commit()
        return True

    def get_by_employee_number(self, employee_number: str) -> Optional[Staff]:
        return self.db.query(Staff).options(
            joinedload(Staff.department)
        ).filter(Staff.employee_number == employee_number).first()

    def get_by_email(self, email: str) -> Optional[Staff]:
        return self.db.query(Staff).options(
            joinedload(Staff.department)
        ).filter(Staff.email_address == email).first()
