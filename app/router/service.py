from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..service.service_service import ServiceService
from ..dto.service import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Create a new service"""
    try:
        service_service = ServiceService(db)
        return service_service.create_service(service)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: str, db: Session = Depends(get_db)):
    """Get a service by ID"""
    service_service = ServiceService(db)
    service = service_service.get_service(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.get("/", response_model=List[ServiceResponse])
def get_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get a list of services with optional search and pagination"""
    service_service = ServiceService(db)
    return service_service.get_service_list(skip=skip, limit=limit, search=search)

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: str, service: ServiceUpdate, db: Session = Depends(get_db)):
    """Update a service"""
    try:
        service_service = ServiceService(db)
        updated_service = service_service.update_service(service_id, service)
        if not updated_service:
            raise HTTPException(status_code=404, detail="Service not found")
        return updated_service
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/{service_id}")
def delete_service(service_id: str, db: Session = Depends(get_db)):
    """Delete a service"""
    service_service = ServiceService(db)
    success = service_service.delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

@router.get("/barcode/{barcode}", response_model=ServiceResponse)
def get_service_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """Get a service by barcode"""
    service_service = ServiceService(db)
    service = service_service.get_service_by_barcode(barcode)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.get("/category/{category_id}", response_model=List[ServiceResponse])
def get_services_by_category(category_id: str, db: Session = Depends(get_db)):
    """Get all services in a specific category"""
    service_service = ServiceService(db)
    return service_service.get_services_by_category(category_id)

@router.get("/department/{department_id}", response_model=List[ServiceResponse])
def get_services_by_department(department_id: str, db: Session = Depends(get_db)):
    """Get all services in a specific department"""
    service_service = ServiceService(db)
    return service_service.get_services_by_department(department_id)
