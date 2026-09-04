from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.order_controller import OrderController
from app.db.session import get_db
from app.repositories.order_product_repository import OrderProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.order_service import OrderService


def get_order_controller(db: Session = Depends(get_db)) -> OrderController:
    service = OrderService(
        repository=OrderRepository(db=db),
        order_product_repository=OrderProductRepository(db=db),
        product_repository=ProductRepository(db=db),
    )
    return OrderController(service=service)
