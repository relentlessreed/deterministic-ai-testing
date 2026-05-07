# deterministic-ai-testing

> Playwright for AI agents.
>
> Deterministic OpenAI-compatible testing infrastructure for AI applications, agents, and CI pipelines.

---

## The problem

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

## The solution

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

## Why developers use this

Instead of paying for real inference during tests:

```text
frontend -> real OpenAI API

