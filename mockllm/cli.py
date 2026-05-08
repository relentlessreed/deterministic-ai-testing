import argparse
import difflib
import json
import sys
from pathlib import Path

import httpx
import uvicorn

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
    expected_tool_order = expected.get("tool_order")

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

    if expected_tool_order is not None:
        tool_calls = response["choices"][0]["message"].get("tool_calls") or []
        actual_order = [
            tool_call.get("function", {}).get("name")
            for tool_call in tool_calls
        ]

        if actual_order != expected_tool_order:
            passed = False
            print(f"FAIL {path}")
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










def replay_conversation(args):
    path = Path(args.file)

    if not path.exists():
        print(f"conversation file not found: {path}")
        return 1

    conversation = json.loads(path.read_text())

    model = conversation.get("model", "gpt-4o")
    messages = conversation.get("messages", [])

    if not messages:
        print("no messages found")
        return 1

    for index, message in enumerate(messages, start=1):
        request = {
            "model": model,
            "messages": [message],
        }

        print(f"--- message {index} ---")
        print(f"user: {message.get('content', '')}")

        response = post_chat(args.base_url, request)

        assistant = (
            response["choices"][0]["message"]
            .get("content") or ""
        )

        if assistant:
            print(f"assistant: {assistant}")

        tool_calls = (
            response["choices"][0]["message"]
            .get("tool_calls") or []
        )

        if tool_calls:
            print("tool calls:")
            for tool_call in tool_calls:
                name = tool_call.get("function", {}).get("name")
                print(f"  - {name}")

        print()


def generate_html_report(args):
    target = Path(args.file)
    files = sorted(target.glob("*.json")) if target.is_dir() else [target]

    if not files:
        print(f"no snapshot files found: {target}")
        return 1

    sections = []

    for path in files:
        snapshot = json.loads(path.read_text())

        request = snapshot.get("request", {})
        expected = snapshot.get("expected", {})
        response = snapshot.get("response", {})

        prompt = ""
        messages = request.get("messages") or []
        if messages:
            prompt = messages[-1].get("content", "")

        expected_content = expected.get("content", "")
        actual_content = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        section = f"""
        <div class="snapshot">
            <h2>{path.name}</h2>

            <h3>Prompt</h3>
            <pre>{prompt}</pre>

            <h3>Expected</h3>
            <pre>{expected_content}</pre>

            <h3>Response</h3>
            <pre>{actual_content}</pre>
        </div>
        """

        sections.append(section)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>mockllm snapshot report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }}

        h1 {{
            color: #222;
        }}

        .snapshot {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        pre {{
            background: #f0f0f0;
            padding: 12px;
            overflow-x: auto;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
    <h1>mockllm snapshot report</h1>

    {''.join(sections)}

</body>
</html>
"""

    output = Path("mockllm-report.html")
    output.write_text(html)

    print(f"generated report: {output}")


def init_project(args):
    scenarios_dir = Path("scenarios")
    snapshots_dir = Path("snapshots")
    tests_dir = Path("tests")

    scenarios_dir.mkdir(exist_ok=True)
    snapshots_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)

    scenario_file = scenarios_dir / "default.yaml"
    if not scenario_file.exists():
        scenario_file.write_text(
            """scenarios:
  - name: hello
    match:
      contains: hello
    response:
      content: Hello from mockllm.
"""
        )

    test_file = tests_dir / "test_ai.py"
    if not test_file.exists():
        test_file.write_text(
            """def test_mockllm():
    assert True
"""
        )

    print("initialized mockllm project")
    print("created:")
    print("  scenarios/default.yaml")
    print("  snapshots/")
    print("  tests/test_ai.py")


def serve(args):
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


def main():
    parser = argparse.ArgumentParser(
        prog="mockllm",
        description="Snapshot testing CLI for deterministic AI testing.",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=init_project)

    replay_parser = subparsers.add_parser("replay")
    replay_parser.add_argument("file")
    replay_parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    replay_parser.set_defaults(func=replay_conversation)

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--reload", action="store_true")
    serve_parser.set_defaults(func=serve)

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

    report = snapshot_sub.add_parser("report")
    report.add_argument("file")
    report.set_defaults(func=generate_html_report)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    result = args.func(args)
    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())