import difflib
import json
from pathlib import Path

from .common import github_error


def save_state_snapshot(args):
    path = Path(args.file)

    state = json.loads(args.json)

    snapshot = {
        "name": args.name or path.stem,
        "state": state,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2) + "\n")

    print(f"saved state snapshot: {path}")


def test_state_snapshot(args):
    path = Path(args.file)

    if not path.exists():
        print(f"state snapshot not found: {path}")
        return 1

    snapshot = json.loads(path.read_text())

    expected_state = snapshot.get("state", {})
    actual_state = json.loads(args.json)

    if expected_state != actual_state:
        print(f"FAIL {path}")

        github_error(
            path,
            "State Snapshot Mismatch",
            "Expected state did not match actual state",
        )

        print("expected:")
        print(json.dumps(expected_state, indent=2))

        print("actual:")
        print(json.dumps(actual_state, indent=2))

        diff = difflib.unified_diff(
            json.dumps(expected_state, indent=2).splitlines(),
            json.dumps(actual_state, indent=2).splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )

        print("\n".join(diff))
        return 1

    print(f"PASS {path}")
    return 0
