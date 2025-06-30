from sqlalchemy.orm import Session
from app.models.product import Product
from typing import List, Optional

class ProductDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product_id: str, product_data: dict) -> Optional[Product]:
        product = self.get_product(product_id)
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete_product(self, product_id: str) -> bool:
        product = self.get_product(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

    def get_products_by_category(self, category_id: str) -> List[Product]:
        return self.db.query(Product).filter(Product.category_id == category_id).all()

    def search_products(self, query: str) -> List[Product]:
        return self.db.query(Product).filter(
            (Product.name.ilike(f"%{query}%")) | 
            (Product.sku.ilike(f"%{query}%"))
        ).all() 