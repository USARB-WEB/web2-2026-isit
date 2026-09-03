from fastapi.testclient import TestClient

from app.db.models.product import Product
from app.db.session import SessionLocal
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    db = SessionLocal()
    try:
        db.query(Product).delete()
        db.commit()
    finally:
        db.close()


def test_create_product() -> None:
    response = client.post(
        "/api/v1/products",
        json={"name": "Laptop", "description": "15-inch laptop", "price": 999.99},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Laptop"
    assert body["price"] == 999.99
    assert "id" in body


def test_list_products() -> None:
    client.post(
        "/api/v1/products",
        json={"name": "Mouse", "description": "Wireless mouse", "price": 19.99},
    )

    response = client.get("/api/v1/products")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Mouse"


def test_get_products_with_prices() -> None:
    client.post(
        "/api/v1/products",
        json={"name": "Keyboard", "description": "Mechanical keyboard", "price": 49.5},
    )

    response = client.get("/api/v1/products/with-prices")

    assert response.status_code == 200
    assert response.json()[0]["price"] == 49.5


def test_get_product() -> None:
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Monitor", "description": "27-inch monitor", "price": 299.0},
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Monitor"


def test_update_product() -> None:
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Webcam", "description": "HD webcam", "price": 39.0},
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/products/{product_id}",
        json={"name": "Webcam Pro", "description": "4K webcam", "price": 59.0},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": product_id,
        "name": "Webcam Pro",
        "description": "4K webcam",
        "price": 59.0,
    }


def test_delete_product() -> None:
    create_response = client.post(
        "/api/v1/products",
        json={"name": "Headset", "description": "Gaming headset", "price": 79.0},
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
