from fastapi import APIRouter, Depends

from app.api.v1.dependencies.order_products import get_order_product_controller
from app.controllers.order_product_controller import OrderProductController
from app.schemas.order_product import OrderProductCreate, OrderProductRead, OrderProductUpdate

router = APIRouter(prefix="/orders/{order_id}/products", tags=["orders"])


@router.get("", response_model=list[OrderProductRead])
def list_order_products(
    order_id: int,
    controller: OrderProductController = Depends(get_order_product_controller),
) -> list[OrderProductRead]:
    return controller.list_order_products(order_id)


@router.get("/{order_product_id}", response_model=OrderProductRead)
def get_order_product(
    order_id: int,
    order_product_id: int,
    controller: OrderProductController = Depends(get_order_product_controller),
) -> OrderProductRead:
    return controller.get_order_product(order_id, order_product_id)


@router.post("", response_model=OrderProductRead, status_code=201)
def add_order_product(
    order_id: int,
    payload: OrderProductCreate,
    controller: OrderProductController = Depends(get_order_product_controller),
) -> OrderProductRead:
    return controller.add_order_product(order_id, payload)


@router.put("/{order_product_id}", response_model=OrderProductRead)
def update_order_product(
    order_id: int,
    order_product_id: int,
    payload: OrderProductUpdate,
    controller: OrderProductController = Depends(get_order_product_controller),
) -> OrderProductRead:
    return controller.update_order_product(order_id, order_product_id, payload)


@router.delete("/{order_product_id}", status_code=204)
def delete_order_product(
    order_id: int,
    order_product_id: int,
    controller: OrderProductController = Depends(get_order_product_controller),
):
    return controller.delete_order_product(order_id, order_product_id)
