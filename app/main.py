import asyncio
import json
import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.models import ChatCompletionRequest, CompletionRequest, EmbeddingsRequest, ResponsesRequest
from app.openai_compat import chat_completion_response, completion_response, embeddings_response, responses_response
from app.scenarios import DEFAULT_RESPONSE, find_matching_scenario, messages_to_prompt
from app.validation import validate_scenarios_file


app = FastAPI(
    title="Deterministic AI Testing",
    description="OpenAI-compatible mock LLM server for deterministic AI testing.",
    version="0.3.0",
)


SCENARIO_SEQUENCE_STATE = {}


def scenario_key(scenario: dict) -> str:
    return scenario.get("name") or json.dumps(scenario.get("match", {}), sort_keys=True)


def resolve_scenario_step(scenario: dict | None) -> dict | None:
    if not scenario:
        return None

    sequence = scenario.get("response_sequence")
    if not sequence:
        return scenario

    key = scenario_key(scenario)
    index = SCENARIO_SEQUENCE_STATE.get(key, 0)
    SCENARIO_SEQUENCE_STATE[key] = index + 1

    if index >= len(sequence):
        index = len(sequence) - 1

    return sequence[index]


def raise_scenario_error(step: dict | None):
    if step and step.get("error"):
        error = step["error"]
        raise HTTPException(
            status_code=error.get("status_code", 500),
            detail={
                "error": {
                    "message": error.get("message", "Mock error."),
                    "type": "mock_error",
                    "code": error.get("status_code", 500),
                }
            },
        )


def scenario_content_and_tools(step: dict | None):
    content = DEFAULT_RESPONSE
    tool_calls = None

    if step and step.get("response"):
        response = step["response"]
        content = response.get("content", DEFAULT_RESPONSE)
        tool_calls = response.get("tool_calls")

    return content, tool_calls


def load_scenarios():
    path = "scenarios/default.yaml"

    try:
        return validate_scenarios_file(path)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[scenario validation error] {e}")
        raise


@app.get("/health")
def health():
    return {"status": "ok", "service": "deterministic-ai-testing"}


@app.get("/")
def root():
    return {
        "name": "deterministic-ai-testing",
        "description": "OpenAI-compatible mock LLM server for deterministic AI testing.",
        "docs": "/docs",
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    scenarios = load_scenarios()
    prompt = messages_to_prompt(request.messages)
    scenario = find_matching_scenario(prompt, scenarios)

    step = resolve_scenario_step(scenario)
    raise_scenario_error(step)
    content, tool_calls = scenario_content_and_tools(step)

    if request.stream:
        return StreamingResponse(
            stream_chat_response(request.model, content),
            media_type="text/event-stream",
        )

    return chat_completion_response(request.model, content, tool_calls=tool_calls)


async def stream_chat_response(model: str, content: str):
    words = content.split() or [""]
    stream_id = f"chatcmpl-mock-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    for word in words:
        chunk = {
            "id": stream_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": word + " "},
                    "finish_reason": None,
                }
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.02)

    final_chunk = {
        "id": stream_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop",
            }
        ],
    }

    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    scenarios = load_scenarios()
    prompt = request.prompt if isinstance(request.prompt, str) else json.dumps(request.prompt)
    scenario = find_matching_scenario(prompt, scenarios)

    step = resolve_scenario_step(scenario)
    raise_scenario_error(step)
    content, _ = scenario_content_and_tools(step)

    if request.stream:
        return StreamingResponse(
            stream_completion_response(request.model, content),
            media_type="text/event-stream",
        )

    return completion_response(request.model, content)


async def stream_completion_response(model: str, content: str):
    words = content.split() or [""]
    stream_id = f"cmpl-mock-{uuid.uuid4().hex[:12]}"
    created = int(time.time())

    for word in words:
        chunk = {
            "id": stream_id,
            "object": "text_completion",
            "created": created,
            "model": model,
            "choices": [
                {
                    "text": word + " ",
                    "index": 0,
                    "finish_reason": None,
                }
            ],
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.02)

    yield "data: [DONE]\n\n"


def responses_input_to_prompt(input_value):
    if isinstance(input_value, str):
        return input_value

    if isinstance(input_value, list):
        parts = []
        for item in input_value:
            if isinstance(item, dict):
                content = item.get("content")
                if isinstance(content, str):
                    parts.append(content)
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            text = block.get("text")
                            if text:
                                parts.append(str(text))
                else:
                    parts.append(json.dumps(item))
            else:
                parts.append(str(item))
        return "\n".join(parts)

    return json.dumps(input_value)


@app.post("/v1/responses")
async def responses(request: ResponsesRequest):
    scenarios = load_scenarios()
    prompt = responses_input_to_prompt(request.input)
    scenario = find_matching_scenario(prompt, scenarios)

    step = resolve_scenario_step(scenario)
    raise_scenario_error(step)
    content, _ = scenario_content_and_tools(step)

    return responses_response(request.model, content)


@app.post("/v1/embeddings")
async def embeddings(request: EmbeddingsRequest):
    return embeddings_response(request.model, request.input)
