from fastapi.testclient import TestClient

from main import app, db, get_todos_db


# Setup: Override dependency during testing
def setup_module():
    app.dependency_overrides[get_todos_db] = override_get_todos_db


# Teardown: Drop test_todos database after tests have run
def teardown_module():
    def drop_test_todos_db() -> None:
        db.drop_collection("test_todos")

    drop_test_todos_db()


def override_get_todos_db():
    test_todos = db.test_todos
    return test_todos


client = TestClient(app)


def test_root_returns_200_status_and_json_response():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_todo_item_returns_200_status_and_json_response():
    response = client.post(
        "/todos", json={"id": 1, "title": "Task One", "complete": False}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Task One",
        "complete": False,
    }


def test_create_todo_item2_returns_200_status_and_json_response():
    response = client.post(
        "/todos", json={"id": 2, "title": "Task Two", "complete": False}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "title": "Task Two",
        "complete": False,
    }


def test_create_existing_todo_returns_400_status_and_error():
    response = client.post(
        "/todos", json={"id": 1, "title": "Task One", "complete": False}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "To-do item with id 1 already exists",
    }


def test_get_all_todos_returns_200_status_and_json_response():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Task One",
            "complete": False,
        },
        {
            "id": 2,
            "title": "Task Two",
            "complete": False,
        },
    ]


def test_get_todo_item_by_id_returns_200_status_and_correct_response():
    response = client.get("/todos/2")
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "title": "Task Two",
        "complete": False,
    }


def test_get_todo_item_by_inexistent_id_returns_404_status_and_error():
    response = client.get("/todos/99")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No to-do item with id 99 found",
    }


def test_update_todo_item_returns_200_status_and_correct_response():
    response = client.put(
        "/todos/1",
        json={
            "id": 1,
            "title": "UPDATED Task One",
            "complete": True,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "UPDATED Task One",
        "complete": True,
    }


def test_update_todo_item_actually_updates_database():
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "UPDATED Task One",
        "complete": True,
    }


def test_update_todo_item_inexistent_id_returns_404_status_and_error():
    response = client.put(
        "/todos/99",
        json={
            "id": 99,
            "title": "INEXISTENT TASK!",
            "complete": True,
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No to-do item with id 99 found",
    }
