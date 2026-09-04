from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.order_product_controller import OrderProductController
from app.db.session import get_db
from app.repositories.order_product_repository import OrderProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.order_product_service import OrderProductService


def get_order_product_controller(db: Session = Depends(get_db)) -> OrderProductController:
    repository = OrderProductRepository(db=db)
    service = OrderProductService(
        repository=repository,
        order_repository=OrderRepository(db=db),
        product_repository=ProductRepository(db=db),
    )
    return OrderProductController(service=service)
