from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP Error")

    def json(self):
        return self._json

def dummy_requests_post(url, headers=None, json=None):
    return DummyResponse(200, [{"generated_text": "Hello, test response!"}])

def test_chat(monkeypatch):
    monkeypatch.setattr("app.main.requests.post", dummy_requests_post)

    payload = {"message": "Hi there!"}
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Hello, test response!"
