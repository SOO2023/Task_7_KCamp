from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def get_authentication():
    login_response = client.post(
        "/auth/login", data={"username": "sam", "password": "secret"}
    )
    token = login_response.json()["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    return header


header = get_authentication()


def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_create_user():
    response = client.post(
        "/users",
        json={
            "username": "sam",
            "password": "12345",
        },
    )
    assert response.status_code == 406
    assert response.json() == {"detail": {"message": "UNIQUE constraint failed"}}


def test_login():
    response = client.post(
        "/auth/login", data={"username": "sam", "password": "secret"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_get_all_posts():
    response = client.get("/posts/all-posts")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_all_user_posts():
    response = client.get("/posts", headers=header)
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_a_post():
    response = client.get("/posts/1", headers=header)
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_post():
    response = client.post(
        "/posts", data={"title": "test1234", "content": "test1234"}, headers=header
    )
    assert response.status_code == 201
    assert response.json()["content"] == "test1234"


def test_update_post():
    response = client.put(
        "/posts/2",
        data={"title": "updated1234", "content": "updated1234"},
        headers=header,
    )
    assert response.status_code == 201
    assert response.json()["content"] == "updated1234"


def test_delete_post():
    response = client.delete(
        "/posts/2",
        headers=header,
    )
    assert response.status_code == 204

