from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def get_authentication():
    login_response = client.post(
        "/auth/login", data={"username": "sam@email.com", "password": "secret"}
    )
    token = login_response.json()["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    return header


header = get_authentication()


def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_all_authors():
    response = client.get("/authors")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "samson ayo",
            "email": "sam@email.com",
            "password": "12345",
        },
    )
    assert response.status_code == 422
    assert response.json() == {"detail": {"message": "UNIQUE constraint failed"}}


def test_login():
    response = client.post(
        "/auth/login", data={"username": "sam@email.com", "password": "secret"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_borrow_book():
    response = client.post(
        "/borrow/30", headers=header, data={"return_date": "4-10-2024"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": {"message": "Book with id 30 cannot be found."}
    }


def test_return_book():
    response = client.post("/return/3", headers=header)
    assert response.status_code == 400
    assert response.json() == {
        "detail": {"message": "You have already returned this book with id 3."}
    }

