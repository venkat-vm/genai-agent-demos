# Google ADK Tool-Calling Agent

## What this demonstrates
The same multi-step tool-orchestration task as [Module 1](../01-langchain-tool-calling),
implemented in Google's **Agent Development Kit (ADK)** — built specifically
to directly compare the two frameworks' approaches to identical logic.

Given *"What is the length of the word 'engineering', multiplied by 3?"*,
the agent must call `get_word_length`, then feed that result into `multiply`
— chaining two dependent tool calls, not just a single lookup.

## LangChain vs. ADK — the real differences observed hands-on

| Aspect | LangChain (`create_agent`) | Google ADK (`Agent`) |
|---|---|---|
| Tool definition | Explicit `@tool` decorator required | Convention-based — infers schema from docstring + type hints, no decorator |
| Execution model | Single `.invoke()` call, returns final result | Session-based `Runner`, iterates over a stream of `events` |
| Best fit | Simple, one-shot agent calls | Multi-turn conversations where session state matters from the start |
| Maturity/API stability | Consolidated around `create_agent` as of LangChain 1.x (older `AgentExecutor` pattern removed) | Newer framework, actively evolving — some methods (e.g. `create_session_sync`) already flagged for async migration |

Both frameworks correctly solved the identical task with identical output
(11 × 3 = 33) — the underlying "plan → act → observe → repeat" agent loop is
the same; these are two different ergonomic approaches to building it.

## Setup

\```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
\```

Uses the same `GOOGLE_API_KEY` as Module 1:
\```bash
export GOOGLE_API_KEY="your-key-here"   # Windows: $env:GOOGLE_API_KEY = "your-key-here"
\```

## Run it

\```bash
python agent.py
\```

Expected output:
\```
=== AGENT RUN ===
The length of the word 'engineering' is 11, and 11 multiplied by 3 is **33**.

=== DONE ===
\```

## Notes
- `create_session_sync` currently prints a deprecation warning pointing to
  ADK's newer async session API — functionally fine for this demo, but
  worth migrating in a longer-lived project.
- The `JSON_SCHEMA_FOR_FUNC_DECL` warning reflects that ADK's docstring/
  type-hint-based tool-schema inference is still marked experimental
  internally — expected, not a bug.
