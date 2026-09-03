from __future__ import annotations

from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def get_products(self) -> list[ProductRead]:
        return [ProductRead.model_validate(product) for product in self._repository.list()]

    def get_products_with_prices(self) -> list[dict]:
        return [
            {**product.model_dump(), "price": float(product.price)}
            for product in self.get_products()
        ]

    def get_product(self, product_id: int) -> ProductRead:
        product = self._repository.get(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductRead.model_validate(product)

    def create_product(self, payload: ProductCreate) -> ProductRead:
        product = self._repository.create(payload.model_dump())
        return ProductRead.model_validate(product)

    def update_product(self, product_id: int, payload: ProductUpdate) -> ProductRead:
        product = self._repository.update(product_id, payload.model_dump())
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductRead.model_validate(product)

    def delete_product(self, product_id: int) -> None:
        deleted = self._repository.delete(product_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
