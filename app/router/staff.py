from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..service.staff_service import StaffService
from ..dto.staff import StaffCreate, StaffUpdate, StaffResponse

router = APIRouter(prefix="/staff", tags=["staff"])

@router.post("/", response_model=StaffResponse)
def create_staff(
    staff: StaffCreate,
    db: Session = Depends(get_db)
):
    service = StaffService(db)
    try:
        return service.create_staff(staff)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(
    staff_id: str,
    db: Session = Depends(get_db)
):
    service = StaffService(db)
    staff = service.get_staff(staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.get("/", response_model=List[StaffResponse])
def get_staff_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    service = StaffService(db)
    return service.get_staff_list(skip=skip, limit=limit, search=search)

@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: str,
    staff: StaffUpdate,
    db: Session = Depends(get_db)
):
    service = StaffService(db)
    try:
        updated_staff = service.update_staff(staff_id, staff)
        if not updated_staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        return updated_staff
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{staff_id}")
def delete_staff(
    staff_id: str,
    db: Session = Depends(get_db)
):
    service = StaffService(db)
    success = service.delete_staff(staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff deleted successfully"}
