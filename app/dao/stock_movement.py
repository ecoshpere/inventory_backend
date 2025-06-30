from sqlalchemy.orm import Session
from app.models.stock_movement import StockMovement
from app.models.inventory import Inventory
from app.dto.stock_movement import StockMovementCreate, StockMovementUpdate
from typing import List, Optional

class StockMovementDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, stock_movement: StockMovementCreate) -> StockMovement:
        db_stock_movement = StockMovement(**stock_movement.dict())
        self.db.add(db_stock_movement)
        self.db.commit()
        self.db.refresh(db_stock_movement)
        return db_stock_movement

    def get_by_id(self, stock_movement_id: str) -> Optional[StockMovement]:
        return self.db.query(StockMovement).filter(StockMovement.id == stock_movement_id).first()

    def get_by_movement_number(self, movement_number: str) -> Optional[StockMovement]:
        return self.db.query(StockMovement).filter(StockMovement.movement_number == movement_number).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[StockMovement]:
        return self.db.query(StockMovement).offset(skip).limit(limit).all()

    def get_active(self) -> List[StockMovement]:
        return self.db.query(StockMovement).filter(StockMovement.is_active == True).all()

    def update(self, stock_movement_id: str, stock_movement: StockMovementUpdate) -> Optional[StockMovement]:
        db_stock_movement = self.get_by_id(stock_movement_id)
        if db_stock_movement:
            update_data = stock_movement.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_stock_movement, field, value)
            self.db.commit()
            self.db.refresh(db_stock_movement)
        return db_stock_movement

    def delete(self, stock_movement_id: str) -> bool:
        db_stock_movement = self.get_by_id(stock_movement_id)
        if db_stock_movement:
            self.db.delete(db_stock_movement)
            self.db.commit()
            return True
        return False

    def soft_delete(self, stock_movement_id: str) -> bool:
        db_stock_movement = self.get_by_id(stock_movement_id)
        if db_stock_movement:
            db_stock_movement.is_active = False
            self.db.commit()
            return True
        return False

    def update_status(self, stock_movement_id: str, status: str) -> Optional[StockMovement]:
        db_stock_movement = self.get_by_id(stock_movement_id)
        if db_stock_movement:
            db_stock_movement.status = status
            self.db.commit()
            self.db.refresh(db_stock_movement)
        return db_stock_movement

    def check_source_warehouse_availability(self, product_id: str, source_warehouse_id: str, quantity: float) -> bool:
        """Check if source warehouse has sufficient quantity"""
        inventory = self.db.query(Inventory).filter(
            Inventory.product_id == product_id,
            Inventory.warehouse_id == source_warehouse_id
        ).first()
        
        if not inventory:
            return False
        
        return inventory.quantity >= quantity

    def execute_movement(self, stock_movement_id: str) -> bool:
        """Execute the stock movement by updating inventory"""
        db_stock_movement = self.get_by_id(stock_movement_id)
        if not db_stock_movement or db_stock_movement.status != "Draft":
            return False

        # Check source warehouse availability
        if not self.check_source_warehouse_availability(
            db_stock_movement.product_id,
            db_stock_movement.source_warehouse_id,
            db_stock_movement.quantity
        ):
            return False

        # Deduct from source warehouse
        source_inventory = self.db.query(Inventory).filter(
            Inventory.product_id == db_stock_movement.product_id,
            Inventory.warehouse_id == db_stock_movement.source_warehouse_id
        ).first()
        
        if source_inventory:
            source_inventory.quantity -= db_stock_movement.quantity

        # Add to destination warehouse
        dest_inventory = self.db.query(Inventory).filter(
            Inventory.product_id == db_stock_movement.product_id,
            Inventory.warehouse_id == db_stock_movement.destination_warehouse_id
        ).first()
        
        if dest_inventory:
            dest_inventory.quantity += db_stock_movement.quantity
        else:
            # Create new inventory record for destination warehouse
            dest_inventory = Inventory(
                product_id=db_stock_movement.product_id,
                warehouse_id=db_stock_movement.destination_warehouse_id,
                quantity=db_stock_movement.quantity
            )
            self.db.add(dest_inventory)

        # Update movement status
        db_stock_movement.status = "Completed"
        
        self.db.commit()
        return True 