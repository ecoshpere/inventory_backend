from sqlalchemy.orm import Session
from app.dao.stock_movement import StockMovementDAO
from app.dto.stock_movement import StockMovementCreate, StockMovementUpdate, StockMovementResponse
from typing import List, Optional

class StockMovementService:
    def __init__(self, db: Session):
        self.dao = StockMovementDAO(db)

    def create_stock_movement(self, stock_movement: StockMovementCreate) -> StockMovementResponse:
        # Check if movement number already exists
        existing_movement = self.dao.get_by_movement_number(stock_movement.movement_number)
        if existing_movement:
            raise ValueError(f"Stock movement with number {stock_movement.movement_number} already exists")
        
        # Validate that source and destination warehouses are different
        if stock_movement.source_warehouse_id == stock_movement.destination_warehouse_id:
            raise ValueError("Source and destination warehouses must be different")
        
        # Check source warehouse availability
        if not self.dao.check_source_warehouse_availability(
            stock_movement.product_id,
            stock_movement.source_warehouse_id,
            stock_movement.quantity
        ):
            raise ValueError("Insufficient quantity in source warehouse")
        
        db_stock_movement = self.dao.create(stock_movement)
        return StockMovementResponse.from_orm(db_stock_movement)

    def get_stock_movement(self, stock_movement_id: str) -> Optional[StockMovementResponse]:
        db_stock_movement = self.dao.get_by_id(stock_movement_id)
        if db_stock_movement:
            return StockMovementResponse.from_orm(db_stock_movement)
        return None

    def get_stock_movements(self, skip: int = 0, limit: int = 100) -> List[StockMovementResponse]:
        db_stock_movements = self.dao.get_all(skip=skip, limit=limit)
        return [StockMovementResponse.from_orm(movement) for movement in db_stock_movements]

    def get_active_stock_movements(self) -> List[StockMovementResponse]:
        db_stock_movements = self.dao.get_active()
        return [StockMovementResponse.from_orm(movement) for movement in db_stock_movements]

    def update_stock_movement(self, stock_movement_id: str, stock_movement: StockMovementUpdate) -> Optional[StockMovementResponse]:
        # If updating movement number, check if it already exists
        if stock_movement.movement_number:
            existing_movement = self.dao.get_by_movement_number(stock_movement.movement_number)
            if existing_movement and existing_movement.id != stock_movement_id:
                raise ValueError(f"Stock movement with number {stock_movement.movement_number} already exists")
        
        # If updating quantity, check source warehouse availability
        if stock_movement.quantity:
            current_movement = self.dao.get_by_id(stock_movement_id)
            if current_movement:
                source_warehouse_id = stock_movement.source_warehouse_id or current_movement.source_warehouse_id
                product_id = stock_movement.product_id or current_movement.product_id
                
                if not self.dao.check_source_warehouse_availability(
                    product_id,
                    source_warehouse_id,
                    stock_movement.quantity
                ):
                    raise ValueError("Insufficient quantity in source warehouse")
        
        db_stock_movement = self.dao.update(stock_movement_id, stock_movement)
        if db_stock_movement:
            return StockMovementResponse.from_orm(db_stock_movement)
        return None

    def delete_stock_movement(self, stock_movement_id: str) -> bool:
        return self.dao.soft_delete(stock_movement_id)

    def update_stock_movement_status(self, stock_movement_id: str, status: str) -> Optional[StockMovementResponse]:
        # Validate status
        valid_statuses = ["Draft", "Completed", "Cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        db_stock_movement = self.dao.update_status(stock_movement_id, status)
        if db_stock_movement:
            return StockMovementResponse.from_orm(db_stock_movement)
        return None

    def execute_stock_movement(self, stock_movement_id: str) -> bool:
        """Execute a stock movement (move from Draft to Completed)"""
        try:
            success = self.dao.execute_movement(stock_movement_id)
            if not success:
                raise ValueError("Failed to execute stock movement. Check if movement exists and is in Draft status.")
            return success
        except Exception as e:
            raise ValueError(f"Failed to execute stock movement: {str(e)}")

    def check_warehouse_availability(self, product_id: str, warehouse_id: str, quantity: float) -> bool:
        """Check if a warehouse has sufficient quantity of a product"""
        return self.dao.check_source_warehouse_availability(product_id, warehouse_id, quantity) 