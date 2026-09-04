from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.order_product import OrderProduct


class OrderProductRepository:
    """SQLAlchemy-backed persistence for order products."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def list_by_order(self, order_id: int) -> list[OrderProduct]:
        return list(self._db.query(OrderProduct).filter(OrderProduct.order_id == order_id).all())

    def get(self, order_id: int, order_product_id: int) -> OrderProduct | None:
        order_product = self._db.get(OrderProduct, order_product_id)
        if order_product is None or order_product.order_id != order_id:
            return None
        return order_product

    def create(self, order_id: int, data: dict[str, object]) -> OrderProduct:
        order_product = OrderProduct(order_id=order_id, **data)
        self._db.add(order_product)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        self._db.refresh(order_product)
        return order_product

    def update(self, order_id: int, order_product_id: int, data: dict[str, object]) -> OrderProduct | None:
        order_product = self.get(order_id, order_product_id)
        if order_product is None:
            return None
        for key, value in data.items():
            setattr(order_product, key, value)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        self._db.refresh(order_product)
        return order_product

    def delete(self, order_id: int, order_product_id: int) -> bool:
        order_product = self.get(order_id, order_product_id)
        if order_product is None:
            return False
        self._db.delete(order_product)
        self._db.commit()
        return True
