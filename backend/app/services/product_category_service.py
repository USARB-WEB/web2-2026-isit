from __future__ import annotations

from fastapi import HTTPException, status

from app.repositories.product_category_repository import ProductCategoryRepository
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)


class ProductCategoryService:
    def __init__(self, repository: ProductCategoryRepository) -> None:
        self._repository = repository

    def list_categories(self) -> list[ProductCategoryRead]:
        return [ProductCategoryRead.model_validate(category) for category in self._repository.list()]

    def get_category(self, category_id: int) -> ProductCategoryRead:
        category = self._repository.get(category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product category not found")
        return ProductCategoryRead.model_validate(category)

    def create_category(self, payload: ProductCategoryCreate) -> ProductCategoryRead:
        category = self._repository.create(payload.model_dump())
        return ProductCategoryRead.model_validate(category)

    def update_category(self, category_id: int, payload: ProductCategoryUpdate) -> ProductCategoryRead:
        category = self._repository.update(category_id, payload.model_dump())
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product category not found")
        return ProductCategoryRead.model_validate(category)

    def delete_category(self, category_id: int) -> None:
        deleted = self._repository.delete(category_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product category not found")
