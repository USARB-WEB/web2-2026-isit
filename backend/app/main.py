from typing import Any

from fastapi import FastAPI
from fastapi.openapi.constants import METHODS_WITH_BODY
from fastapi.openapi.utils import get_openapi

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.order_products import router as order_products_router
from app.api.v1.routes.orders import router as orders_router
from app.api.v1.routes.product_categories import router as product_categories_router
from app.api.v1.routes.products import router as products_router
from app.core.config import settings

# The HTTP QUERY method (RFC 9110 style: safe, idempotent, but with a request body)
# is newer than the defaults FastAPI ships with, so two things need a nudge:
# 1. FastAPI only documents a requestBody for methods it knows can carry one.
METHODS_WITH_BODY.add("QUERY")
# 2. "query" only became a valid path item method in OpenAPI 3.2, and Swagger UI
#    silently hides operations whose method it does not recognise.
OPENAPI_VERSION = "3.2.0"


def build_openapi(app: FastAPI) -> dict[str, Any]:
    if app.openapi_schema is not None:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=OPENAPI_VERSION,
        routes=app.routes,
    )
    app.openapi_schema = schema
    return schema


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )
    app.include_router(health_router, prefix=settings.api_v1_prefix)
    app.include_router(products_router, prefix=settings.api_v1_prefix)
    app.include_router(product_categories_router, prefix=settings.api_v1_prefix)
    app.include_router(orders_router, prefix=settings.api_v1_prefix)
    app.include_router(order_products_router, prefix=settings.api_v1_prefix)
    app.openapi = lambda: build_openapi(app)
    return app


app = create_app()
