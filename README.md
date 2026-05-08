# deterministic-ai-testing

> Playwright for AI agents.
>
> Deterministic OpenAI-compatible testing infrastructure for AI applications, agents, and CI pipelines.

---

# The problem

AI applications are extremely difficult to test.

Real LLMs are:

- nondeterministic
- expensive
- slow
- flaky in CI
- hard to reproduce
- difficult to debug

That breaks:

- automated tests
- agent workflows
- CI/CD pipelines
- regression testing
- local development

---

# The solution

`deterministic-ai-testing` is a local OpenAI-compatible mock server that gives you:

✅ deterministic outputs  
✅ reproducible AI tests  
✅ local/offline development  
✅ CI-safe LLM simulation  
✅ programmable scenarios  
✅ tool-call mocking  
✅ streaming simulation  
✅ rate-limit/error testing  

Without calling real model APIs.

---

# Why developers use this

Instead of paying for real inference during tests:

```text
frontend -> real OpenAI API
```

you can do:

```text
frontend -> deterministic-ai-testing
```

using only:

```python
base_url="http://localhost:8000/v1"
```

Everything else stays compatible.

---

# Snapshot Testing

Save deterministic AI outputs:

```bash
mockllm snapshot save snapshots/hello.json --prompt "hello"
```

Validate them later:

```bash
mockllm snapshot test snapshots/
```

Example output:

```text
PASS snapshots/hello.json
PASS snapshots/refund.json
```

This enables:

- deterministic regression testing
- CI-safe AI verification
- stable agent workflows
- reproducible LLM behavior

---

# Tool-call assertions

MockLLM includes assertion helpers for deterministic agent testing.

Example:

```python
from mockllm.assertions import (
    assert_tool_called,
    assert_tool_called_with,
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "find refund policy"}
    ],
)

assert_tool_called(response, "search_docs")

assert_tool_called_with(
    response,
    "search_docs",
    {"query": "refund policy"},
)
```

This enables:

- deterministic AI-agent testing
- orchestration verification
- workflow regression testing
- CI-safe agent assertions

---

# Demo

## Start the server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

---

## Health check

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok","service":"deterministic-ai-testing"}
```

---

## Chat completions

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"hello"}]}'
```

Expected:

```json
{
  "choices": [
    {
      "message": {
        "content": "Hello from MockLLM. This response is deterministic."
      }
    }
  ]
}
```

---

## Tool-call mocking

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"please use tool"}]}'
```

Expected:

```json
{
  "tool_calls": [
    {
      "function": {
        "name": "search_docs"
      }
    }
  ]
}
```

---

## Error simulation

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"rate limit"}]}'
```

Expected:

```json
{
  "detail": {
    "error": {
      "message": "Rate limit exceeded by mock scenario."
    }
  }
}
```

---

## Streaming simulation

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","stream":true,"messages":[{"role":"user","content":"hello"}]}'
```

---

## OpenAI SDK compatibility

Works with the official OpenAI SDK.

```python
from openai import OpenAI

client = OpenAI(
    api_key="mock-key",
    base_url="http://localhost:8000/v1",
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "hello"}
    ],
)

print(response.choices[0].message.content)
```

Run:

```bash
python3 examples/openai_sdk_example.py
```

---

## 60-Second Quickstart

Install directly from PyPI:

```bash
pip install deterministic-ai-testing
```

Start the MockLLM server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Verify the server is running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "deterministic-ai-testing"
}
```

Save a deterministic AI snapshot:

```bash
mockllm snapshot save snapshots/hello.json --prompt "hello"
```

Run snapshot tests:

```bash
mockllm snapshot test snapshots/
```

Expected output:

```text
PASS snapshots/hello.json
PASS snapshots/refund.json
```

Run MockLLM with Docker:

```bash
docker compose up --build
```

Use with the OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="mock-key",
    base_url="http://localhost:8000/v1",
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "hello"}
    ],
)

print(response.choices[0].message.content)
```

Example deterministic response:

```text
Hello User - this mock response changed live from YAML.
```

Run the included example:

```bash
python examples/openai_sdk_example.py
```


---

# Features

## OpenAI-compatible endpoints

- `/v1/chat/completions`
- `/v1/completions`
- `/v1/embeddings`

---

## Deterministic scenario engine

Supports:

- exact matching
- contains matching
- regex matching

---

## YAML scenarios

Edit:

```bash
scenarios/default.yaml
```

Example:

```yaml
- name: refund request
  match:
    contains: refund
  response:
    content: Refund approved. Your money will be returned in 3-5 business days.
```

Live edits apply immediately.

No recompilation required.

---

## Tool-call simulation

Mock:

- function calls
- tool invocations
- agent actions
- assistant tool responses

Useful for:

- agent testing
- orchestration testing
- frontend AI development

---

## Failure simulation

Test:

- rate limits
- retries
- API failures
- fallback logic
- degraded AI behavior

---

## Streaming support

Simulate streaming token responses locally.

Useful for:

- chat UIs
- token rendering
- frontend streaming logic
- websocket/SSE behavior

---

## Embeddings support

Includes deterministic fake embeddings for:

- RAG testing
- retrieval simulation
- vector pipeline testing
- semantic search development

---

## CI-safe AI testing

Run deterministic AI tests in:

- GitHub Actions
- CI/CD pipelines
- local test suites

without paying for inference.

---

# Testing

Run all tests:

```bash
python -m pytest
```

---

# Docker

## Run locally

```bash
docker compose up --build
```

Then test:

```bash
curl http://localhost:8000/health
```

---

# Example use cases

- AI app testing
- AI agent testing
- LangChain testing
- RAG testing
- frontend AI UI development
- CI/CD pipelines
- retry/fallback testing
- local AI simulation
- offline AI development
- deterministic regression testing

---

# Architecture

```text
application
    ↓
