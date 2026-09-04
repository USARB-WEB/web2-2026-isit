from fastapi import APIRouter, Depends, status

from app.api.v1.dependencies.products import get_product_service
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def get_products(service: ProductService = Depends(get_product_service)) -> list[ProductRead]:
    return service.get_products()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)) -> ProductRead:
    return service.get_product(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    return service.create_product(payload)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    return service.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_product_service)) -> None:
    service.delete_product(product_id)
