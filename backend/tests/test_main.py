import pytest
from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)

# A dummy response class to simulate external API responses
class DummyResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP Error")

    def json(self):
        return self._json

# Dummy async function for a successful external API call
async def dummy_async_post(self, url, headers=None, json=None):
    return DummyResponse(200, [{"generated_text": "Hello, test response!"}])

# Dummy async function to simulate an external API returning an error message
async def dummy_async_post_error(self, url, headers=None, json=None):
    return DummyResponse(200, {"error": "Hugging Face API error"})

def test_chat(monkeypatch):
    # Patch the 'post' method on the AsyncClient class from httpx
    monkeypatch.setattr(httpx.AsyncClient, "post", dummy_async_post)

    payload = {"message": "Hi there!"}
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Hello, test response!"

def test_chat_missing_message():
    # Missing the "message" field should trigger a validation error (422)
    response = client.post("/api/chat", json={})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # FastAPI returns a "detail" key with error info

def test_chat_empty_message():
    # An empty message should fail validation because min_length is 1
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_chat_too_long_message():
    # A message longer than allowed (more than 500 characters)
    long_message = "a" * 501
    response = client.post("/api/chat", json={"message": long_message})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_chat_external_api_error(monkeypatch):
    # Patch the 'post' method on httpx.AsyncClient to simulate an error response
    monkeypatch.setattr(httpx.AsyncClient, "post", dummy_async_post_error)
    
    payload = {"message": "Hi there!"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 500
    data = response.json()
    # Our custom exception handler returns an "error" and "message"
    assert "error" in data
    assert data["message"] == "Hugging Face API error"
