# deterministic-ai-testing

**Playwright for AI agents — deterministic OpenAI-compatible testing infrastructure.**

A local mock LLM server for testing AI apps, agents, chat UIs, RAG pipelines, and CI workflows without calling real model APIs.

## Why this exists

Real LLMs make tests slow, expensive, and flaky.

This project gives you:

- deterministic AI outputs
- OpenAI-compatible endpoints
- local/offline development
- CI-safe LLM mocking
- programmable YAML scenarios
- streaming response simulation
- tool/function-call mocking
- rate-limit and failure simulation
- Docker support

## 60-second start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

## Use with OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(api_key="mock-key", base_url="http://localhost:8000/v1")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)

print(response.choices[0].message.content)
```

## Test with curl

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"hello"}]}'
```

## Scenarios

Scenarios live in `scenarios/default.yaml`.

```yaml
- name: refund request
  match:
    contains: refund
  response:
    content: Refund approved. Your money will be returned in 3-5 business days.
```

## Docker

```bash
docker build -t deterministic-ai-testing .
docker run -p 8000:8000 deterministic-ai-testing
```

Or:

```bash
docker compose up
```

## Run tests

```bash
pytest
```

## Product positioning

This is not just a fake OpenAI server.

The bigger product is:

> Deterministic AI testing infrastructure for AI apps and agents.

Future paid features:

- hosted team dashboard
- snapshot regression testing
- GitHub Action
- scenario sync
- agent replay
- audit logs
- private enterprise deployment
- flaky AI test detection
