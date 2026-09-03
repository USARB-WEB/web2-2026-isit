from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy


class ProductCategoryRepository:
    def __init__(self) -> None:
        self._categories: dict[int, dict[str, object]] = {}
        self._next_id = 1

    def list(self) -> list[dict[str, object]]:
        return [deepcopy(category) for category in self._categories.values()]

    def get(self, category_id: int) -> dict[str, object] | None:
        category = self._categories.get(category_id)
        if category is None:
            return None
        return deepcopy(category)

    def create(self, category_data: dict[str, object]) -> dict[str, object]:
        category = deepcopy(category_data)
        category["id"] = self._next_id
        self._categories[self._next_id] = category
        self._next_id += 1
        return deepcopy(category)

    def update(self, category_id: int, category_data: dict[str, object]) -> dict[str, object] | None:
        if category_id not in self._categories:
            return None
        category = deepcopy(category_data)
        category["id"] = category_id
        self._categories[category_id] = category
        return deepcopy(category)

    def delete(self, category_id: int) -> bool:
        if category_id not in self._categories:
            return False
        del self._categories[category_id]
        return True

    def replace_all(self, categories: Iterable[dict[str, object]]) -> None:
        self._categories = {int(category["id"]): deepcopy(category) for category in categories}
        self._next_id = max(self._categories, default=0) + 1
