from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.product import Product


class ProductRepository:
    """SQLAlchemy-backed persistence for products."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self) -> list[Product]:
        return list(self._db.query(Product).all())

    def get(self, product_id: int) -> Product | None:
        return self._db.get(Product, product_id)

    def create(self, data: dict[str, object]) -> Product:
        product = Product(**data)
        self._db.add(product)
        self._db.commit()
        self._db.refresh(product)
        return product

    def update(self, product_id: int, data: dict[str, object]) -> Product | None:
        product = self.get(product_id)
        if product is None:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        self._db.commit()
        self._db.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get(product_id)
        if product is None:
            return False
        self._db.delete(product)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        return True
