from pathlib import Path

from .common import post_chat, load_json


def replay_conversation(args):
    path = Path(args.file)

    if not path.exists():
        print(f"conversation file not found: {path}")
        return 1

    conversation = load_json(path)

    model = conversation.get("model", "gpt-4o")
    messages = conversation.get("messages", [])

    if not messages:
        print("no messages found")
        return 1

    for index, message in enumerate(messages, start=1):
        request = {
            "model": model,
            "messages": [message],
        }

        print(f"--- message {index} ---")
        print(f"user: {message.get('content', '')}")

        response = post_chat(args.base_url, request)

        assistant = (
            response["choices"][0]["message"]
            .get("content") or ""
        )

        if assistant:
            print(f"assistant: {assistant}")

        tool_calls = (
            response["choices"][0]["message"]
            .get("tool_calls") or []
        )

        if tool_calls:
            print("tool calls:")

            for tool_call in tool_calls:
                name = tool_call.get("function", {}).get("name")
                print(f"  - {name}")

        print()
