from typing import List, Optional
from sqlalchemy.orm import Session
from app.dao.category import CategoryDAO
from app.dto.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.models.category import Category

class CategoryService:
    def __init__(self, db: Session):
        self.category_dao = CategoryDAO(db)

    def get_category(self, category_id: str) -> Optional[CategoryResponse]:
        category = self.category_dao.get_category(category_id)
        if category:
            return CategoryResponse.model_validate(category)
        return None

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[CategoryResponse]:
        categories = self.category_dao.get_categories(skip, limit)
        return [CategoryResponse.model_validate(category) for category in categories]

    def create_category(self, category: CategoryCreate) -> CategoryResponse:
        category_data = category.model_dump()
        created_category = self.category_dao.create_category(category_data)
        return CategoryResponse.model_validate(created_category)

    def update_category(self, category_id: str, category: CategoryUpdate) -> Optional[CategoryResponse]:
        category_data = category.model_dump(exclude_unset=True)
        updated_category = self.category_dao.update_category(category_id, category_data)
        if updated_category:
            return CategoryResponse.model_validate(updated_category)
        return None

    def delete_category(self, category_id: str) -> bool:
        return self.category_dao.delete_category(category_id)

    def search_categories(self, query: str) -> List[CategoryResponse]:
        categories = self.category_dao.search_categories(query)
        return [CategoryResponse.model_validate(category) for category in categories] 