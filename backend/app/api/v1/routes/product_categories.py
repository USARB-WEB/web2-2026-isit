from fastapi import APIRouter, Depends

from app.api.v1.dependencies.product_categories import get_product_category_controller
from app.controllers.product_category_controller import ProductCategoryController
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)

router = APIRouter(prefix="/product-categories", tags=["product-categories"])


@router.get("", response_model=list[ProductCategoryRead])
def list_product_categories(
    controller: ProductCategoryController = Depends(get_product_category_controller),
) -> list[ProductCategoryRead]:
    return controller.list_categories()


@router.get("/{category_id}", response_model=ProductCategoryRead)
def get_product_category(
    category_id: int,
    controller: ProductCategoryController = Depends(get_product_category_controller),
) -> ProductCategoryRead:
    return controller.get_category(category_id)


@router.post("", response_model=ProductCategoryRead, status_code=201)
def create_product_category(
    payload: ProductCategoryCreate,
    controller: ProductCategoryController = Depends(get_product_category_controller),
) -> ProductCategoryRead:
    return controller.create_category(payload)


@router.put("/{category_id}", response_model=ProductCategoryRead)
def update_product_category(
    category_id: int,
    payload: ProductCategoryUpdate,
    controller: ProductCategoryController = Depends(get_product_category_controller),
) -> ProductCategoryRead:
    return controller.update_category(category_id, payload)


@router.delete("/{category_id}", status_code=204)
def delete_product_category(
    category_id: int,
    controller: ProductCategoryController = Depends(get_product_category_controller),
):
    return controller.delete_category(category_id)
