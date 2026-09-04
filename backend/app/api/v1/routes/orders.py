from fastapi import APIRouter, Depends

from app.api.v1.dependencies.orders import get_order_controller
from app.controllers.order_controller import OrderController
from app.schemas.order import OrderCreate, OrderRead, OrderSummary, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderSummary])
def list_orders(
    controller: OrderController = Depends(get_order_controller),
) -> list[OrderSummary]:
    return controller.list_orders()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    controller: OrderController = Depends(get_order_controller),
) -> OrderRead:
    return controller.get_order(order_id)


@router.post("", response_model=OrderRead, status_code=201)
def create_order(
    payload: OrderCreate,
    controller: OrderController = Depends(get_order_controller),
) -> OrderRead:
    return controller.create_order(payload)


@router.put("/{order_id}", response_model=OrderRead)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    controller: OrderController = Depends(get_order_controller),
) -> OrderRead:
    return controller.update_order(order_id, payload)


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    controller: OrderController = Depends(get_order_controller),
):
    return controller.delete_order(order_id)
