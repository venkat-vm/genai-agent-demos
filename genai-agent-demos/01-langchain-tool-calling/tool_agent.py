"""
LangChain Tool-Calling Agent — Multi-Step Tool Orchestration Demo

Demonstrates the core "plan -> act -> observe -> repeat" agent loop:
the model decides which tool(s) to call, in what order, based on the
user's request — chaining two tool calls together when the second
depends on the first's result.

Requires: pip install langchain langchain-google-genai
Requires: GOOGLE_API_KEY environment variable set (see README)
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b


def extract_text(message) -> str:
    """
    Gemini 3.x returns content as a list of structured blocks rather than
    a plain string. This normalizes either format into clean text.
    """
    if isinstance(message.content, list):
        return "".join(
            block.get("text", "") for block in message.content if isinstance(block, dict)
        )
    return message.content


def main():
    tools = [get_word_length, multiply]

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # create_agent (LangChain 1.x) replaces the deprecated
    # create_tool_calling_agent + AgentExecutor pattern from pre-1.0 LangChain.
    # It's built on LangGraph internally.
    agent = create_agent(llm, tools)

    result = agent.invoke({
        "messages": [
            ("human", "What is the length of the word 'engineering', multiplied by 3?")
        ]
    })

    print("\n=== FINAL ANSWER ===")
    print(extract_text(result["messages"][-1]))


if __name__ == "__main__":
    main()
