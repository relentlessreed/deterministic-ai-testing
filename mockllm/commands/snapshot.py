import difflib
import json
from pathlib import Path

from .common import (
    DEFAULT_BASE_URL,
    extract_content,
    github_error,
    load_json,
    post_chat,
)


def save_snapshot(args):
    path = Path(args.file)

    request = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.prompt}],
    }

    response = post_chat(args.base_url, request)
    content = extract_content(response)

    snapshot = {
        "name": args.name or path.stem,
        "base_url": args.base_url,
        "request": request,
        "expected": {"content": content},
        "response": response,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2) + "\n")

    print(f"saved snapshot: {path}")
    print(f"expected content: {content}")


def test_snapshot_file(path: Path, base_url_override: str | None = None) -> bool:
    snapshot = load_json(path)

    base_url = base_url_override or snapshot.get("base_url") or DEFAULT_BASE_URL
    request = snapshot["request"]
    expected = snapshot["expected"]

    response = post_chat(base_url, request)
    actual_content = extract_content(response)

    expected_content = expected.get("content")
    expected_contains = expected.get("contains")
    expected_tool_name = expected.get("tool_name")
    expected_tool_order = expected.get("tool_order")

    passed = True

    if expected_content is not None and actual_content != expected_content:
        passed = False
        print(f"FAIL {path}")

        github_error(
            path,
            "Snapshot Content Mismatch",
            "Expected content did not match actual response",
        )

        print("expected exact:")
        print(expected_content)
        print("actual:")
        print(actual_content)
        print("diff:")

        diff = difflib.unified_diff(
            expected_content.splitlines(),
            actual_content.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )

        print("\n".join(diff))

    if expected_contains is not None and expected_contains not in actual_content:
        passed = False
        print(f"FAIL {path}")

        github_error(
            path,
            "Snapshot Contains Mismatch",
            f"Expected response to contain: {expected_contains}",
        )

        print(f"expected contains: {expected_contains}")
        print(f"actual:            {actual_content}")

    tool_calls = response["choices"][0]["message"].get("tool_calls") or []
    tool_names = [
        tool_call.get("function", {}).get("name")
        for tool_call in tool_calls
    ]

    if expected_tool_name is not None and expected_tool_name not in tool_names:
        passed = False
        print(f"FAIL {path}")

        github_error(
            path,
            "Snapshot Tool Call Mismatch",
            f"Expected tool call: {expected_tool_name}",
        )

        print(f"expected tool call: {expected_tool_name}")
        print(f"actual tool calls:   {tool_names}")

    if expected_tool_order is not None:
        actual_order = tool_names

        if actual_order != expected_tool_order:
            passed = False
            print(f"FAIL {path}")

            github_error(
                path,
                "Snapshot Tool Order Mismatch",
                "Tool call order did not match expected order",
            )

            print(f"expected tool order: {expected_tool_order}")
            print(f"actual tool order:   {actual_order}")

    if passed:
        print(f"PASS {path}")

    return passed


def test_snapshots(args):
    target = Path(args.file)
    files = sorted(target.glob("*.json")) if target.is_dir() else [target]

    if not files:
        print(f"no snapshot files found: {target}")
        return 1

    results = [test_snapshot_file(path, args.base_url) for path in files]
    return 0 if all(results) else 1
