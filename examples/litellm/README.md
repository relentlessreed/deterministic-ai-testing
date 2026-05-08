# LiteLLM integration

Install dependencies in a separate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate

pip install litellm
```

Start the mock server from the repository root:

```bash
uvicorn app.main:app --reload --port 8000
```

Run the example from the repository root:

```bash
python examples/litellm/example.py
```

This example routes LiteLLM through the local OpenAI-compatible mock server.
