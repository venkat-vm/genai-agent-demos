# LangChain Tool-Calling Agent

## What this demonstrates
The core agentic AI pattern — **plan → act → observe → repeat**: an LLM
decides which tool(s) to call, executes them, and chains multiple tool calls
together when a task requires sequential steps.

Two simple tools are defined:
- `get_word_length(word)` — returns a word's character count
- `multiply(a, b)` — multiplies two integers

Given the prompt *"What is the length of the word 'engineering', multiplied
by 3?"*, the agent must:
1. Recognize it needs `get_word_length` first
2. Call it, get `11` back
3. Recognize it now needs `multiply(11, 3)`
4. Call that, get `33` back
5. Synthesize both results into a final natural-language answer

This is a real, working demonstration of multi-step tool orchestration —
not a single tool call, but the model correctly sequencing two dependent
steps on its own.

## Why this matters
Modern backend/platform roles increasingly involve integrating LLM-driven
features — this demo shows the underlying mechanics: how tools are
described to a model, how the model decides when to invoke them, and how
results flow back into the reasoning loop. The same resilience patterns
that apply to any external API call (timeouts, retries, validating
untrusted input) apply here too — an LLM's tool-call arguments should never
be trusted blindly, same as any other external input.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com)
(Get API Key → Create API key), then:

```bash
export GOOGLE_API_KEY="your-key-here"   # Windows: $env:GOOGLE_API_KEY = "your-key-here"
```

## Run it

```bash
python tool_agent.py
```

Expected output:
```
=== FINAL ANSWER ===
The length of the word 'engineering' is 11.

Multiplied by 3, the result is 33.
```

## Switching to a different LLM provider

LangChain abstracts the model behind a common interface — the agent, tools,
and orchestration logic (everything except the `llm =` line) stay identical
regardless of provider. Only two things change per provider: the **import**
and the **package to install**.

### Anthropic (Claude)

**Prerequisite:** an Anthropic API key from
[console.anthropic.com](https://console.anthropic.com), with billing/credits
added — note this is separate from a claude.ai chat subscription, which does
NOT include API access.

```bash
pip install langchain-anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
```

### OpenAI (GPT)

**Prerequisite:** an OpenAI API key from
[platform.openai.com](https://platform.openai.com), with billing/credits
added.

```bash
pip install langchain-openai
export OPENAI_API_KEY="your-key-here"
```

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

### Google (Gemini) — what this module uses by default

**Prerequisite:** a free Gemini API key from
[aistudio.google.com](https://aistudio.google.com) — no billing required for
the free tier, though it carries rate limits.

```bash
pip install langchain-google-genai
export GOOGLE_API_KEY="your-key-here"
```

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
```

**Everything below the `llm =` line — `tools`, `create_agent(llm, tools)`,
`.invoke()` — needs no changes at all when switching providers.** This is
the actual value LangChain provides: provider-agnostic agent logic.

## Notes on framework/model churn
This code targets **LangChain 1.x**, which consolidated agent construction
around a single `create_agent` function (built on LangGraph internally),
replacing the older `create_tool_calling_agent` + `AgentExecutor` pattern
used in pre-1.0 LangChain — that older pattern is no longer importable as
of LangChain 1.0.

Model names also move fast: `gemini-1.5-flash` and the entire Gemini 2.0
line have been fully shut down as of this writing. `gemini-2.5-flash` is
used here as the current stable baseline; Google's newest generation
(3.x) is also available and evolving quickly. Pin model versions
deliberately in production code rather than assuming a name stays valid.
