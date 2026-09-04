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


def test_create_product_category() -> None:
    response = client.post(
        "/api/v1/product-categories",
        json={"name": "Electronics", "description": "Phones, laptops and gadgets"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Electronics"
    assert body["description"] == "Phones, laptops and gadgets"
    assert "id" in body


def test_list_product_categories() -> None:
    client.post(
        "/api/v1/product-categories",
        json={"name": "Books", "description": "Printed and digital books"},
    )

    response = client.get("/api/v1/product-categories")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Books"


def test_get_product_category() -> None:
    create_response = client.post(
        "/api/v1/product-categories",
        json={"name": "Toys", "description": "Games and toys for kids"},
    )
    category_id = create_response.json()["id"]

    response = client.get(f"/api/v1/product-categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Toys"


def test_update_product_category() -> None:
    create_response = client.post(
        "/api/v1/product-categories",
        json={"name": "Food", "description": "Groceries and snacks"},
    )
    category_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/product-categories/{category_id}",
        json={"name": "Food & Drinks", "description": "Groceries, snacks and beverages"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": category_id,
        "name": "Food & Drinks",
        "description": "Groceries, snacks and beverages",
    }


def test_delete_product_category() -> None:
    create_response = client.post(
        "/api/v1/product-categories",
        json={"name": "Sports", "description": "Fitness and sports gear"},
    )
    category_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/product-categories/{category_id}")
    list_response = client.get("/api/v1/product-categories")

    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_delete_product_category_in_use_returns_409() -> None:
    category_response = client.post(
        "/api/v1/product-categories",
        json={"name": "Electronics", "description": "Phones and laptops"},
    )
    category_id = category_response.json()["id"]
    client.post(
        "/api/v1/products",
        json={"name": "Laptop", "description": "Portable computer", "price": 999.99, "category_id": category_id},
    )

    response = client.delete(f"/api/v1/product-categories/{category_id}")

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Cannot delete this product category because it is used by one or more products."
    }


def test_missing_product_category_returns_404() -> None:
    response = client.get("/api/v1/product-categories/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}
