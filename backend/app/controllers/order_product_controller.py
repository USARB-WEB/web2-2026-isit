from fastapi import Response, status

from app.schemas.order_product import OrderProductCreate, OrderProductRead, OrderProductUpdate
from app.services.order_product_service import OrderProductService


class OrderProductController:
    def __init__(self, service: OrderProductService) -> None:
        self._service = service

    def list_order_products(self, order_id: int) -> list[OrderProductRead]:
        return self._service.list_order_products(order_id)

    def get_order_product(self, order_id: int, order_product_id: int) -> OrderProductRead:
        return self._service.get_order_product(order_id, order_product_id)

    def add_order_product(self, order_id: int, payload: OrderProductCreate) -> OrderProductRead:
        return self._service.add_order_product(order_id, payload)

    def update_order_product(
        self, order_id: int, order_product_id: int, payload: OrderProductUpdate
    ) -> OrderProductRead:
        return self._service.update_order_product(order_id, order_product_id, payload)

    def delete_order_product(self, order_id: int, order_product_id: int) -> Response:
        self._service.delete_order_product(order_id, order_product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
