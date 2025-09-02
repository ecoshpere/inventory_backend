from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..service.department_service import DepartmentService
from ..dto.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    service = DepartmentService(db)
    return service.create_department(department)

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: str,
    db: Session = Depends(get_db)
):
    service = DepartmentService(db)
    department = service.get_department(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    service = DepartmentService(db)
    return service.get_departments(skip=skip, limit=limit, search=search)

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: str,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    service = DepartmentService(db)
    updated_department = service.update_department(department_id, department)
    if not updated_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated_department

@router.delete("/{department_id}")
def delete_department(
    department_id: str,
    db: Session = Depends(get_db)
):
    service = DepartmentService(db)
    success = service.delete_department(department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department deleted successfully"}
