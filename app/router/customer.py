from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..service.customer_service import CustomerService
from ..dto.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    try:
        customer_service = CustomerService(db)
        return customer_service.create_customer(customer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get a customer by ID"""
    customer_service = CustomerService(db)
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all customers with optional search"""
    customer_service = CustomerService(db)
    return customer_service.get_customer_list(skip=skip, limit=limit, search=search)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: str, 
    customer: CustomerUpdate, 
    db: Session = Depends(get_db)
):
    """Update a customer"""
    try:
        customer_service = CustomerService(db)
        updated_customer = customer_service.update_customer(customer_id, customer)
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    """Delete a customer"""
    customer_service = CustomerService(db)
    success = customer_service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.get("/search/", response_model=List[CustomerResponse])
def search_customers(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Search customers by name, company, email, or phone"""
    customer_service = CustomerService(db)
    return customer_service.search_customers(query)

@router.get("/company/{company_name}", response_model=List[CustomerResponse])
def get_customers_by_company(company_name: str, db: Session = Depends(get_db)):
    """Get customers by company name"""
    customer_service = CustomerService(db)
    return customer_service.get_customers_by_company(company_name)
