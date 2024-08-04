from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def get_authentication():
    logint_response = client.post(
        "/auth/login", data={"username": "sam@email.com", "password": "secret"}
    )
    token = logint_response.json()["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    return header


header = get_authentication()


def test_get_all_user():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json()[0] == {
        "name": "John Doe",
        "address": "1 Abc Street",
        "contact": "+234123456789",
        "email": "johndoe@email.com",
        "id": 1,
    }


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "sam",
            "address": "abc",
            "contact": "123456789",
            "email": "sam@email.com",
            "password": "12345",
        },
    )
    assert response.status_code == 406
    assert response.json() == {
        "detail": {"message": "The email has already been used by another user."}
    }


def test_login():
    response = client.post(
        "/auth/login", data={"username": "sam@email.com", "password": "secret"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_get_order_by_id():
    response = client.get("/orders/1", headers=header)
    assert response.status_code == 200
    assert response.json() == {
        "product_id": 2,
        "quantity": 5,
        "id": 1,
        "user_id": 3,
        "unit_price": 30.1,
        "total_price": 150.5,
        "order_date": "2024-08-01T18:40:37.949558",
        "order_status": "Pending",
        "completion_time": 2,
        "product_details": {
            "product_id": 2,
            "product_name": "Aeon Deep Freezer",
            "product_category": "Electronics",
        },
    }


def test_get_all_user_orders():
    response = client.get("/orders", headers=header)
    assert response.status_code == 200
    assert response.json()[0] == {
        "product_id": 2,
        "quantity": 5,
        "id": 1,
        "user_id": 3,
        "unit_price": 30.1,
        "total_price": 150.5,
        "order_date": "2024-08-01T18:40:37.949558",
        "order_status": "Pending",
        "completion_time": 2,
        "product_details": {
            "product_id": 2,
            "product_name": "Aeon Deep Freezer",
            "product_category": "Electronics",
        },
    }


def test_make_order():
    response = client.post(
        "/orders", data={"product_id": 4, "quantity": 2}, headers=header
    )
    assert response.status_code == 201
    assert response.json()["product_details"] == {
        "product_id": 4,
        "product_name": "Liverpool Jersey",
        "product_category": "Clothing",
    }


def test_update_order():
    response = client.put("/orders/11", data={"quantity": 4}, headers=header)
    assert response.status_code == 201
    assert response.json()["quantity"] == 4


def test_delete_order():
    response = client.delete("/orders/11", headers=header)
    assert response.status_code == 204



