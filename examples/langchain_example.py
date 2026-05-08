from langchain_openai import ChatOpenAI


def main():
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key="mock-key",
        base_url="http://localhost:8000/v1",
    )

    response = llm.invoke("hello")

    print("\n=== LangChain Response ===\n")
    print(response.content)


if __name__ == "__main__":
    main()
