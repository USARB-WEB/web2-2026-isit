from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.product_category import ProductCategory


class ProductCategoryRepository:
    """SQLAlchemy-backed persistence for product categories."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self) -> list[ProductCategory]:
        return list(self._db.query(ProductCategory).all())

    def get(self, category_id: int) -> ProductCategory | None:
        return self._db.get(ProductCategory, category_id)

    def create(self, data: dict[str, object]) -> ProductCategory:
        category = ProductCategory(**data)
        self._db.add(category)
        self._db.commit()
        self._db.refresh(category)
        return category

    def update(self, category_id: int, data: dict[str, object]) -> ProductCategory | None:
        category = self.get(category_id)
        if category is None:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        self._db.commit()
        self._db.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get(category_id)
        if category is None:
            return False
        self._db.delete(category)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise
        return True
