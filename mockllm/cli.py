import argparse
import difflib
import json
import sys
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
    snapshot = json.loads(path.read_text())

    base_url = base_url_override or snapshot.get("base_url") or DEFAULT_BASE_URL
    request = snapshot["request"]
    expected = snapshot["expected"]

    response = post_chat(base_url, request)
    actual_content = extract_content(response)

    expected_content = expected.get("content")
    expected_contains = expected.get("contains")
    expected_tool_name = expected.get("tool_name")

    passed = True

    if expected_content is not None and actual_content != expected_content:
        passed = False
        print(f"FAIL {path}")
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
        print(f"expected contains: {expected_contains}")
        print(f"actual:            {actual_content}")

    if expected_tool_name is not None:
        tool_calls = response["choices"][0]["message"].get("tool_calls") or []
        tool_names = [
            tool_call.get("function", {}).get("name")
            for tool_call in tool_calls
        ]

        if expected_tool_name not in tool_names:
            passed = False
            print(f"FAIL {path}")
            print(f"expected tool call: {expected_tool_name}")
            print(f"actual tool calls:   {tool_names}")

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


def main():
    parser = argparse.ArgumentParser(
        prog="mockllm",
        description="Snapshot testing CLI for deterministic AI testing.",
    )

    subparsers = parser.add_subparsers(dest="command")

    snapshot = subparsers.add_parser("snapshot")
    snapshot_sub = snapshot.add_subparsers(dest="snapshot_command")

    save = snapshot_sub.add_parser("save")
    save.add_argument("file")
    save.add_argument("--prompt", required=True)
    save.add_argument("--name")
    save.add_argument("--model", default="gpt-4o")
    save.add_argument("--base-url", default=DEFAULT_BASE_URL)
    save.set_defaults(func=save_snapshot)

    test = snapshot_sub.add_parser("test")
    test.add_argument("file")
    test.add_argument("--base-url")
    test.set_defaults(func=test_snapshots)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    result = args.func(args)
    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())
PY
