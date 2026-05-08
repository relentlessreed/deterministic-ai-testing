# Vercel AI SDK integration

This example uses the Vercel AI SDK with the local OpenAI-compatible mock server.

## Install

Use a separate Node environment for this example:

```bash
cd examples/vercel-ai-sdk
npm install
```

## Start the mock server

From the repository root:

```bash
uvicorn app.main:app --reload --port 8000
```

## Run the example

From `examples/vercel-ai-sdk`:

```bash
npm start
```

Expected output:

```text
=== Vercel AI SDK Response ===

Hello User - this mock response changed live from YAML.
```

The example uses `@ai-sdk/openai-compatible` to point the Vercel AI SDK at:

```text
http://localhost:8000/v1
```
