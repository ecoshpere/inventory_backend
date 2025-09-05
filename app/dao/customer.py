from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..models.customer import Customer
from ..dto.customer import CustomerCreate, CustomerUpdate
import uuid
from datetime import datetime

class CustomerDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer: CustomerCreate) -> Customer:
        now = datetime.utcnow()
        db_customer = Customer(
            id=str(uuid.uuid4()),
            title=customer.title,
            first_name=customer.first_name,
            middle_name=customer.middle_name,
            last_name=customer.last_name,
            company_name=customer.company_name,
            gender=customer.gender,
            date_of_birth=customer.date_of_birth,
            address=customer.address,
            state_region=customer.state_region,
            country=customer.country,
            mobile_number=customer.mobile_number,
            phone_number=customer.phone_number,
            email=customer.email,
            website=customer.website,
            created_at=now,
            updated_at=now
        )
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Customer]:
        query = self.db.query(Customer)
        
        if search:
            search_filter = or_(
                Customer.first_name.ilike(f"%{search}%"),
                Customer.last_name.ilike(f"%{search}%"),
                Customer.company_name.ilike(f"%{search}%"),
                Customer.email.ilike(f"%{search}%"),
                Customer.mobile_number.ilike(f"%{search}%"),
                Customer.phone_number.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()

    def update(self, customer_id: str, customer: CustomerUpdate) -> Optional[Customer]:
        db_customer = self.get_by_id(customer_id)
        if not db_customer:
            return None
        
        update_data = customer.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        db_customer.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def delete(self, customer_id: str) -> bool:
        db_customer = self.get_by_id(customer_id)
        if not db_customer:
            return False
        
        self.db.delete(db_customer)
        self.db.commit()
        return True

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.email == email).first()

    def get_by_mobile_number(self, mobile_number: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.mobile_number == mobile_number).first()

    def get_by_company(self, company_name: str) -> List[Customer]:
        return self.db.query(Customer).filter(
            Customer.company_name.ilike(f"%{company_name}%")
        ).all()

    def search_customers(self, search_term: str) -> List[Customer]:
        """Search customers by name, company, email, or phone"""
        return self.db.query(Customer).filter(
            or_(
                Customer.first_name.ilike(f"%{search_term}%"),
                Customer.last_name.ilike(f"%{search_term}%"),
                Customer.company_name.ilike(f"%{search_term}%"),
                Customer.email.ilike(f"%{search_term}%"),
                Customer.mobile_number.ilike(f"%{search_term}%"),
                Customer.phone_number.ilike(f"%{search_term}%")
            )
        ).all()
