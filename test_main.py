from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_returns_200_status_and_json_response():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_todo_item_returns_200_status_and_json_response():
    response = client.post(
        "/todos", json={"id": 1234, "title": "Task One", "complete": False}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1234,
        "title": "Task One",
        "complete": False,
    }


def test_create_existing_todo_returns_400_status_and_error():
    response = client.post(
        "/todos", json={"id": 1234, "title": "Task One", "complete": False}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "To-do item with id 1234 already exists",
    }
