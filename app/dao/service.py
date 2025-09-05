from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional
import uuid
from datetime import datetime
from ..models.service import Service
from ..dto.service import ServiceCreate, ServiceUpdate

class ServiceDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, service: ServiceCreate) -> Service:
        # Generate barcode if not provided
        barcode = service.barcode
        if not barcode:
            barcode = f"SRV-{str(uuid.uuid4())[:8].upper()}"
        
        now = datetime.utcnow()
        db_service = Service(
            id=str(uuid.uuid4()),
            name=service.name,
            description=service.description,
            price=service.price,
            category_id=service.category_id,
            department_id=service.department_id,
            image_thumbnail=service.image_thumbnail,
            status=service.status,
            barcode=barcode,
            created_at=now,
            updated_at=now
        )
        self.db.add(db_service)
        self.db.commit()
        self.db.refresh(db_service)
        return db_service

    def get_by_id(self, service_id: str) -> Optional[Service]:
        return self.db.query(Service).options(
            joinedload(Service.category),
            joinedload(Service.department)
        ).filter(Service.id == service_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Service]:
        query = self.db.query(Service).options(
            joinedload(Service.category),
            joinedload(Service.department)
        )
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Service.name.ilike(search_term),
                    Service.description.ilike(search_term),
                    Service.barcode.ilike(search_term),
                    Service.status.ilike(search_term)
                )
            )
        
        return query.offset(skip).limit(limit).all()

    def update(self, service_id: str, service: ServiceUpdate) -> Optional[Service]:
        db_service = self.get_by_id(service_id)
        if not db_service:
            return None
        
        update_data = service.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_service, field, value)
        
        # Update the updated_at timestamp
        db_service.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_service)
        return db_service

    def delete(self, service_id: str) -> bool:
        db_service = self.get_by_id(service_id)
        if not db_service:
            return False
        
        self.db.delete(db_service)
        self.db.commit()
        return True

    def get_by_barcode(self, barcode: str) -> Optional[Service]:
        return self.db.query(Service).options(
            joinedload(Service.category),
            joinedload(Service.department)
        ).filter(Service.barcode == barcode).first()

    def get_by_category(self, category_id: str) -> List[Service]:
        return self.db.query(Service).options(
            joinedload(Service.category),
            joinedload(Service.department)
        ).filter(Service.category_id == category_id).all()

    def get_by_department(self, department_id: str) -> List[Service]:
        return self.db.query(Service).options(
            joinedload(Service.category),
            joinedload(Service.department)
        ).filter(Service.department_id == department_id).all()
