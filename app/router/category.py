from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.service.category_service import CategoryService
from app.dto.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_categories(skip, limit)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    category = category_service.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    print("category", category  )
    category_service = CategoryService(db)
    return category_service.create_category(category)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, category: CategoryUpdate, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    updated_category = category_service.update_category(category_id, category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}")
def delete_category(category_id: str, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    success = category_service.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

@router.get("/search/{query}", response_model=List[CategoryResponse])
def search_categories(query: str, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.search_categories(query) 