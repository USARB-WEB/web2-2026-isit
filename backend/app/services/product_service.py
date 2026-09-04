from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories.product_category_repository import ProductCategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


class ProductService:
    def __init__(
        self,
        repository: ProductRepository,
        category_repository: ProductCategoryRepository,
    ) -> None:
        self._repository = repository
        self._category_repository = category_repository

    def _ensure_category_exists(self, category_id: int) -> None:
        if self._category_repository.get(category_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product category {category_id} not found",
            )

    def get_products(self) -> list[ProductRead]:
        return [ProductRead.model_validate(product) for product in self._repository.list()]

    def get_product(self, product_id: int) -> ProductRead:
        product = self._repository.get(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductRead.model_validate(product)

    def create_product(self, payload: ProductCreate) -> ProductRead:
        self._ensure_category_exists(payload.category_id)
        product = self._repository.create(payload.model_dump())
        return ProductRead.model_validate(product)

    def update_product(self, product_id: int, payload: ProductUpdate) -> ProductRead:
        self._ensure_category_exists(payload.category_id)
        product = self._repository.update(product_id, payload.model_dump())
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductRead.model_validate(product)

    def delete_product(self, product_id: int) -> None:
        try:
            deleted = self._repository.delete(product_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete this product because it is used by one or more orders.",
            )
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
