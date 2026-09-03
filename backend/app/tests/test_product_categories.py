from fastapi.testclient import TestClient

from app.api.v1.dependencies.product_categories import product_category_repository
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    product_category_repository.replace_all([])


def test_create_product_category() -> None:
    response = client.post(
        "/api/v1/product-categories",
        json={"name": "Electronics", "description": "Phones, laptops and gadgets"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Electronics",
        "description": "Phones, laptops and gadgets",
    }


def test_list_product_categories() -> None:
    client.post(
        "/api/v1/product-categories",
        json={"name": "Books", "description": "Printed and digital books"},
    )

    response = client.get("/api/v1/product-categories")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Books", "description": "Printed and digital books"}]


def test_get_product_category() -> None:
    client.post(
        "/api/v1/product-categories",
        json={"name": "Toys", "description": "Games and toys for kids"},
    )

    response = client.get("/api/v1/product-categories/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Toys"


def test_update_product_category() -> None:
    client.post(
        "/api/v1/product-categories",
        json={"name": "Food", "description": "Groceries and snacks"},
    )

    response = client.put(
        "/api/v1/product-categories/1",
        json={"name": "Food & Drinks", "description": "Groceries, snacks and beverages"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Food & Drinks",
        "description": "Groceries, snacks and beverages",
    }


def test_delete_product_category() -> None:
    client.post(
        "/api/v1/product-categories",
        json={"name": "Sports", "description": "Fitness and sports gear"},
    )

    delete_response = client.delete("/api/v1/product-categories/1")
    list_response = client.get("/api/v1/product-categories")

    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_missing_product_category_returns_404() -> None:
    response = client.get("/api/v1/product-categories/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}
