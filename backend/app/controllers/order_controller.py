from fastapi import Response, status

from app.schemas.order import OrderCreate, OrderRead, OrderSummary, OrderUpdate
from app.services.order_service import OrderService


class OrderController:
    def __init__(self, service: OrderService) -> None:
        self._service = service

    def list_orders(self) -> list[OrderSummary]:
        return self._service.list_orders()

    def get_order(self, order_id: int) -> OrderRead:
        return self._service.get_order(order_id)

    def create_order(self, payload: OrderCreate) -> OrderRead:
        return self._service.create_order(payload)

    def update_order(self, order_id: int, payload: OrderUpdate) -> OrderRead:
        return self._service.update_order(order_id, payload)

    def delete_order(self, order_id: int) -> Response:
        self._service.delete_order(order_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
