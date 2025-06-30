from typing import List, Optional
from sqlalchemy.orm import Session
from app.dao.product import ProductDAO
from app.dto.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product

class ProductService:
    def __init__(self, db: Session):
        self.product_dao = ProductDAO(db)

    def get_product(self, product_id: int) -> Optional[ProductResponse]:
        product = self.product_dao.get_product(product_id)
        if product:
            return ProductResponse.model_validate(product)
        return None

    def get_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        products = self.product_dao.get_products(skip, limit)
        return [ProductResponse.model_validate(product) for product in products]

    def create_product(self, product: ProductCreate) -> ProductResponse:
        product_data = product.model_dump()
        created_product = self.product_dao.create_product(product_data)
        return ProductResponse.model_validate(created_product)

    def update_product(self, product_id: int, product: ProductUpdate) -> Optional[ProductResponse]:
        product_data = product.model_dump(exclude_unset=True)
        updated_product = self.product_dao.update_product(product_id, product_data)
        if updated_product:
            return ProductResponse.model_validate(updated_product)
        return None

    def delete_product(self, product_id: int) -> bool:
        return self.product_dao.delete_product(product_id)

    def get_products_by_category(self, category_id: int) -> List[ProductResponse]:
        products = self.product_dao.get_products_by_category(category_id)
        return [ProductResponse.model_validate(product) for product in products]

    def search_products(self, query: str) -> List[ProductResponse]:
        products = self.product_dao.search_products(query)
        return [ProductResponse.model_validate(product) for product in products] 