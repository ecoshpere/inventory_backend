from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.service.product_service import ProductService
from app.dto.product import ProductCreate, ProductUpdate, ProductResponse
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_products(skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.create_product(product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: ProductUpdate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    updated_product = product_service.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    success = product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.get("/category/{category_id}", response_model=List[ProductResponse])
def get_products_by_category(category_id: str, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_products_by_category(category_id)

@router.get("/search/{query}", response_model=List[ProductResponse])
def search_products(query: str, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.search_products(query) 