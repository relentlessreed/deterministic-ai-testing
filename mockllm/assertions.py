import json
from typing import Any


def extract_tool_calls(response: Any) -> list[dict]:
    if isinstance(response, dict):
        return response.get("choices", [{}])[0].get("message", {}).get("tool_calls") or []

    choices = getattr(response, "choices", [])
    if not choices:
        return []

    message = getattr(choices[0], "message", None)
    if message is None:
        return []

    return getattr(message, "tool_calls", None) or []


def _tool_name(tool_call: Any) -> str | None:
    if isinstance(tool_call, dict):
        return tool_call.get("function", {}).get("name")

    function = getattr(tool_call, "function", None)
    return getattr(function, "name", None)


def _tool_arguments(tool_call: Any) -> dict:
    if isinstance(tool_call, dict):
        raw = tool_call.get("function", {}).get("arguments") or "{}"
    else:
        function = getattr(tool_call, "function", None)
        raw = getattr(function, "arguments", "{}")

    if isinstance(raw, dict):
        return raw

    try:
        return json.loads(raw)
    except Exception:
        return {}


def assert_tool_called(response: Any, tool_name: str):
    tool_calls = extract_tool_calls(response)
    names = [_tool_name(tool_call) for tool_call in tool_calls]

    assert tool_name in names, (
        f"Expected tool call '{tool_name}', but got {names}"
    )


def assert_tool_called_with(response: Any, tool_name: str, expected_arguments: dict):
    tool_calls = extract_tool_calls(response)

    for tool_call in tool_calls:
        if _tool_name(tool_call) != tool_name:
            continue

        actual_arguments = _tool_arguments(tool_call)

        for key, expected_value in expected_arguments.items():
            actual_value = actual_arguments.get(key)

            assert actual_value == expected_value, (
                f"Expected tool '{tool_name}' argument {key}={expected_value!r}, "
                f"but got {actual_value!r}. Full arguments: {actual_arguments}"
            )

        return

    names = [_tool_name(tool_call) for tool_call in tool_calls]
    raise AssertionError(
        f"Expected tool call '{tool_name}', but got {names}"
    )
