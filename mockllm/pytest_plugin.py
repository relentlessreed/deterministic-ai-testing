import socket
import subprocess
import sys
import time

import httpx
import pytest


def _find_free_port():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture
def mockllm_server():
    port = _find_free_port()
    base_url = f"http://127.0.0.1:{port}"

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    health_url = f"{base_url}/health"

    try:
        for _ in range(50):
            try:
                response = httpx.get(health_url, timeout=0.2)
                if response.status_code == 200:
                    break
            except Exception:
                time.sleep(0.1)
        else:
            stdout, stderr = process.communicate(timeout=1)
            raise RuntimeError(
                f"MockLLM server did not start.\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
            )

        yield base_url

    finally:
        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
