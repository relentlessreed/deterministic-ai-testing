from pathlib import Path

from .common import load_json


def generate_html_report(args):
    target = Path(args.file)
    files = sorted(target.glob("*.json")) if target.is_dir() else [target]

    if not files:
        print(f"no snapshot files found: {target}")
        return 1

    sections = []

    for path in files:
        snapshot = load_json(path)

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

        .snapshot {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
        }}

        pre {{
            background: #f0f0f0;
            padding: 12px;
            overflow-x: auto;
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
