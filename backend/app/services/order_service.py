from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories.order_product_repository import OrderProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate, OrderRead, OrderSummary, OrderUpdate
from app.schemas.order_product import OrderProductRead


class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        order_product_repository: OrderProductRepository,
        product_repository: ProductRepository,
    ) -> None:
        self._repository = repository
        self._order_product_repository = order_product_repository
        self._product_repository = product_repository

    def _ensure_product_exists(self, product_id: int) -> None:
        if self._product_repository.get(product_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found",
            )

    def _compute_totals(self, order_products) -> tuple[int, float]:
        products_count = sum(order_product.quantity for order_product in order_products)
        total_sum = 0.0
        for order_product in order_products:
            product = self._product_repository.get(order_product.product_id)
            if product is not None and product.price is not None:
                total_sum += float(product.price) * order_product.quantity
        return products_count, round(total_sum, 2)

    def _build_order_read(self, order, order_products=None) -> OrderRead:
        if order_products is None:
            order_products = self._order_product_repository.list_by_order(order.id)

        products_count, total_sum = self._compute_totals(order_products)

        return OrderRead(
            id=order.id,
            client_name=order.client_name,
            products=[OrderProductRead.model_validate(order_product) for order_product in order_products],
            products_count=products_count,
            total_sum=total_sum,
        )

    def _build_order_summary(self, order) -> OrderSummary:
        order_products = self._order_product_repository.list_by_order(order.id)
        products_count, total_sum = self._compute_totals(order_products)

        return OrderSummary(
            id=order.id,
            client_name=order.client_name,
            products_count=products_count,
            total_sum=total_sum,
        )

    def list_orders(self) -> list[OrderSummary]:
        return [self._build_order_summary(order) for order in self._repository.list()]

    def get_order(self, order_id: int) -> OrderRead:
        order = self._repository.get(order_id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return self._build_order_read(order)

    def create_order(self, payload: OrderCreate) -> OrderRead:
        for item in payload.products:
            self._ensure_product_exists(item.product_id)

        order = self._repository.create({"client_name": payload.client_name})
        order_products = [
            self._order_product_repository.create(order.id, item.model_dump())
            for item in payload.products
        ]
        return self._build_order_read(order, order_products=order_products)

    def update_order(self, order_id: int, payload: OrderUpdate) -> OrderRead:
        order = self._repository.update(order_id, payload.model_dump())
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return self._build_order_read(order)

    def delete_order(self, order_id: int) -> None:
        try:
            deleted = self._repository.delete(order_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete this order because it is still referenced by other records.",
            )
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
