import argparse
import sys

from mockllm.commands.common import DEFAULT_BASE_URL
from mockllm.commands.dashboard import dashboard
from mockllm.commands.init import init_project
from mockllm.commands.replay import replay_conversation
from mockllm.commands.reports import generate_html_report
from mockllm.commands.serve import serve
from mockllm.commands.snapshot import save_snapshot, test_snapshots
from mockllm.commands.state import save_state_snapshot, test_state_snapshot


def main():
    parser = argparse.ArgumentParser(
        prog="mockllm",
        description="Snapshot testing CLI for deterministic AI testing.",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=init_project)

    state_parser = subparsers.add_parser("state")
    state_sub = state_parser.add_subparsers(dest="state_command")

    state_save = state_sub.add_parser("save")
    state_save.add_argument("file")
    state_save.add_argument("--name")
    state_save.add_argument("--json", required=True)
    state_save.set_defaults(func=save_state_snapshot)

    state_test = state_sub.add_parser("test")
    state_test.add_argument("file")
    state_test.add_argument("--json", required=True)
    state_test.set_defaults(func=test_state_snapshot)

    dashboard_parser = subparsers.add_parser("dashboard")
    dashboard_parser.add_argument("--open", action="store_true")
    dashboard_parser.set_defaults(func=dashboard)

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
