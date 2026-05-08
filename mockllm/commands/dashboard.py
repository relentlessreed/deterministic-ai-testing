from html import escape
from pathlib import Path
import json
import webbrowser

from .common import load_json


def snapshot_card(path: Path) -> str:
    snapshot = load_json(path)

    request = snapshot.get("request", {})
    expected = snapshot.get("expected", {})
    response = snapshot.get("response", {})

    messages = request.get("messages") or []
    prompt = messages[-1].get("content", "") if messages else ""

    expected_content = expected.get("content", "")

    actual_content = (
        response.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )

    return f"""
    <div class="card">
        <h2>{escape(path.name)}</h2>

        <h3>Prompt</h3>
        <pre>{escape(prompt)}</pre>

        <h3>Expected</h3>
        <pre>{escape(expected_content)}</pre>

        <h3>Recorded response</h3>
        <pre>{escape(actual_content or "")}</pre>
    </div>
    """


def state_card(path: Path) -> str:
    snapshot = load_json(path)

    return f"""
    <div class="card">
        <h2>{escape(path.name)}</h2>
        <pre>{escape(json.dumps(snapshot.get("state", {}), indent=2))}</pre>
    </div>
    """


def dashboard(args):
    snapshots_dir = Path("snapshots")
    state_dir = Path("state")

    snapshot_files = sorted(snapshots_dir.glob("*.json"))
    state_files = sorted(state_dir.glob("*.json")) if state_dir.exists() else []

    snapshot_sections = "\n".join(
        snapshot_card(path)
        for path in snapshot_files
    ) or "<p>No snapshots found</p>"

    state_sections = "\n".join(
        state_card(path)
        for path in state_files
    ) or "<p>No state snapshots found</p>"

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>mockllm dashboard</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 40px;
        }}

        h1 {{
            margin-bottom: 32px;
        }}

        .section {{
            margin-bottom: 48px;
        }}

        .card {{
            background: white;
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}

        pre {{
            background: #f0f0f0;
            border-radius: 6px;
            padding: 12px;
            overflow-x: auto;
        }}
    </style>
</head>

<body>

    <h1>mockllm dashboard</h1>

    <div class="section">
        <h2>Snapshots</h2>
        {snapshot_sections}
    </div>

    <div class="section">
        <h2>State snapshots</h2>
        {state_sections}
    </div>

</body>
</html>
"""

    output = Path("mockllm-dashboard.html")
    output.write_text(html)

    print(f"generated dashboard: {output}")

    if args.open:
        webbrowser.open(output.resolve().as_uri())
