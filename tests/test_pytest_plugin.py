import httpx


def test_mockllm_server_fixture(mockllm_server):
    response = httpx.get(f"{mockllm_server}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
