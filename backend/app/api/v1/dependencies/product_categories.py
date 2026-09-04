from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.product_category_controller import ProductCategoryController
from app.db.session import get_db
from app.repositories.product_category_repository import ProductCategoryRepository
from app.services.product_category_service import ProductCategoryService


def get_product_category_controller(db: Session = Depends(get_db)) -> ProductCategoryController:
    repository = ProductCategoryRepository(db=db)
    service = ProductCategoryService(repository=repository)
    return ProductCategoryController(service=service)
