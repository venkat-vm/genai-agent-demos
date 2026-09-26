"""
Google ADK Tool-Calling Agent — Multi-Step Tool Orchestration Demo

Same task and tools as the LangChain module (../01-langchain-tool-calling),
implemented in Google's Agent Development Kit — for a direct, hands-on
comparison of how the two frameworks approach the same problem.

Requires: pip install google-adk
Requires: GOOGLE_API_KEY environment variable set (see README)
"""

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types


def get_word_length(word: str) -> dict:
    """Returns the length of a word.

    Args:
        word: The word to measure.

    Returns:
        dict with the word's length.
    """
    return {"length": len(word)}


def multiply(a: int, b: int) -> dict:
    """Multiplies two integers together.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        dict with the product.
    """
    return {"result": a * b}


# ADK infers each tool's schema from its docstring and type hints directly —
# no explicit decorator needed, unlike LangChain's @tool. Convention over
# decoration is the core API-design difference between the two frameworks.
root_agent = Agent(
    name="tool_calling_demo",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant with access to tools. Use them when needed.",
    tools=[get_word_length, multiply],
)


def main():
    runner = InMemoryRunner(agent=root_agent)

    session = runner.session_service.create_session_sync(
        app_name=runner.app_name, user_id="demo_user"
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text="What is the length of the word 'engineering', multiplied by 3?")],
    )

    print("\n=== AGENT RUN ===")
    for event in runner.run(
        user_id="demo_user", session_id=session.id, new_message=user_message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
