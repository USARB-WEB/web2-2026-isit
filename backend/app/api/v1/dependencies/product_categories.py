from app.controllers.product_category_controller import ProductCategoryController
from app.repositories.product_category_repository import ProductCategoryRepository
from app.services.product_category_service import ProductCategoryService

product_category_repository = ProductCategoryRepository()


def get_product_category_controller() -> ProductCategoryController:
    service = ProductCategoryService(repository=product_category_repository)
    return ProductCategoryController(service=service)
