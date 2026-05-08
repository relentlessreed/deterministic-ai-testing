from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_completion_default():
    response = client.post("/v1/chat/completions", json={"model": "gpt-4o", "messages": [{"role": "user", "content": "unknown prompt"}]})
    assert response.status_code == 200
    assert response.json()["object"] == "chat.completion"


def test_chat_completion_scenario_match():
    response = client.post("/v1/chat/completions", json={"model": "gpt-4o", "messages": [{"role": "user", "content": "hello"}]})
    assert response.status_code == 200
    assert "Hello" in response.json()["choices"][0]["message"]["content"]


def test_tool_call_scenario():
    response = client.post("/v1/chat/completions", json={"model": "gpt-4o", "messages": [{"role": "user", "content": "please use tool"}]})
    assert response.status_code == 200
    message = response.json()["choices"][0]["message"]
    assert message["tool_calls"][0]["function"]["name"] == "search_docs"


def test_error_scenario():
    response = client.post("/v1/chat/completions", json={"model": "gpt-4o", "messages": [{"role": "user", "content": "rate limit"}]})
    assert response.status_code == 429


def test_embeddings():
    response = client.post("/v1/embeddings", json={"model": "text-embedding-3-small", "input": "hello"})
    assert response.status_code == 200
    assert len(response.json()["data"][0]["embedding"]) == 32


def test_responses_api_default():
    response = client.post(
        "/v1/responses",
        json={
            "model": "gpt-4o",
            "input": "unknown prompt",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["object"] == "response"
    assert body["status"] == "completed"
    assert "output_text" in body


def test_responses_api_scenario_match():
    response = client.post(
        "/v1/responses",
        json={
            "model": "gpt-4o",
            "input": "hello",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "Hello" in body["output_text"]
    assert body["output"][0]["role"] == "assistant"
