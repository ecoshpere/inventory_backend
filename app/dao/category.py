from sqlalchemy.orm import Session
from app.models.category import Category
from typing import List, Optional

class CategoryDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_category(self, category_id: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.db.query(Category).offset(skip).limit(limit).all()

    def create_category(self, category_data: dict) -> Category:
        category = Category(**category_data)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: str, category_data: dict) -> Optional[Category]:
        category = self.get_category(category_id)
        if category:
            for key, value in category_data.items():
                setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
        return category

    def delete_category(self, category_id: str) -> bool:
        category = self.get_category(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False

    def search_categories(self, query: str) -> List[Category]:
        return self.db.query(Category).filter(
            Category.name.ilike(f"%{query}%")
        ).all() 