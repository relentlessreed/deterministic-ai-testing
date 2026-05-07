# deterministic-ai-testing

## Playwright for AI agents.

Deterministic OpenAI-compatible testing infrastructure for AI apps, agents, RAG pipelines, and CI/CD.

Stop paying for flaky AI tests.

---

## Why this exists

Real LLMs make tests:

- slow
- expensive
- flaky
- nondeterministic
- hard to debug
- unsafe for CI

This project gives you a local OpenAI-compatible mock server with deterministic outputs.

Use it to test AI products without calling real model APIs.

---

## What it supports

- OpenAI-compatible `/v1/chat/completions`
- OpenAI-compatible `/v1/completions`
- OpenAI-compatible `/v1/embeddings`
- YAML scenario matching
- exact / contains / regex matching
- streaming responses
- tool/function-call mocks
- error and rate-limit simulation
- OpenAI SDK compatibility
- Docker support
- GitHub Actions CI

---

## 60-second start

```bash
git clone git@github.com:relentlessreed/deterministic-ai-testing.git
cd deterministic-ai-testing

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m uvicorn app.main:app --reload --port 8000
