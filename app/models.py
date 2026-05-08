from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChatCompletionRequest(BaseModel):
    model: str = "gpt-4o"
    messages: List[ChatMessage]
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Any] = None


class CompletionRequest(BaseModel):
    model: str = "gpt-4o"
    prompt: Any
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class EmbeddingsRequest(BaseModel):
    model: str = "text-embedding-3-small"
    input: Any


class ScenarioMatch(BaseModel):
    contains: Optional[str] = None
    exact: Optional[str] = None
    regex: Optional[str] = None


class ScenarioResponse(BaseModel):
    content: str = "Mock response."
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ScenarioError(BaseModel):
    status_code: int = 500
    message: str = "Mock error."


class Scenario(BaseModel):
    name: str = "unnamed scenario"
    match: ScenarioMatch = Field(default_factory=ScenarioMatch)
    response: Optional[ScenarioResponse] = None
    error: Optional[ScenarioError] = None


class ResponsesRequest(BaseModel):
    model: str = "gpt-4o"
    input: Any
    stream: bool = False
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Any] = None
