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


def _create_product(category_id: int, name: str = "Laptop", price: float = 999.99) -> int:
    response = client.post(
        "/api/v1/products",
        json={"name": name, "description": "Test product", "price": price, "category_id": category_id},
    )
    return response.json()["id"]


def _create_order(client_name: str = "Alice") -> int:
    response = client.post("/api/v1/orders", json={"client_name": client_name})
    return response.json()["id"]


def test_add_order_product() -> None:
    order_id = _create_order()
    product_id = _create_product(_create_category())

    response = client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 2},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["order_id"] == order_id
    assert body["product_id"] == product_id
    assert body["quantity"] == 2
    assert "id" in body


def test_add_order_product_with_missing_order_returns_404() -> None:
    product_id = _create_product(_create_category())

    response = client.post(
        "/api/v1/orders/999999/products",
        json={"product_id": product_id, "quantity": 1},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_add_order_product_with_missing_product_returns_404() -> None:
    order_id = _create_order()

    response = client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": 999999, "quantity": 1},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product 999999 not found"}


def test_list_order_products() -> None:
    order_id = _create_order()
    product_id = _create_product(_create_category())
    client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 3},
    )

    response = client.get(f"/api/v1/orders/{order_id}/products")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["quantity"] == 3


def test_get_order_product() -> None:
    order_id = _create_order()
    product_id = _create_product(_create_category())
    create_response = client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 1},
    )
    order_product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/orders/{order_id}/products/{order_product_id}")

    assert response.status_code == 200
    assert response.json()["id"] == order_product_id


def test_update_order_product() -> None:
    order_id = _create_order()
    product_id = _create_product(_create_category())
    create_response = client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 1},
    )
    order_product_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/orders/{order_id}/products/{order_product_id}",
        json={"product_id": product_id, "quantity": 5},
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_delete_order_product() -> None:
    order_id = _create_order()
    product_id = _create_product(_create_category())
    create_response = client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 1},
    )
    order_product_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/orders/{order_id}/products/{order_product_id}")
    list_response = client.get(f"/api/v1/orders/{order_id}/products")

    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_missing_order_product_returns_404() -> None:
    order_id = _create_order()

    response = client.get(f"/api/v1/orders/{order_id}/products/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order product not found"}


def test_delete_product_used_in_order_returns_409() -> None:
    order_id = _create_order()
    category_id = _create_category()
    product_id = _create_product(category_id)
    client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 1},
    )

    response = client.delete(f"/api/v1/products/{product_id}")

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Cannot delete this product because it is used by one or more orders."
    }


def test_delete_order_removes_its_order_products() -> None:
    order_id = _create_order()
    product_id = _create_product(_create_category())
    client.post(
        f"/api/v1/orders/{order_id}/products",
        json={"product_id": product_id, "quantity": 1},
    )

    delete_response = client.delete(f"/api/v1/orders/{order_id}")

    assert delete_response.status_code == 204
