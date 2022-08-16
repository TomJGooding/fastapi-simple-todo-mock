from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_returns_200_status_and_json_response():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
