import time
import uuid
from typing import Any, Dict, List


def chat_completion_response(model: str, content: str, tool_calls=None) -> Dict[str, Any]:
    message: Dict[str, Any] = {"role": "assistant", "content": content}
    if tool_calls:
        message["tool_calls"] = tool_calls
        message["content"] = content or None
    return {
        "id": f"chatcmpl-mock-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "message": message, "finish_reason": "tool_calls" if tool_calls else "stop"}],
        "usage": {
            "prompt_tokens": 1,
            "completion_tokens": len(content.split()) if content else 0,
            "total_tokens": 1 + (len(content.split()) if content else 0),
        },
    }


def completion_response(model: str, content: str) -> Dict[str, Any]:
    return {
        "id": f"cmpl-mock-{uuid.uuid4().hex[:12]}",
        "object": "text_completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{"text": content, "index": 0, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 1, "completion_tokens": len(content.split()), "total_tokens": 1 + len(content.split())},
    }


def embedding_vector(text: str, dimensions: int = 32) -> List[float]:
    values = [0.0] * dimensions
    for index, char in enumerate(text):
        values[index % dimensions] += (ord(char) % 97) / 100.0
    norm = sum(abs(v) for v in values) or 1.0
    return [round(v / norm, 6) for v in values]


def embeddings_response(model: str, input_value) -> Dict[str, Any]:
    inputs = [input_value] if isinstance(input_value, str) else list(input_value)
    return {
        "object": "list",
        "model": model,
        "data": [
            {"object": "embedding", "index": index, "embedding": embedding_vector(str(item))}
            for index, item in enumerate(inputs)
        ],
        "usage": {"prompt_tokens": len(inputs), "total_tokens": len(inputs)},
    }
