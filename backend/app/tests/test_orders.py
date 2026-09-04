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


def test_create_order() -> None:
    response = client.post("/api/v1/orders", json={"client_name": "Alice"})

    assert response.status_code == 201
    body = response.json()
    assert body["client_name"] == "Alice"
    assert body["products"] == []
    assert body["products_count"] == 0
    assert body["total_sum"] == 0.0
    assert "id" in body


def _create_category(name: str = "Electronics") -> int:
    response = client.post(
        "/api/v1/product-categories",
        json={"name": name, "description": "Test category"},
    )
    return response.json()["id"]


def _create_product(category_id: int, name: str = "Laptop", price: float = 999.99) -> int:
    response = client.post(
        "/api/v1/products",
        json={"name": name, "description": "Test product", "price": price, "category_id": category_id},
    )
    return response.json()["id"]


def test_create_order_with_products() -> None:
    category_id = _create_category()
    product_id = _create_product(category_id, name="Laptop", price=999.99)
    other_product_id = _create_product(category_id, name="Mouse", price=19.99)

    response = client.post(
        "/api/v1/orders",
        json={
            "client_name": "Frank",
            "products": [
                {"product_id": product_id, "quantity": 1},
                {"product_id": other_product_id, "quantity": 2},
            ],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["client_name"] == "Frank"
    assert len(body["products"]) == 2
    assert {p["product_id"] for p in body["products"]} == {product_id, other_product_id}
    assert all(p["order_id"] == body["id"] for p in body["products"])
    assert body["products_count"] == 3  # 1 laptop + 2 mice
    assert body["total_sum"] == round(999.99 * 1 + 19.99 * 2, 2)

    list_response = client.get(f"/api/v1/orders/{body['id']}/products")
    assert len(list_response.json()) == 2


def test_create_order_with_missing_product_returns_404() -> None:
    response = client.post(
        "/api/v1/orders",
        json={"client_name": "Grace", "products": [{"product_id": 999999, "quantity": 1}]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product 999999 not found"}


def test_list_orders() -> None:
    client.post("/api/v1/orders", json={"client_name": "Bob"})

    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["client_name"] == "Bob"
    assert body[0]["products_count"] == 0
    assert body[0]["total_sum"] == 0.0
    assert "products" not in body[0]


def test_list_orders_includes_totals_without_product_list() -> None:
    category_id = _create_category()
    product_id = _create_product(category_id, name="Monitor", price=299.0)
    create_response = client.post(
        "/api/v1/orders",
        json={"client_name": "Ivan", "products": [{"product_id": product_id, "quantity": 2}]},
    )
    order_id = create_response.json()["id"]

    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    order_summary = next(o for o in response.json() if o["id"] == order_id)
    assert order_summary["products_count"] == 2
    assert order_summary["total_sum"] == round(299.0 * 2, 2)
    assert "products" not in order_summary


def test_get_order() -> None:
    create_response = client.post("/api/v1/orders", json={"client_name": "Carol"})
    order_id = create_response.json()["id"]

    response = client.get(f"/api/v1/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["client_name"] == "Carol"


def test_get_order_computes_count_and_total_sum() -> None:
    category_id = _create_category()
    product_id = _create_product(category_id, name="Keyboard", price=49.50)
    create_response = client.post(
        "/api/v1/orders",
        json={"client_name": "Heidi", "products": [{"product_id": product_id, "quantity": 3}]},
    )
    order_id = create_response.json()["id"]

    response = client.get(f"/api/v1/orders/{order_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["products_count"] == 3
    assert body["total_sum"] == round(49.50 * 3, 2)


def test_update_order() -> None:
    create_response = client.post("/api/v1/orders", json={"client_name": "Dave"})
    order_id = create_response.json()["id"]

    response = client.put(f"/api/v1/orders/{order_id}", json={"client_name": "David"})

    assert response.status_code == 200
    assert response.json() == {
        "id": order_id,
        "client_name": "David",
        "products": [],
        "products_count": 0,
        "total_sum": 0.0,
    }


def test_delete_order() -> None:
    create_response = client.post("/api/v1/orders", json={"client_name": "Eve"})
    order_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/orders/{order_id}")
    list_response = client.get("/api/v1/orders")

    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_missing_order_returns_404() -> None:
    response = client.get("/api/v1/orders/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