OpenAI SDK
    ↓
deterministic-ai-testing
    ↓
deterministic YAML scenarios
```

---

# Roadmap

Planned features:

- snapshot diffing
- GitHub Actions integration
- installable CLI
- scenario validation
- tool-call assertions
- agent replay
- multi-agent workflows
- hosted team dashboard

---

# Product vision

This is not just an OpenAI mock server.

The goal is to become:

> deterministic AI testing infrastructure

for the next generation of AI-native software.

or:

> Playwright for AI agents.

---

# Why this matters

The next major software wave is:

- AI infrastructure
- agent orchestration
- deterministic testing
- AI observability
- developer workflow acceleration

AI software requires a new testing stack.

This project is part of that stack.

---

# Contributing

Contributions are welcome.

Especially:

- OpenAI compatibility improvements
- snapshot testing
- LangChain examples
- CLI tooling
- GitHub Actions
- scenario validation
- agent testing workflows

---

# License

MIT

## Snapshot diffs

When a snapshot fails, MockLLM shows a unified diff:

```text
FAIL snapshots/hello.json
expected exact:
BROKEN EXPECTED OUTPUT

actual:
Hello User - this mock response changed live from YAML.

diff:
--- expected
+++ actual
@@ -1 +1 @@
-BROKEN EXPECTED OUTPUT
+Hello User - this mock response changed live from YAML.
```

This makes AI output regressions easy to debug in local development and CI pipelines.

---

## Scenario validation

MockLLM validates `scenarios/default.yaml` before using it.

It catches:

- missing `match`
- missing `response` or `error`
- invalid scenario structure
- scenarios that define both `response` and `error`

This helps teams fail fast when test scenarios are malformed.

# Multi-step workflow snapshots

MockLLM can validate deterministic tool workflows inside snapshots.

Example:

```json
{
  "name": "tool-workflow",
  "request": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": "please use tool"
      }
    ]
  },
  "expected": {
    "tool_name": "search_docs",
    "tool_order": [
      "search_docs"
    ]
  }
}

## LangChain integration

`deterministic-ai-testing` works with LangChain through the OpenAI-compatible chat completions API.

Install the LangChain OpenAI adapter:

```bash
pip install langchain-openai
```

Start the mock server:

```bash
uvicorn app.main:app --reload --port 8000
```

Run the example:

```bash
python examples/langchain_example.py
```

Example:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    api_key="mock-key",
    base_url="http://localhost:8000/v1",
)

response = llm.invoke("hello")
print(response.content)
```

The request is routed to the local mock server at `/v1/chat/completions`, making LangChain workflows deterministic and testable.

## Docker

Run the mock server with Docker:

```bash
docker run --rm -p 8000:8000 ghcr.io/relentlessreed/deterministic-ai-testing:latest
```

Verify the server is running:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"deterministic-ai-testing"}
```

Send a mock chat completion request:

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"hello"}]}' | python -m json.tool
```

## CLI server

Start the local mock server with:

```bash
mockllm serve
```

Use a custom host or port:

```bash
mockllm serve --host 0.0.0.0 --port 8000
```

Enable reload during development:

```bash
mockllm serve --reload
```

## Project initialization

Create a starter deterministic AI testing project with:

```bash
mockllm init
```

This creates:

```text
scenarios/default.yaml
snapshots/
tests/test_ai.py
```

Then start the mock server:

```bash
mockllm serve
```

## HTML snapshot reports

Generate a static HTML report for snapshots:

```bash
mockllm snapshot report snapshots
```

This creates:

```text
mockllm-report.html
```

Open it in a browser to inspect prompts, expected outputs, and recorded responses.

## Retry and failure workflow testing

Scenarios can model transient failures with `response_sequence`:

```yaml
- name: retry-flow
  match:
    contains: retry sequence
  response_sequence:
    - error:
        status_code: 429
        message: Rate limit, try again.
    - response:
        content: Recovered after retry.
```

Each matching request advances the sequence. After the last step, the final step is reused.

## Conversation replay

Replay a conversation file against the local mock server:

```bash
mockllm replay examples/replay/conversation.json
```

Example conversation file:

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "hello"},
    {"role": "user", "content": "please use tool"}
  ]
}
```

Replay sends each message to the mock server and prints deterministic assistant responses and tool calls.

## Memory and state snapshots

Save a workflow or agent state snapshot:

```bash
mockllm state save state/current.json --name checkout-agent --json '{"step":"payment","memory":{"user_intent":"refund"}}'
```

Validate current state against a saved snapshot:

```bash
mockllm state test state/current.json --json '{"step":"payment","memory":{"user_intent":"refund"}}'
```

State snapshot diffs show expected and actual JSON when workflow state changes.

## Local dashboard

Generate a local dashboard for snapshots and state snapshots:

```bash
mockllm dashboard
```

This creates:

```text
mockllm-dashboard.html
```

Open it in a browser to inspect available snapshot and state snapshot files.

## v0.3.0 quickstart

```bash
pip install deterministic-ai-testing
mockllm init
mockllm serve
```

In another terminal:

```bash
mockllm snapshot save snapshots/hello.json --prompt "hello"
mockllm snapshot test snapshots
mockllm snapshot report snapshots
mockllm dashboard
```

Additional workflows:

```bash
mockllm replay examples/replay/conversation.json
mockllm state save state/current.json --name checkout-agent --json '{"step":"payment"}'
mockllm state test state/current.json --json '{"step":"payment"}'
```
