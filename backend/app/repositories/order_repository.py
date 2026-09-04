from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.order import Order


class OrderRepository:
    """SQLAlchemy-backed persistence for orders."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self) -> list[Order]:
        return list(self._db.query(Order).all())

    def get(self, order_id: int) -> Order | None:
        return self._db.get(Order, order_id)

    def create(self, data: dict[str, object]) -> Order:
        order = Order(**data)
        self._db.add(order)
        self._db.commit()
        self._db.refresh(order)
        return order

    def update(self, order_id: int, data: dict[str, object]) -> Order | None:
        order = self.get(order_id)
        if order is None:
            return None
        for key, value in data.items():
            setattr(order, key, value)
        self._db.commit()
        self._db.refresh(order)
        return order

    def delete(self, order_id: int) -> bool:
        order = self.get(order_id)
        if order is None:
            return False
        self._db.delete(order)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        return True
