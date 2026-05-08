from litellm import completion


def main():
    response = completion(
        model="openai/gpt-4o",
        api_key="mock-key",
        api_base="http://localhost:8000/v1",
        messages=[
            {"role": "user", "content": "hello"},
        ],
    )

    print("\n=== LiteLLM Response ===\n")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
