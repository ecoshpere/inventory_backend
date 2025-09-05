from sqlalchemy.orm import Session
from typing import List, Optional
from ..dao.service import ServiceDAO
from ..dto.service import ServiceCreate, ServiceUpdate, ServiceResponse

class ServiceService:
    def __init__(self, db: Session):
        self.dao = ServiceDAO(db)

    def create_service(self, service: ServiceCreate) -> ServiceResponse:
        # Validate price is positive
        if service.price <= 0:
            raise ValueError("Price must be greater than zero")
        
        # Validate status is valid
        valid_statuses = ["Active", "Inactive", "Discontinued"]
        if service.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        db_service = self.dao.create(service)
        return self._to_response(db_service)

    def get_service(self, service_id: str) -> Optional[ServiceResponse]:
        db_service = self.dao.get_by_id(service_id)
        if db_service:
            return self._to_response(db_service)
        return None

    def get_service_list(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[ServiceResponse]:
        db_services = self.dao.get_all(skip=skip, limit=limit, search=search)
        return [self._to_response(service) for service in db_services]

    def update_service(self, service_id: str, service: ServiceUpdate) -> Optional[ServiceResponse]:
        # Validate price if being updated
        if service.price is not None and service.price <= 0:
            raise ValueError("Price must be greater than zero")
        
        # Validate status if being updated
        if service.status is not None:
            valid_statuses = ["Active", "Inactive", "Discontinued"]
            if service.status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        db_service = self.dao.update(service_id, service)
        if db_service:
            return self._to_response(db_service)
        return None

    def delete_service(self, service_id: str) -> bool:
        return self.dao.delete(service_id)

    def get_service_by_barcode(self, barcode: str) -> Optional[ServiceResponse]:
        db_service = self.dao.get_by_barcode(barcode)
        if db_service:
            return self._to_response(db_service)
        return None

    def get_services_by_category(self, category_id: str) -> List[ServiceResponse]:
        db_services = self.dao.get_by_category(category_id)
        return [self._to_response(service) for service in db_services]

    def get_services_by_department(self, department_id: str) -> List[ServiceResponse]:
        db_services = self.dao.get_by_department(department_id)
        return [self._to_response(service) for service in db_services]

    def _to_response(self, db_service) -> ServiceResponse:
        return ServiceResponse(
            id=db_service.id,
            name=db_service.name,
            description=db_service.description,
            price=db_service.price,
            category_id=db_service.category_id,
            department_id=db_service.department_id,
            image_thumbnail=db_service.image_thumbnail,
            status=db_service.status,
            barcode=db_service.barcode,
            category_name=db_service.category.name if db_service.category else None,
            department_name=db_service.department.name if db_service.department else None,
            created_at=db_service.created_at if db_service.created_at else None,
            updated_at=db_service.updated_at if db_service.updated_at else None
        )
