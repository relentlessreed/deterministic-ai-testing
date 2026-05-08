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

    if expected_content != actual_content:
        print(f"FAIL {path}")

        github_error(
            path,
            "Snapshot Content Mismatch",
            "Expected content did not match actual response",
        )

        print("expected:")
        print(expected_content)
        print("actual:")
        print(actual_content)

        diff = difflib.unified_diff(
            expected_content.splitlines(),
            actual_content.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )

        print("\n".join(diff))
        return False

    print(f"PASS {path}")
    return True


def test_snapshots(args):
    target = Path(args.file)
    files = sorted(target.glob("*.json")) if target.is_dir() else [target]

    if not files:
        print(f"no snapshot files found: {target}")
        return 1

    results = [test_snapshot_file(path, args.base_url) for path in files]
    return 0 if all(results) else 1
