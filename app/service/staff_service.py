from sqlalchemy.orm import Session
from typing import List, Optional
from ..dao.staff import StaffDAO
from ..dto.staff import StaffCreate, StaffUpdate, StaffResponse

class StaffService:
    def __init__(self, db: Session):
        self.dao = StaffDAO(db)

    def create_staff(self, staff: StaffCreate) -> StaffResponse:
        # Check if employee number already exists
        existing_employee = self.dao.get_by_employee_number(staff.employee_number)
        if existing_employee:
            raise ValueError("Employee number already exists")
        
        # Check if email already exists
        existing_email = self.dao.get_by_email(staff.email_address)
        if existing_email:
            raise ValueError("Email address already exists")
        
        db_staff = self.dao.create(staff)
        return self._to_response(db_staff)

    def get_staff(self, staff_id: str) -> Optional[StaffResponse]:
        db_staff = self.dao.get_by_id(staff_id)
        if db_staff:
            return self._to_response(db_staff)
        return None

    def get_staff_list(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[StaffResponse]:
        db_staff = self.dao.get_all(skip=skip, limit=limit, search=search)
        return [self._to_response(staff) for staff in db_staff]

    def update_staff(self, staff_id: str, staff: StaffUpdate) -> Optional[StaffResponse]:
        # Check if employee number already exists (if being updated)
        if staff.employee_number:
            existing_employee = self.dao.get_by_employee_number(staff.employee_number)
            if existing_employee and existing_employee.id != staff_id:
                raise ValueError("Employee number already exists")
        
        # Check if email already exists (if being updated)
        if staff.email_address:
            existing_email = self.dao.get_by_email(staff.email_address)
            if existing_email and existing_email.id != staff_id:
                raise ValueError("Email address already exists")
        
        db_staff = self.dao.update(staff_id, staff)
        if db_staff:
            return self._to_response(db_staff)
        return None

    def delete_staff(self, staff_id: str) -> bool:
        return self.dao.delete(staff_id)

    def _to_response(self, db_staff) -> StaffResponse:
        return StaffResponse(
            id=db_staff.id,
            status=db_staff.status,
            title=db_staff.title,
            firstname=db_staff.firstname,
            middlename=db_staff.middlename,
            lastname=db_staff.lastname,
            mobile_number=db_staff.mobile_number,
            email_address=db_staff.email_address,
            address=db_staff.address,
            gender=db_staff.gender,
            date_of_birth=db_staff.date_of_birth,
            employee_number=db_staff.employee_number,
            designation=db_staff.designation,
            date_employed=db_staff.date_employed,
            department_id=db_staff.department_id,
            department_name=None,  # We'll add this back later
            created_at=db_staff.created_at,
            updated_at=db_staff.updated_at
        )
