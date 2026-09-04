from fastapi.testclient import TestClient

from app.db.models.order import Order
from app.db.models.order_product import OrderProduct
from app.db.models.product import Product
from app.db.models.product_category import ProductCategory
from app.tests.conftest import TestSessionLocal as SessionLocal
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    db = SessionLocal()
    try:
        db.query(OrderProduct).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(ProductCategory).delete()
        db.commit()
    finally:
        db.close()


def _create_category(name: str = "Electronics") -> int:
    response = client.post(
        "/api/v1/product-categories",
        json={"name": name, "description": "Test category"},
    )
    return response.json()["id"]


def test_create_product() -> None:
    category_id = _create_category()

    response = client.post(
        "/api/v1/products",
        json={"name": "Laptop", "description": "15-inch laptop", "price": 999.99, "category_id": category_id},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Laptop"
    assert body["price"] == 999.99
    assert body["category_id"] == category_id
    assert "id" in body


def test_create_product_without_category_fails() -> None:
    response = client.post(
        "/api/v1/products",
        json={"name": "Laptop", "description": "15-inch laptop", "price": 999.99},
    )

    assert response.status_code == 422


def test_create_product_with_invalid_category_returns_404() -> None:
    response = client.post(
        "/api/v1/products",
        json={"name": "Laptop", "description": "15-inch laptop", "price": 999.99, "category_id": 999999},
    )

    assert response.status_code == 404


def test_list_products() -> None:
    category_id = _create_category()
    client.post(
        "/api/v1/products",
        json={"name": "Mouse", "description": "Wireless mouse", "price": 19.99, "category_id": category_id},
    )

    response = client.get("/api/v1/products")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Mouse"


def test_get_product() -> None:
    category_id = _create_category()
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Monitor", "description": "27-inch monitor", "price": 299.0, "category_id": category_id},
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Monitor"


def test_update_product() -> None:
    category_id = _create_category()
    other_category_id = _create_category("Accessories")
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Webcam", "description": "HD webcam", "price": 39.0, "category_id": category_id},
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/products/{product_id}",
        json={
            "name": "Webcam Pro",
            "description": "4K webcam",
            "price": 59.0,
            "category_id": other_category_id,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": product_id,
        "name": "Webcam Pro",
        "description": "4K webcam",
        "price": 59.0,
        "category_id": other_category_id,
    }


def test_delete_product() -> None:
    category_id = _create_category()
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Headset", "description": "Gaming headset", "price": 79.0, "category_id": category_id},
    )
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/products/{product_id}")
    list_response = client.get("/api/v1/products")

    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_missing_product_returns_404() -> None:
    response = client.get("/api/v1/products/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
