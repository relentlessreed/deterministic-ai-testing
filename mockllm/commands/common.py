import json
import os
from pathlib import Path

import httpx

DEFAULT_BASE_URL = "http://localhost:8000/v1"


def post_chat(base_url: str, request: dict) -> dict:
    url = f"{base_url.rstrip('/')}/chat/completions"
    response = httpx.post(url, json=request, timeout=10)
    response.raise_for_status()
    return response.json()


def extract_content(response: dict) -> str:
    return response["choices"][0]["message"].get("content") or ""


def load_json(path: Path):
    return json.loads(path.read_text())


def github_actions_enabled() -> bool:
    return os.getenv("GITHUB_ACTIONS", "").lower() == "true"


def github_error(path: Path, title: str, message: str):
    if github_actions_enabled():
        print(f"::error file={path},title={title}::{message}")
