from typing import List, Optional
from sqlalchemy.orm import Session
from ..dao.customer import CustomerDAO
from ..dto.customer import CustomerCreate, CustomerUpdate, CustomerResponse

class CustomerService:
    def __init__(self, db: Session):
        self.customer_dao = CustomerDAO(db)

    def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        # Check if email already exists
        if customer.email:
            existing_customer = self.customer_dao.get_by_email(customer.email)
            if existing_customer:
                raise ValueError("Customer with this email already exists")
        
        # Check if mobile number already exists
        if customer.mobile_number:
            existing_customer = self.customer_dao.get_by_mobile_number(customer.mobile_number)
            if existing_customer:
                raise ValueError("Customer with this mobile number already exists")
        
        db_customer = self.customer_dao.create(customer)
        return self._to_response(db_customer)

    def get_customer(self, customer_id: str) -> Optional[CustomerResponse]:
        db_customer = self.customer_dao.get_by_id(customer_id)
        if not db_customer:
            return None
        return self._to_response(db_customer)

    def get_customer_list(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[CustomerResponse]:
        db_customers = self.customer_dao.get_all(skip=skip, limit=limit, search=search)
        return [self._to_response(customer) for customer in db_customers]

    def update_customer(self, customer_id: str, customer: CustomerUpdate) -> Optional[CustomerResponse]:
        # Check if email already exists for another customer
        if customer.email:
            existing_customer = self.customer_dao.get_by_email(customer.email)
            if existing_customer and existing_customer.id != customer_id:
                raise ValueError("Customer with this email already exists")
        
        # Check if mobile number already exists for another customer
        if customer.mobile_number:
            existing_customer = self.customer_dao.get_by_mobile_number(customer.mobile_number)
            if existing_customer and existing_customer.id != customer_id:
                raise ValueError("Customer with this mobile number already exists")
        
        db_customer = self.customer_dao.update(customer_id, customer)
        if not db_customer:
            return None
        return self._to_response(db_customer)

    def delete_customer(self, customer_id: str) -> bool:
        return self.customer_dao.delete(customer_id)

    def search_customers(self, search_term: str) -> List[CustomerResponse]:
        db_customers = self.customer_dao.search_customers(search_term)
        return [self._to_response(customer) for customer in db_customers]

    def get_customers_by_company(self, company_name: str) -> List[CustomerResponse]:
        db_customers = self.customer_dao.get_by_company(company_name)
        return [self._to_response(customer) for customer in db_customers]

    def _to_response(self, db_customer) -> CustomerResponse:
        return CustomerResponse(
            id=db_customer.id,
            title=db_customer.title,
            first_name=db_customer.first_name,
            middle_name=db_customer.middle_name,
            last_name=db_customer.last_name,
            company_name=db_customer.company_name,
            gender=db_customer.gender,
            date_of_birth=db_customer.date_of_birth,
            address=db_customer.address,
            state_region=db_customer.state_region,
            country=db_customer.country,
            mobile_number=db_customer.mobile_number,
            phone_number=db_customer.phone_number,
            email=db_customer.email,
            website=db_customer.website,
            created_at=db_customer.created_at if db_customer.created_at else None,
            updated_at=db_customer.updated_at if db_customer.updated_at else None
        )
