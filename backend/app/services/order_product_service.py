from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories.order_product_repository import OrderProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order_product import OrderProductCreate, OrderProductRead, OrderProductUpdate


class OrderProductService:
    def __init__(
        self,
        repository: OrderProductRepository,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
    ) -> None:
        self._repository = repository
        self._order_repository = order_repository
        self._product_repository = product_repository

    def _ensure_order_exists(self, order_id: int) -> None:
        if self._order_repository.get(order_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    def _ensure_product_exists(self, product_id: int) -> None:
        if self._product_repository.get(product_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found",
            )

    def list_order_products(self, order_id: int) -> list[OrderProductRead]:
        self._ensure_order_exists(order_id)
        return [
            OrderProductRead.model_validate(order_product)
            for order_product in self._repository.list_by_order(order_id)
        ]

    def get_order_product(self, order_id: int, order_product_id: int) -> OrderProductRead:
        self._ensure_order_exists(order_id)
        order_product = self._repository.get(order_id, order_product_id)
        if order_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order product not found")
        return OrderProductRead.model_validate(order_product)

    def add_order_product(self, order_id: int, payload: OrderProductCreate) -> OrderProductRead:
        self._ensure_order_exists(order_id)
        self._ensure_product_exists(payload.product_id)
        order_product = self._repository.create(order_id, payload.model_dump())
        return OrderProductRead.model_validate(order_product)

    def update_order_product(
        self, order_id: int, order_product_id: int, payload: OrderProductUpdate
    ) -> OrderProductRead:
        self._ensure_order_exists(order_id)
        self._ensure_product_exists(payload.product_id)
        order_product = self._repository.update(order_id, order_product_id, payload.model_dump())
        if order_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order product not found")
        return OrderProductRead.model_validate(order_product)

    def delete_order_product(self, order_id: int, order_product_id: int) -> None:
        self._ensure_order_exists(order_id)
        try:
            deleted = self._repository.delete(order_id, order_product_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete this order product because it is still referenced by other records.",
            )
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order product not found")
