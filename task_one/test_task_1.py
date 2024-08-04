from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_get_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["description"] == "Push ups"


def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_create_task():
    response = client.post(
        "/tasks", json={"description": "test1234", "content": "test1234"}
    )
    assert response.status_code == 201
    assert response.json()["content"] == "test1234"


def test_update_task():
    response = client.put(
        "/tasks/4",
        json={
            "description": "Deleted",
            "content": "This will be deleted by the test_delete_task",
            "completed": False,
        },
    )
    assert response.status_code == 201
    assert response.json()["content"] == "This will be deleted by the test_delete_task"


def test_delete_taskk():
    response = client.delete("/tasks/4")
    assert response.status_code == 204



