from fastapi import Response, status

from app.dto.product_category import ProductCategoryCreateDTO, ProductCategoryUpdateDTO
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)
from app.services.product_category_service import ProductCategoryService


class ProductCategoryController:
    def __init__(self, service: ProductCategoryService) -> None:
        self._service = service

    def list_categories(self) -> list[ProductCategoryRead]:
        return self._service.list_categories()

    def get_category(self, category_id: int) -> ProductCategoryRead:
        return self._service.get_category(category_id)

    def create_category(self, payload: ProductCategoryCreate) -> ProductCategoryRead:
        return self._service.create_category(ProductCategoryCreateDTO.from_schema(payload))

    def update_category(self, category_id: int, payload: ProductCategoryUpdate) -> ProductCategoryRead:
        return self._service.update_category(category_id, ProductCategoryUpdateDTO.from_schema(payload))

    def delete_category(self, category_id: int) -> Response:
        self._service.delete_category(category_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
