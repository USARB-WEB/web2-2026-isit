from fastapi.testclient import TestClient

from app.api.v1.dependencies.students import student_repository
from app.main import app

client = TestClient(app)


def setup_function() -> None:
    student_repository.replace_all([])


def test_create_student() -> None:
    response = client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "first_name": "Ana",
        "last_name": "Popescu",
        "email": "ana.popescu@example.com",
        "age": 20,
    }


def test_list_students() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ion",
            "last_name": "Rusu",
            "email": "ion.rusu@example.com",
            "age": 22,
        },
    )

    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
        {
            "id": 2,
            "first_name": "Ion",
            "last_name": "Rusu",
            "email": "ion.rusu@example.com",
            "age": 22,
        },
    ]


def test_get_student() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )

    response = client.get("/api/v1/students/1")

    assert response.status_code == 200
    assert response.json()["email"] == "ana.popescu@example.com"


def test_update_student() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )

    response = client.put(
        "/api/v1/students/1",
        json={
            "first_name": "Ana Maria",
            "last_name": "Popescu",
            "email": "ana.maria@example.com",
            "age": 21,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "first_name": "Ana Maria",
        "last_name": "Popescu",
        "email": "ana.maria@example.com",
        "age": 21,
    }


def test_delete_student() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )

    delete_response = client.delete("/api/v1/students/1")
    list_response = client.get("/api/v1/students")

    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_missing_student_returns_404() -> None:
    response = client.get("/api/v1/students/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_list_students_with_query_filters() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Rusu",
            "email": "ana.rusu@example.com",
            "age": 23,
        },
    )

    response = client.get("/api/v1/students/query?first_name=Ana&max_age=21")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "ana.popescu@example.com"


def test_query_students_with_query_method() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Popescu",
            "email": "ana.popescu@example.com",
            "age": 20,
        },
    )
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ana",
            "last_name": "Rusu",
            "email": "ana.rusu@example.com",
            "age": 23,
        },
    )

    response = client.request(
        "QUERY",
        "/api/v1/students",
        json={"first_name": "Ana", "max_age": 21},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "ana.popescu@example.com"


def test_query_students_with_empty_body_returns_all() -> None:
    client.post(
        "/api/v1/students",
        json={
            "first_name": "Ion",
            "last_name": "Rusu",
            "email": "ion.rusu@example.com",
            "age": 22,
        },
    )

    response = client.request("QUERY", "/api/v1/students", json={})

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_query_students_with_invalid_filter_returns_422() -> None:
    response = client.request("QUERY", "/api/v1/students", json={"min_age": 5})

    assert response.status_code == 422


def test_query_method_is_documented_in_openapi() -> None:
    schema = client.get("/openapi.json").json()
    operation = schema["paths"]["/api/v1/students"]["query"]

    assert schema["openapi"] == "3.2.0"
    assert operation["requestBody"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/StudentQuery"
    }
